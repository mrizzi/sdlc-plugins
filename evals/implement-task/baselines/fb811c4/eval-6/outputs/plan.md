# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001 (this task is incorporated by TC-9001)
**Dependencies:** None

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: Present, with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Present, with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), and GitHub Issue custom field (customfield_10747)
- **Code Intelligence**: Present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` (rust-analyzer)

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API via `scripts/jira-client.py` if MCP fails.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint pattern in `get.rs`, add `severity_summary` method to `AdvisoryService`, use `sbom_advisory` join table, count by severity level from `AdvisorySummary`, register route, use `AppError` with `.context()`, return struct directly via `Json`
- **Acceptance Criteria:** 5 items (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 test cases
- **Target PR:** Not present (default flow)
- **Bookend Type:** Not present (default flow)
- **Dependencies:** None

Capture `webUrl` from the issue response for PR description linking.

**GitHub Issue extraction:** The Jira Configuration has `GitHub Issue custom field: customfield_10747`. Check the issue's fields for this custom field. If present, extract and parse the GitHub issue URL. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

1. Fetch comments on TC-9201 via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment: one comment found with body `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
3. Comment edit detection: `created` == `updated` -- comment is unmodified, no warning
4. Extract stored digest: tag = `md`, hex = `a1b2c3d4e5f67890...` (format-tagged, not legacy)
5. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, output = `sha256-md:a1b2c3d4e5f67890...`
6. Compare format tags: both `md` -- tags match
7. Compare hex digests: **match**
8. **Outcome: proceed silently.** No user prompt, no warning, no delay.

## Step 2 -- Verify Dependencies

The task lists `Dependencies: None`. No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

Use `mcp__serena_backend__<tool>` for all code intelligence operations.

### 4.1 Inspect files to modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol("severity_summary")` to confirm it does not already exist
   - `mcp__serena_backend__find_symbol("fetch", include_body=true)` to understand the method pattern (parameters, return type, transaction handling)

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see current route registration pattern
   - Identify how routes are added (`Router::new().route(...)`)

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing module registrations
   - Confirm pattern for adding `pub mod severity_summary;`

4. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to understand the `severity` field type and structure

5. **`entity/src/sbom_advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to understand the join table structure

### 4.2 Check backward compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure adding a new method won't break existing code

### 4.3 Convention conformance analysis

**Sibling files to inspect:**
- `modules/fundamental/src/advisory/endpoints/get.rs` (sibling endpoint handler)
- `modules/fundamental/src/advisory/endpoints/list.rs` (sibling endpoint handler)
- `modules/fundamental/src/sbom/endpoints/get.rs` (cross-module sibling for SBOM-scoped endpoint pattern)
- `modules/fundamental/src/advisory/model/details.rs` (sibling model)

Use `mcp__serena_backend__get_symbols_overview` on each to discover conventions for:
- Error handling (expected: `Result<T, AppError>` with `.context()`)
- Naming (expected: `verb_noun` pattern for service methods)
- Endpoint registration pattern
- Response struct conventions (derive macros, serde attributes)
- Import organization

### 4.4 Test convention analysis

**Sibling test files:**
- `tests/api/advisory.rs` (advisory endpoint tests)
- `tests/api/sbom.rs` (SBOM endpoint tests)
- `tests/api/search.rs` (search endpoint tests)

Inspect for:
- Assertion style (expected: `assert_eq!(resp.status(), StatusCode::OK)`)
- Response validation patterns
- Error case coverage (404 tests)
- Test naming (`test_<endpoint>_<scenario>`)
- Setup/teardown patterns (database seeding, test fixtures)

### 4.5 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root. Read it if present. Extract:
- CI check commands (for Step 9)
- Code generation commands
- Any naming or structural conventions

### 4.6 Documentation file identification

Check for:
- `docs/api.md` (API documentation -- may need updating for new endpoint)
- `docs/architecture.md`
- `README.md` at repository root

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

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

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts.
#[derive(Clone, Debug, Default, Deserialize, Serialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

Follow existing model struct patterns (derive macros from sibling `summary.rs` and `details.rs`).

### 6.2 Register the model module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` following the pattern of existing module registrations.

### 6.3 Add `severity_summary` method to `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total. Advisories are deduplicated by advisory ID before
/// counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to this SBOM ID
    // 2. Verify SBOM exists (return 404 AppError if not)
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Error handling: use `.context("Failed to fetch severity summary")` wrapping, matching `common/src/error.rs` patterns.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: Extension<AdvisoryService>,
    tx: Extension<Transactional<'_>>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service.severity_summary(id, &tx).await?;
    Ok(Json(summary))
}
```

### 6.5 Register the route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route following existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation impact

Check if `docs/api.md` documents existing endpoints. If so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with request/response documentation.

### 6.7 Code quality verification

Ensure all new public symbols (`SeveritySummary`, `severity_summary`, `get_severity_summary`) have documentation comments as implemented above.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with integration tests following sibling test conventions:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that a valid SBOM with associated advisories returns correct per-severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisory severity distribution
    // (seed test data with specific critical/high/medium/low advisories)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK);
    // assert_eq!(body.critical, expected_critical);
    // assert_eq!(body.high, expected_high);
    // assert_eq!(body.medium, expected_medium);
    // assert_eq!(body.low, expected_low);
    // assert_eq!(body.total, expected_total);
}
```

### Test 2: Non-existent SBOM ID returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint

    // Then the response is 404 Not Found
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns zero counts for all severity levels.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary endpoint

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0);
    // assert_eq!(body.high, 0);
    // assert_eq!(body.medium, 0);
    // assert_eq!(body.low, 0);
    // assert_eq!(body.total, 0);
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links for the same SBOM are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary endpoint

    // Then the advisory is counted only once
    // assert_eq!(body.total, expected_unique_count);
}
```

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Test 1 validates response shape with actual values |
| 2 | Returns 404 when SBOM ID does not exist | Test 2 validates 404 response |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Test 4 validates deduplication logic |
| 4 | All severity levels default to 0 when no advisories exist | Test 3 validates zero defaults |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Verify via test execution time or manual benchmark |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Expected files:

Modified:
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

Created:
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files (e.g., if `docs/api.md` was updated, flag it and ask user approval since it is not listed in Files to Modify).

### Untracked file check

Run `git status --short`, filter for `??` entries in directories containing modified/created files. Check for code references to any untracked files.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency

Verify `docs/api.md` is still accurate if it documents endpoints. The new endpoint should be documented there if the file exists.

### CI checks from CONVENTIONS.md

Run any CI check commands extracted from CONVENTIONS.md (formatting, linting, compilation). Fix any failures. Hard stop on any non-zero exit.

### Data-flow trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (id) -> call `AdvisoryService::severity_summary(id)` -> query `sbom_advisory` join table -> fetch advisory severities -> count by level -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract & sibling parity

- `SeveritySummary` is a standalone struct (no trait/interface to implement) -- no contract gaps
- Sibling parity with `get.rs` endpoint handler: error handling (AppError), response pattern (Json), path extraction (Path<Id>) -- verify consistency
- No cross-module shared entity concerns (read-only query on `sbom_advisory`)

### Duplication check

Search for existing severity aggregation logic: `grep -r "severity" modules/fundamental/src/` to ensure no duplicate counting utilities exist.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total) for
advisories linked to a given SBOM. Includes deduplication by advisory ID
and proper 404 handling for missing SBOMs.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint \`GET /api/v2/sbom/{id}/advisory-summary\` that aggregates
vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets
to render severity breakdowns without client-side counting.

### Changes
- Added \`SeveritySummary\` response struct in \`advisory/model/severity_summary.rs\`
- Added \`severity_summary\` method to \`AdvisoryService\`
- Added GET handler and route registration for \`/api/v2/sbom/{id}/advisory-summary\`
- Added integration tests covering valid responses, 404, zero-advisory, and deduplication cases

Implements [TC-9201](<webUrl>)

## Test Plan
- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated in the count"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL in ADF format (inlineCard)

2. **Add Jira comment** summarizing changes made:
   - PR link
   - Summary: Added `SeveritySummary` model, `severity_summary` service method, GET endpoint at `/api/v2/sbom/{id}/advisory-summary`, and 4 integration tests
   - No deviations from the plan
   - Include the sdlc-workflow/implement-task footer with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. **Transition** TC-9201 to "In Review"
