# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

All validations pass. Proceeding.

## Step 0.5 -- JIRA Access Initialization

JIRA access will use MCP as the preferred method. If MCP fails at any step, prompt the user with fallback options (REST API, skip, or retry) per the skill specification.

## Step 1 -- Fetch and Parse Jira Task

Fetch via `jira.get_issue(TC-9201)`. Capture the `webUrl` field (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

Parsed sections from the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **GitHub Issue custom field**: Look up `customfield_10747` from the fetched issue; extract GitHub issue reference if present for PR description.

## Step 1.5 -- Verify Description Integrity

See `digest-match.md` for full details. Summary: the digest comment is located via the `[sdlc-workflow] Description digest:` marker, the stored `sha256-md` digest is compared against the computed digest from the current description using `scripts/sha256-digest.py`, the comment's created/updated timestamps match (no editing detected), and the hex digests match. Proceeding silently with no user prompt.

## Step 2 -- Verify Dependencies

No dependencies listed. Skipping.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue(TC-9201) -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__<tool>` for all Serena operations:

1. **`modules/fundamental/src/advisory/service/advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` method to understand the method signature pattern (takes `&self, id: Id, tx: &Transactional<'_>`) and return type pattern

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing route registrations
   - Understand the `Router::new().route(...)` pattern for adding new routes

3. **`modules/fundamental/src/advisory/model/mod.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations (`pub mod summary;`, `pub mod details;`)

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** (referenced pattern):
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to understand Path param extraction, service call, and JSON response pattern

5. **`modules/fundamental/src/advisory/model/summary.rs`**:
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` to understand the `severity` field type and structure

6. **`entity/src/sbom_advisory.rs`**:
   - `mcp__serena_backend__get_symbols_overview` to understand the join table entity columns and relations

7. **`common/src/error.rs`**:
   - `mcp__serena_backend__find_symbol` on `AppError` to understand error variants and `.context()` wrapping pattern

### 4.2 Check for Backward Compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure adding a new method doesn't break existing callers
- Confirm route registration pattern is additive (no conflicts with existing `/api/v2/sbom/{id}/*` routes)

### 4.3 Search for Reusable Code

- Check if any existing aggregation/counting utilities exist in `common/src/db/query.rs`
- Check if `PaginatedResults<T>` from `common/src/model/paginated.rs` is relevant (it is not -- this endpoint returns a fixed summary, not a paginated list)

### 4.4 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` (REST API reference) -- may need updating with new endpoint
- `docs/architecture.md` -- likely no change needed
- `CONVENTIONS.md` at repository root -- read for CI check commands and conventions

### 4.5 CONVENTIONS.md Lookup

Look for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Read it and extract:
- CI check commands (formatting, linting, compilation) for use in Step 9
- Code generation commands (e.g., OpenAPI spec generation) for Step 9
- Follow all naming rules, directory structure, code patterns, and test conventions

### 4.6 Convention Conformance Analysis

**Discovered conventions (from sibling analysis):**

- **Module structure**: Each domain (sbom, advisory, package) follows `model/ + service/ + endpoints/` structure consistently
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping (from `common/src/error.rs`)
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern**: Handlers extract path params via `Path<Id>`, call the service method, return `Json<T>` response
- **Route registration**: `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` chaining
- **Response types**: List endpoints use `PaginatedResults<T>`; detail endpoints return the model struct directly
- **Model structs**: Use `#[derive(Serialize, Deserialize)]` with serde; each model is in its own file under `model/`

### 4.7 Test Convention Analysis

**Discovered test conventions (from sibling test analysis of `tests/api/advisory.rs`, `tests/api/sbom.rs`):**

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` for success, `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404
- **Response validation**: Deserialize response body to the expected struct, then assert on specific field values
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern
- **Error cases**: Each endpoint test file includes a 404 test case
- **Setup**: Tests use a real PostgreSQL test database with fixture data

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the SeveritySummary response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides counts per severity level and a total count,
/// enabling dashboard widgets to render severity breakdowns.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Count of critical-severity advisories.
    pub critical: u32,
    /// Count of high-severity advisories.
    pub high: u32,
    /// Count of medium-severity advisories.
    pub medium: u32,
    /// Count of low-severity advisories.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

### 6.2 Register model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` alongside existing module declarations (`pub mod summary;`, `pub mod details;`).

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the existing pattern of `fetch` and `list` methods:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Returns counts per severity level (Critical, High, Medium, Low) and a total.
/// Advisories are deduplicated by advisory ID so each is counted at most once.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table to find advisory IDs linked to this SBOM
    // Join with advisory table to get severity field
    // Deduplicate by advisory ID
    // Count by severity level
    // Return SeveritySummary with counts defaulting to 0
    // Return 404 AppError if SBOM does not exist
}
```

Key implementation details:
- Use SeaORM query on `sbom_advisory` entity filtered by `sbom_id`
- Join with `advisory` entity to access the `severity` field from `AdvisorySummary`
- Use `DISTINCT` on advisory ID to deduplicate
- Group by severity and count, or fetch all and count in-memory
- First verify the SBOM exists (query `sbom` entity); return `AppError` with 404 context if not found
- Use `.context()` wrapping for all database errors

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Following the pattern in `endpoints/get.rs`:

```rust
use axum::{extract::Path, Json};
use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use common::db::Transactional;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all
/// advisories linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(sbom_id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(sbom_id, &tx)
        .await
        .context("Failed to retrieve advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the new route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the route following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

Import the new module: `mod severity_summary;`

### 6.6 Documentation Impact

- `docs/api.md`: Add documentation for `GET /api/v2/sbom/{id}/advisory-summary` with request/response format and examples
- No changes needed to `docs/architecture.md` (follows existing patterns, no architectural change)

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following the test conventions discovered in Step 4:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (setup: create test SBOM, create advisories with Critical=2, High=1, Medium=3, Low=0,
    //  link them via sbom_advisory)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 2);
    assert_eq!(summary.high, 1);
    assert_eq!(summary.medium, 3);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 6);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/nonexistent-id/advisory-summary").await;

    // Then the response is 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then all severity counts are zero
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM where the same advisory is linked multiple times
    // (setup: create one Critical advisory, link it via sbom_advisory twice)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 1);
    assert_eq!(summary.total, 1);
}
```

Register the test module in `tests/` if needed (e.g., add `mod advisory_summary;` to a test harness file).

Run tests:

```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by `test_advisory_summary_valid_sbom`
- [x] Returns 404 when SBOM ID does not exist -- verified by `test_advisory_summary_not_found`
- [x] Counts only unique advisories (deduplicates by advisory ID) -- verified by `test_advisory_summary_deduplicates`
- [x] All severity levels default to 0 when no advisories exist -- verified by `test_advisory_summary_no_advisories` and by `SeveritySummary` deriving `Default`
- [x] Response time under 200ms for SBOMs with up to 500 advisories -- ensured by single database query with GROUP BY rather than N+1 queries

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified/created files:
- `modules/fundamental/src/advisory/service/advisory.rs` (modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (create)
- `tests/api/advisory_summary.rs` (create)

Possibly out-of-scope (requiring user approval):
- `docs/api.md` -- documentation impact from Step 6 (justified by new endpoint)

### Untracked File Check

Run `git status --short` and check for `??` entries in directories where implementation occurred. For any untracked files in `modules/fundamental/src/advisory/` or `tests/api/`, check for code references and ask the user before staging.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Verify no secrets are present in the diff.

### Documentation Currency

Verify `docs/api.md` reflects the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Update if not already done in Step 6.

### Documentation Scope Preservation

If `docs/api.md` was modified, verify replacement text still covers all originally documented endpoints and scenarios.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any non-zero exit. Run any code generation commands (e.g., OpenAPI spec generation) and stage resulting file changes.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path param (input) -> call `AdvisoryService.severity_summary()` (processing: query DB, deduplicate, count) -> return `Json<SeveritySummary>` (output) -- **COMPLETE**

### Contract & Sibling Parity

- **SeveritySummary**: standalone struct, no trait contract to verify -- OK
- **Endpoint handler**: follows same `Result<Json<T>, AppError>` pattern as `get.rs` siblings -- parity OK
- **AdvisoryService.severity_summary**: follows same `(&self, id, tx) -> Result<T, AppError>` pattern as `fetch` and `list` -- parity OK
- **Error handling**: uses `.context()` wrapping matching all other service methods -- parity OK
- **Cross-module shared entity**: `sbom_advisory` table is used by `ingestor/graph/advisory/mod.rs` for inserts; new code only reads (SELECT) so no conflict in write patterns

### Duplication Check

Search for existing severity counting or aggregation logic. Verify no existing utility performs the same computation.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# If docs were updated:
git add docs/api.md

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add advisory severity aggregation endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM. The endpoint returns counts per severity level (Critical, High,
Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without
client-side counting.

### Changes
- New \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- New \`severity_summary\` method on \`AdvisoryService\`
- New GET handler at \`/api/v2/sbom/{id}/advisory-summary\`
- Integration tests covering valid SBOM, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
Closes <owner>/<repo>#<number> (if GitHub Issue custom field is populated)"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations. Include the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue(TC-9201) -> In Review
```
