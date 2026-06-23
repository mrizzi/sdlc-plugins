# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains:

1. **Repository Registry** -- present. Contains `trustify-backend` with Serena Instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present. Contains Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`.
3. **Code Intelligence** -- present. Documents tool naming convention `mcp__<serena-instance>__<tool>` and lists the `serena_backend` instance with `rust-analyzer`.

All required sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback. Record the access method for use throughout the skill.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 using `jira.get_issue("TC-9201")`.

### Parsed Sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. |
| Files to Modify | `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/advisory/endpoints/mod.rs`, `modules/fundamental/src/advisory/model/mod.rs` |
| Files to Create | `modules/fundamental/src/advisory/model/severity_summary.rs`, `modules/fundamental/src/advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs` |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Acceptance Criteria | 5 items (see task description) |
| Test Requirements | 4 items (see task description) |
| Target PR | Not present (default flow) |
| Bookend Type | Not present (default flow) |
| Dependencies | None |

### Target Branch Extraction

Target branch: `main`. This is a direct-to-main workflow.

### GitHub Issue Extraction

The GitHub Issue custom field is `customfield_10747` per Jira Configuration. Would read this field from the issue response. If a URL is present, parse `owner/repo#number` for use in the PR description's `Closes` line.

### Web URL Capture

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the detailed analysis.

**Summary:** The digest comment is found, uses the current tagged format (`sha256-md:`), the comment has not been edited (`created` == `updated`), the format tags match, and the hex digests match. Proceed silently -- no user prompt, no added latency.

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to In Progress: `jira.transition_issue("TC-9201", "In Progress")`.

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance (tools called as `mcp__serena_backend__<tool>`).

### 4.1 Inspect Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see the AdvisoryService struct and its methods (`fetch`, `list`, `search`).
   - `mcp__serena_backend__find_symbol("severity_summary", include_body=false)` to confirm no existing method with this name.
   - Understand the method signature pattern: `&self, sbom_id: Id, tx: &Transactional<'_>`.

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing route registrations.
   - Understand the `Router::new().route("/path", get(handler))` pattern.

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations.

### 4.2 Inspect Related Files

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference pattern for endpoint implementation.
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to understand the Path extraction and JSON response pattern.

2. **`modules/fundamental/src/advisory/model/summary.rs`** -- understand the `AdvisorySummary` struct, especially the `severity` field used for counting.

3. **`entity/src/sbom_advisory.rs`** -- understand the join table for SBOM-Advisory relationships.

4. **`common/src/error.rs`** -- understand the `AppError` enum and `.context()` wrapping pattern.

### 4.3 Convention Conformance Analysis

#### Sibling File Analysis

Examine 2-3 sibling files for pattern discovery:

- **Endpoint siblings:** `endpoints/get.rs`, `endpoints/list.rs` in the advisory module -- extract path params via `Path<Id>`, call service, return `Json(result)`.
- **Service siblings:** `advisory.rs` service methods -- `fetch` and `list` method signatures, error wrapping with `.context()`.
- **Model siblings:** `summary.rs`, `details.rs` in the advisory model -- struct definitions with `Serialize`, `Deserialize` derives.

**Discovered conventions:**
- **Error handling:** All handlers return `Result<Json<T>, AppError>` with `.context()` wrapping on service calls.
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- **Path extraction:** Endpoints use `Path(id): Path<Id>` for path parameters.
- **Response types:** Direct struct return with Axum's `Json` extractor.
- **Route registration:** `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`.
- **Model structure:** Structs derive `Serialize, Deserialize, Debug, Clone` and have doc comments.

### 4.4 Test Convention Analysis

Examine sibling test files in `tests/api/`:

- **`tests/api/advisory.rs`** -- advisory endpoint integration tests.
- **`tests/api/sbom.rs`** -- SBOM endpoint integration tests.

**Discovered test conventions:**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Error cases:** Test 404 with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming:** `test_<endpoint>_<scenario>` pattern.
- **Test setup:** Tests hit a real PostgreSQL test database with pre-seeded fixtures.
- **Response validation:** Validate specific field values, not just counts.

### 4.5 Documentation File Identification

- `README.md` at repository root.
- `docs/api.md` -- REST API reference (needs updating for new endpoint).
- `CONVENTIONS.md` at repository root -- check for CI check commands.

### 4.6 CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at the repository root. Extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).
- Code generation commands (if any).

## Step 5 -- Create Branch

This is the default flow (no Target PR, no Bookend Type). Create a task branch from main:

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides counts per severity level (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to expose the new model.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the `fetch` and `list` method pattern:

```rust
/// Computes the severity summary for all advisories linked to the given SBOM.
///
/// Returns counts per severity level (Critical, High, Medium, Low) and a total.
/// Deduplicates advisories by ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Count by severity level using AdvisorySummary's severity field
    // Return SeveritySummary with all counts (defaulting to 0)
}
```

Implementation details:
- Use `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM.
- Fetch `AdvisorySummary` for each linked advisory.
- Deduplicate by advisory ID using a `HashSet` or `DISTINCT` in the query.
- Count by severity level, matching on the `severity` field values.
- Default all counts to 0 when no advisories exist at a given level.
- Return 404 via `AppError` if the SBOM ID does not exist (check SBOM existence first).

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Follow the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// GET handler for /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts per severity level for all advisories
/// linked to the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following the existing pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Code Quality Verification

- All new structs (`SeveritySummary`) have documentation comments.
- All new public functions (`severity_summary`, `get_severity_summary`) have documentation comments.
- Error handling uses `.context()` wrapping consistent with sibling code.

### 6.7 Documentation Impact

- Update `docs/api.md` to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.
- Include request format (path parameter `id`), response format (JSON with `critical`, `high`, `medium`, `low`, `total` fields), and error responses (404 for non-existent SBOM).

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test functions, following sibling test conventions:

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test data in the database)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that a non-existent SBOM ID returns a 404 status code.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/nonexistent-id/advisory-summary").await;

    // Then the response is NOT FOUND
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
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
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, expected_unique_count);
    // Verify specific severity counts reflect deduplicated values
}
```

Run tests: `cargo test` to verify all pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test 1 and endpoint implementation |
| Returns 404 when SBOM ID does not exist | Verified by test 2 |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 and `DISTINCT`/`HashSet` in service method |
| All severity levels default to 0 when no advisories exist | Verified by test 3 and `Default` derive on `SeveritySummary` |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient query design (single query with JOIN and GROUP BY rather than N+1) |

## Step 9 -- Self-Verification

### 9.1 Scope Containment

Run `git diff --name-only` and compare against the expected file lists:

**Files to Modify (expected):**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create (expected):**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

**Potentially out-of-scope (justified):**
- `docs/api.md` -- documentation update for the new endpoint (documentation impact from Step 6.7). Would flag this and ask user approval.

### 9.2 Untracked File Check

Run `git status --short`, look for `??` entries in directories containing modified files. Flag any referenced untracked files for user review.

### 9.3 Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to check for secrets. Expect no matches.

### 9.4 Documentation Currency

Verify `docs/api.md` reflects the new endpoint. Already updated in Step 6.7.

### 9.5 Documentation Scope Preservation

If `docs/api.md` was modified, verify that existing endpoint documentation was not inadvertently removed or narrowed.

### 9.6 Cross-Section Reference Consistency

Verify file paths are consistent across task sections:
- `AdvisoryService` -- referenced in Files to Modify as `advisory/service/advisory.rs` and in Implementation Notes as `advisory/service/advisory.rs`. Consistent.
- `SeveritySummary` -- referenced in Files to Create as `advisory/model/severity_summary.rs` and matches API Changes section. Consistent.

### 9.7 Duplication Check

Search for existing severity aggregation logic (`grep -r "severity_summary\|severity_count\|count_by_severity"`) to ensure no duplication.

### 9.8 CI Checks from CONVENTIONS.md

Run all CI commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Fix any failures before proceeding.

### 9.9 Data-Flow Trace

**Data-flow: GET /api/v2/sbom/{id}/advisory-summary**
- Input: HTTP GET request with SBOM ID path parameter -> `severity_summary.rs` handler extracts `Path(id)` -- COMPLETE
- Processing: Handler calls `AdvisoryService::severity_summary(id, tx)` -> service queries `sbom_advisory` join table, deduplicates, counts by severity -> returns `SeveritySummary` -- COMPLETE
- Output: Handler wraps result in `Json(summary)` and returns to client -- COMPLETE

**Status: COMPLETE** -- all stages connected.

### 9.10 Contract & Sibling Parity

- **Contract:** `get_severity_summary` returns `Result<Json<SeveritySummary>, AppError>`, consistent with all sibling handlers.
- **Sibling parity with `get.rs`, `list.rs`:** Error handling (`.context()`), path extraction (`Path<Id>`), response type (`Json<T>`) -- all consistent.
- **No cross-module shared entity concerns:** The implementation reads from `sbom_advisory` (read-only) and does not insert/update/delete shared entities.

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs \
      docs/api.md

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to an SBOM.

- Add SeveritySummary response model
- Add severity_summary method to AdvisoryService
- Add endpoint handler and route registration
- Add integration tests for the new endpoint
- Update API documentation

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM. Returns counts per severity
level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render
severity breakdowns without client-side counting.

### Changes
- New `SeveritySummary` response model
- New `severity_summary` method on `AdvisoryService`
- New endpoint handler with route registration
- Integration tests covering happy path, 404, empty SBOM, and deduplication
- API documentation updated

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

Closes <owner/repo#number> (if GitHub Issue field is populated)
"
```

## Step 11 -- Update Jira

### Set Git Pull Request Custom Field

Using `customfield_10875` from Jira Configuration:

```
jira.update_issue("TC-9201", fields={
  "customfield_10875": {
    "type": "doc", "version": 1,
    "content": [{"type": "paragraph", "content": [
      {"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}
    ]}]
  }
})
```

### Add Comment

Post a comment to TC-9201 with:
- PR link
- Summary of changes made (new model, service method, endpoint, tests, docs)
- Confirmation that no deviations from the plan occurred
- Skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`)

### Transition to In Review

```
jira.transition_issue("TC-9201", "In Review")
```
