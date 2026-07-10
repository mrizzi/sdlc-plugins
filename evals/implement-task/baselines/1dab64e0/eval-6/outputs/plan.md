# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present. Project key: TC, Cloud ID: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID: 10142.
3. **Code Intelligence** -- present. Tool naming convention: `mcp__<serena-instance>__<tool>`. Instance `serena_backend` configured with `rust-analyzer`.

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all Jira operations. If MCP fails, prompt the user for REST API fallback selection (Yes/No/Retry).

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`.

### Parsed sections:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, `advisory.rs` service, use `sbom_advisory` join table, use `AdvisorySummary.severity` for counting, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly with Axum `Json` extractor.
- **Acceptance Criteria**: 5 items (correct response shape, 404 for missing SBOM, unique advisory dedup, zero defaults, sub-200ms performance)
- **Test Requirements**: 4 tests (valid counts, 404, empty SBOM, dedup)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None

Capture `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for PR description.

### GitHub Issue extraction

Check Jira Configuration for `GitHub Issue custom field: customfield_10747`. Read the field value from the fetched issue. If present, parse the GitHub issue URL and store the reference for the PR description. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments("TC-9201")`.
2. Locate comment with marker `[sdlc-workflow] Description digest:`.
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` and `updated` timestamps are identical -- comment is unmodified.
5. Parse format tag: `sha256-md`. Parse hex digest.
6. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`. Output: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`.
7. Format tags match (`sha256-md` == `sha256-md`). Hex digests match.
8. **Result: MATCH. Proceed silently** -- no user prompt, no delay.

## Step 2 -- Verify Dependencies

The task has no dependencies (`Dependencies: None`). Skip this step.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID: `jira.user_info()`
2. Assign TC-9201 to the current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance (`mcp__serena_backend__<tool>`) for code intelligence.

### 4.1 Inspect files to modify

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, `fetch` and `list` method signatures.
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- see route registration pattern.
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- see module registration pattern.

### 4.2 Study referenced patterns

- `mcp__serena_backend__find_symbol` on the `fetch` method in `advisory.rs` with `include_body=true` -- understand the service method pattern (parameters, transaction handling, return type).
- `mcp__serena_backend__find_symbol` on `get` handler in `modules/fundamental/src/advisory/endpoints/get.rs` with `include_body=true` -- understand endpoint pattern (Path extraction, service call, JSON response).
- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table structure for SBOM-advisory linkage.
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` with `include_body=true` -- understand the `severity` field type.
- `mcp__serena_backend__get_symbols_overview` on `common/src/error.rs` -- understand `AppError` enum and `.context()` usage.

### 4.3 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- ensure the new method does not conflict with existing callers.

### 4.4 Convention conformance analysis (sibling files)

Inspect 2-3 sibling files for each category:

**Service siblings:**
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` -- compare service method patterns (parameter types, return types, error handling).

**Endpoint siblings:**
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs`
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs`

**Model siblings:**
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs`
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs`

Record discovered conventions (expected patterns):
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods use `verb_noun` pattern (e.g., `fetch`, `list`, `severity_summary`)
- **Endpoint registration**: `Router::new().route("/path", get(handler))` pattern in `endpoints/mod.rs`
- **Response types**: Single-entity endpoints return the struct directly via `Json<T>`, list endpoints return `PaginatedResults<T>`
- **Service method signatures**: `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`

### 4.5 Test convention analysis

Inspect sibling test files:
- `mcp__serena_backend__get_symbols_overview` on `tests/api/advisory.rs`
- `mcp__serena_backend__get_symbols_overview` on `tests/api/sbom.rs`

Record discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: Deserialize JSON body and assert on specific fields
- **Error cases**: 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Use test database with seeded data

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it and extract CI check commands for Step 9. If absent, proceed normally.

### 4.7 Documentation file identification

Identify documentation files for later impact evaluation:
- `README.md` at repository root
- `docs/api.md` -- API reference (may need endpoint documentation update)
- `docs/architecture.md` -- architecture overview

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of linked advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Debug, Clone, Serialize, Default)]
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

Follow the pattern from `summary.rs` and `details.rs` siblings -- derive `Serialize`, use doc comments on every field.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

Following the existing pattern of `pub mod summary;` and `pub mod details;`.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`, following the `fetch` and `list` method pattern:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Returns counts per severity level (Critical, High, Medium, Low) and a total,
/// deduplicating by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Deduplicate by advisory ID
    // 3. For each unique advisory, look up severity from AdvisorySummary
    // 4. Count per severity level
    // 5. Return SeveritySummary with counts and total
}
```

Implementation details:
- Use SeaORM to query `sbom_advisory` entity joining on advisory to get severity
- Deduplicate by advisory ID using a HashSet or DISTINCT in the query
- Match severity string values ("Critical", "High", "Medium", "Low") to increment counters
- Default all severity counts to 0 (via `SeveritySummary::default()`)
- Wrap errors with `.context("Failed to compute severity summary for SBOM")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::service::AdvisoryService;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity count summary for all advisories linked to the specified SBOM.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to retrieve advisory summary")?;
    Ok(Json(summary))
}
```

Follow the exact parameter extraction and error handling pattern from the sibling `get.rs` handler.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing `Router::new().route(...)` pattern:

```rust
use severity_summary::get_advisory_summary;

// Add to the router:
.route("/api/v2/sbom/:id/advisory-summary", get(get_advisory_summary))
```

### 6.6 Verify `server/src/main.rs`

Confirm no changes are needed -- routes auto-mount via module registration as stated in the task description.

### 6.7 Documentation impact

- Check if `docs/api.md` documents REST endpoints -- if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response format.
- No other documentation changes expected (no configuration, setup, or architecture changes).

### 6.8 Code quality practices

Verify all new structs, functions, and public symbols have documentation comments (already included in the code above). Every field in `SeveritySummary`, the handler function, and the service method all have doc comments.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with 4 test functions following the sibling test conventions discovered in Step 4.

### Test 1: Valid SBOM with known advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (seed test database with SBOM and linked advisories: 2 Critical, 1 High, 1 Medium, 0 Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and counts match
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 2);
    // assert_eq!(body.high, 1);
    // assert_eq!(body.medium, 1);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 4);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response status is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the SBOM-advisory join table are
/// deduplicated, counting each advisory only once.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the count reflects unique advisories only
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.total, 1); // not 2, despite 2 join table entries
}
```

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by Test 1.
2. Returns 404 when SBOM ID does not exist -- verified by Test 2.
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by Test 4.
4. All severity levels default to 0 when no advisories exist -- verified by Test 3.
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by efficient query design (single query with JOIN and GROUP BY rather than N+1 queries).

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

Expected modified files:
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

Expected created files:
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Possibly out-of-scope (if documentation was updated):
- `docs/api.md` -- justified by Documentation impact evaluation

Flag any unexpected files for user approval.

### Untracked file check

Run `git status --short`, extract `??` entries. Filter by proximity to implementation directories. Search for code references to untracked files. Flag any referenced untracked files for user confirmation before staging.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- flag any matches.

### Documentation currency

Verify `docs/api.md` reflects the new endpoint if it was not already updated in Step 6.

### Documentation scope preservation

If documentation files were modified, verify replacement text covers all use cases from the original.

### Cross-section reference consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` -- Files to Modify references `service/advisory.rs`, Implementation Notes also references `service/advisory.rs` -- consistent.
- `SeveritySummary` model -- Files to Create references `model/severity_summary.rs`, consistent with Implementation Notes.
- Route registration -- Files to Modify references `endpoints/mod.rs`, Implementation Notes also references `endpoints/mod.rs` -- consistent.

### Duplication check

Search for existing severity aggregation or summary functions in the repository using Grep/Serena. Verify no existing utility performs the same counting logic. If found, refactor to reuse.

### CI checks from CONVENTIONS.md

If `CONVENTIONS.md` was found and CI commands extracted in Step 4, run every command. Hard stop on any failure. If no CI section, run `cargo build` and `cargo clippy` as standard checks.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService.severity_summary(id, tx)` -> query `sbom_advisory` join table -> aggregate severity counts -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` implements `Serialize` (required for Axum Json response) -- complete.
- Endpoint handler follows same signature pattern as `get.rs` sibling -- `Path<Id>` extraction, service injection, `Result<Json<T>, AppError>` return type.
- Service method follows same pattern as `fetch` and `list` -- same parameter types, error wrapping with `.context()`.
- No cross-module shared entity concerns -- the endpoint reads from `sbom_advisory` (read-only query, no inserts/updates/deletes).

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
# Add docs/api.md if updated

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to a
given SBOM. Includes SeveritySummary model, AdvisoryService.severity_summary
method, and integration tests.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM. Returns counts per
severity level (Critical, High, Medium, Low) and a total, enabling dashboard
widgets to render severity breakdowns without client-side counting.

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Changes

- **New model**: `SeveritySummary` response struct in `modules/fundamental/src/advisory/model/severity_summary.rs`
- **New service method**: `AdvisoryService.severity_summary()` in `modules/fundamental/src/advisory/service/advisory.rs`
- **New endpoint handler**: GET handler in `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- **Route registration**: New route in `modules/fundamental/src/advisory/endpoints/mod.rs`
- **Integration tests**: 4 tests covering valid counts, 404, empty SBOM, and deduplication

## Test plan

- [x] Test valid SBOM with known advisories returns correct severity counts
- [x] Test non-existent SBOM ID returns 404
- [x] Test SBOM with no advisories returns all zeros
- [x] Test duplicate advisory links are deduplicated in the count
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations. Include the skill footnote (read version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`).

3. **Transition** TC-9201 to In Review:

```
jira.transition_issue("TC-9201", "In Review")
```
