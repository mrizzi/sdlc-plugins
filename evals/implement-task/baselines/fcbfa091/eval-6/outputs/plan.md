# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

All sections are present and complete. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API v3 fallback using `scripts/jira-client.py`.

## Step 1 -- Fetch and Parse Jira Task

Fetch issue TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description.

**Parsed fields:**

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint patterns, use `sbom_advisory` join table, use `AdvisorySummary.severity` for counting, return `Result<T, AppError>` with `.context()` wrapping
- **Acceptance Criteria:** 5 items (correct response shape, 404 on missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 test cases
- **Bookend Type:** not present
- **Target PR:** not present
- **Dependencies:** None
- **GitHub Issue custom field:** check `customfield_10747` on the fetched issue; extract if present

Capture the issue's `webUrl` for PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

## Step 1.5 -- Verify Description Integrity

1. Fetch comments via `jira.get_issue_comments("TC-9201")`
2. Locate the digest comment -- one comment found with body starting with `[sdlc-workflow] Description digest:`
3. Check comment edit detection -- `created` equals `updated`, comment is unmodified
4. Extract stored digest: format tag `md`, hex digest `a1b2c3d4e5f67890...`
5. Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
6. Compare format tags: both `sha256-md` -- tags match
7. Compare hex digests: match confirmed

**Result:** Digests match. Proceed silently to Step 2 with no user prompt and no added latency.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using `mcp__serena_backend__<tool>`:

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`)
   - `find_symbol("severity_summary", include_body=false)` to confirm no existing method with this name
   - `find_symbol("list", include_body=true)` on AdvisoryService to understand the pattern: method signature, transaction handling, return type

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `get_symbols_overview` to see route registration pattern
   - `find_symbol` on the route registration function to see how existing routes like `get.rs` and `list.rs` are mounted

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Read to see existing `pub mod` declarations (summary, details)

### 4.2 Inspect Reference Files

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference for endpoint pattern
   - `get_symbols_overview` + `find_symbol` to understand: Path param extraction, service call, JSON response

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- reference for AdvisorySummary struct
   - `find_symbol("AdvisorySummary", include_body=true)` to see the `severity` field type and structure

6. **`entity/src/sbom_advisory.rs`** -- join table for SBOM-Advisory relationship
   - `get_symbols_overview` to understand the entity columns and relations

7. **`common/src/error.rs`** -- AppError enum
   - `find_symbol("AppError", include_body=true)` to understand error handling pattern

### 4.3 Check Backward Compatibility

- `find_referencing_symbols` on `AdvisoryService` to identify all callers and confirm that adding a new method does not break existing usage
- `find_referencing_symbols` on the advisory endpoints `mod.rs` router to see how it is mounted in the server

### 4.4 Convention Conformance Analysis

**Sibling files for endpoints:**
- `modules/fundamental/src/advisory/endpoints/get.rs`
- `modules/fundamental/src/advisory/endpoints/list.rs`
- `modules/fundamental/src/sbom/endpoints/get.rs` (cross-module sibling)

Examine for: naming conventions, error handling, parameter extraction, response types, import organization.

**Sibling files for models:**
- `modules/fundamental/src/advisory/model/summary.rs`
- `modules/fundamental/src/advisory/model/details.rs`
- `modules/fundamental/src/sbom/model/summary.rs`

Examine for: derive macros, field naming, documentation patterns, serialization attributes.

**Sibling files for service methods:**
- Existing `fetch` and `list` methods in `advisory.rs`
- `modules/fundamental/src/sbom/service/sbom.rs` for cross-module comparison

### 4.5 Test Convention Analysis

**Sibling test files:**
- `tests/api/advisory.rs`
- `tests/api/sbom.rs`
- `tests/api/search.rs`

Examine for: assertion style (`assert_eq!` with `StatusCode`), response body deserialization, error case patterns (404 tests), test naming (`test_<endpoint>_<scenario>`), setup/teardown patterns (database seeding), parameterized test usage (`#[rstest]` if present).

### 4.6 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture
- `CONVENTIONS.md` at repository root -- read for CI check commands and project conventions

### 4.7 CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at repository root. Extract:
- CI check commands (formatting, linting, clippy, compilation)
- Code generation commands (if any)
- Naming rules, directory structure conventions, test patterns

### Expected Discovered Conventions

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- **Endpoint pattern:** Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Model pattern:** Derive `Serialize, Deserialize, Debug, Clone`; use documentation comments
- **Route registration:** `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`
- **Test pattern:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization; 404 tests for invalid IDs

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create SeveritySummary Model

**File:** `modules/fundamental/src/advisory/model/severity_summary.rs` (NEW)

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories by severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
}
```

### 6.2 Register Model Module

**File:** `modules/fundamental/src/advisory/model/mod.rs` (MODIFY)

Add `pub mod severity_summary;` alongside existing module declarations (`pub mod summary;`, `pub mod details;`).

### 6.3 Add Service Method

**File:** `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

Add a `severity_summary` method to `AdvisoryService` following the same pattern as `fetch` and `list`:

```rust
/// Computes advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked
/// to the specified SBOM, deduplicates by advisory ID, and aggregates
/// counts by severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not found)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Fetch AdvisorySummary for each linked advisory
    // 4. Deduplicate by advisory ID (using HashSet or .distinct() in query)
    // 5. Count by severity level using the AdvisorySummary.severity field
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `entity::sbom_advisory` to join SBOM to advisories
- Use `.distinct()` or `HashSet` to deduplicate by advisory ID (acceptance criterion)
- Map the `severity` field from `AdvisorySummary` to count buckets (Critical, High, Medium, Low)
- Default all severity counts to 0 when no advisories exist at that level (via `SeveritySummary::default()`)
- Return 404 via `AppError` with `.context()` when SBOM ID does not exist

### 6.4 Create Endpoint Handler

**File:** `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (NEW)

Following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// GET handler for /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* injected Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Register Route

**File:** `modules/fundamental/src/advisory/endpoints/mod.rs` (MODIFY)

Add the new route following the existing `Router::new().route()` pattern:

```rust
mod severity_summary;

// In the router function:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

### 6.6 Code Quality Checks

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_advisory_summary`) have documentation comments
- Error handling uses `AppError` with `.context()` wrapping
- Follow existing import organization patterns

### 6.7 Documentation Impact

- Check `docs/api.md` for the REST API reference -- add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation
- No changes needed to `server/src/main.rs` (routes auto-mount via module registration per task description)

## Step 7 -- Write Tests

**File:** `tests/api/advisory_summary.rs` (NEW)

Following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with advisories at known severity levels
    // (seed database with SBOM + linked advisories: 2 Critical, 1 High, 0 Medium, 3 Low)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then the response contains correct counts
    // assert_eq!(resp.status(), StatusCode::OK)
    // Deserialize body as SeveritySummary
    // assert_eq!(summary.critical, 2)
    // assert_eq!(summary.high, 1)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 3)
    // assert_eq!(summary.total, 6)
}

/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent_id}/advisory-summary

    // Then a 404 response is returned
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all zeros.
#[tokio::test]
async fn test_advisory_summary_no_advisories_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{sbom_id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links
    // (same advisory linked twice via sbom_advisory)

    // When requesting the advisory summary

    // Then the advisory is counted only once
    // assert_eq!(summary.total, 1) -- not 2
}
```

Each test has:
- Documentation comment explaining what it verifies
- Given/When/Then section comments for structure
- Value-based assertions (not just length checks)
- Follows sibling test naming convention: `test_<endpoint>_<scenario>`

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape** -- verified by `test_advisory_summary_returns_correct_counts`
2. **Returns 404 for non-existent SBOM** -- verified by `test_advisory_summary_nonexistent_sbom_returns_404`
3. **Deduplicates by advisory ID** -- verified by `test_advisory_summary_deduplicates_advisories`
4. **All severity levels default to 0** -- verified by `test_advisory_summary_no_advisories_returns_zeros`
5. **Response time under 200ms for up to 500 advisories** -- verified by query design (single query with GROUP BY rather than N+1); confirmed via test execution timing

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task spec:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` (modified -- in Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (modified -- in Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (modified -- in Files to Modify)
- `modules/fundamental/src/advisory/model/severity_summary.rs` (created -- in Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (created -- in Files to Create)
- `tests/api/advisory_summary.rs` (created -- in Files to Create)

If `docs/api.md` was updated (documentation impact), flag as out-of-scope and ask user for approval.

### Untracked File Check

Run `git status --short`, filter `??` entries by proximity to modified directories. Check for code references to any untracked files (e.g., `include_str!` references). Flag for user review if found.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets are staged.

### Documentation Currency

If `docs/api.md` describes advisory endpoints, verify it includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Update if needed.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param (input) -> call `AdvisoryService.severity_summary()` (processing) -> query `sbom_advisory` join table -> aggregate by severity -> return `Json<SeveritySummary>` (output) -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` -- standalone struct, no trait implementation required
- Sibling parity with `get.rs` endpoint: error handling pattern (`.context()`) present, Path extraction present, Json response present
- Sibling parity with `AdvisoryService.fetch` / `.list`: transaction parameter present, return type uses `Result<T, AppError>`

### Duplication Check

Search for existing severity aggregation logic: `search_for_pattern("severity_summary")`, `search_for_pattern("severity.*count")`. Confirm no duplication with existing code.

### Cross-Section Reference Consistency

- `AdvisoryService` referenced in Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent
- `SeveritySummary` referenced in Files to Create (`model/severity_summary.rs`) -- consistent
- Route registration in Files to Modify (`endpoints/mod.rs`) and Implementation Notes (`endpoints/mod.rs`) -- consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add tests/api/advisory_summary.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add modules/fundamental/src/advisory/model/mod.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated advisory severity counts (critical, high, medium, low, total)
for a given SBOM. Includes SeveritySummary model, AdvisoryService method,
and integration tests covering correct counts, 404 on missing SBOM,
zero-advisory defaults, and deduplication.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR targeting main:

```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity
counts for a given SBOM, enabling dashboard severity breakdowns.

- New `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- `SeveritySummary` response model with per-severity counts
- `AdvisoryService.severity_summary()` method with deduplication by advisory ID
- Integration tests for correct counts, 404, zero-advisory, and deduplication cases

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test plan

- [ ] `cargo test` passes all new and existing tests
- [ ] Manual verification: GET /api/v2/sbom/{valid-id}/advisory-summary returns correct counts
- [ ] Manual verification: GET /api/v2/sbom/{invalid-id}/advisory-summary returns 404
- [ ] Verify response time under 200ms for SBOMs with many advisories"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint, SeveritySummary model, service method, and integration tests
   - No deviations from the plan

   Include the skill footnote with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

3. **Transition** to In Review:

```
jira.transition_issue("TC-9201") -> In Review
```
