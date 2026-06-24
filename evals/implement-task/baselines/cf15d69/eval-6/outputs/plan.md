# Implementation Plan for TC-9201

**Task:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

---

## Step 0 -- Validate Project Configuration

Project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend mapped to `./` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer

Validation passes. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API v3 if MCP fails.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`.

**Parsed sections:**
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint pattern, use `sbom_advisory` join table, return `AppError` with `.context()`
- **Acceptance Criteria:** 5 items (correct counts, 404 handling, deduplication, defaults to 0, performance)
- **Test Requirements:** 4 test cases
- **Dependencies:** None
- **Bookend Type:** Not present (standard implementation flow)
- **Target PR:** Not present (create new PR)
- **GitHub Issue custom field:** `customfield_10747` -- read from issue fields; if present, parse for PR description `Closes` line

Capture `webUrl` for the Jira link in the PR description.

## Step 1.5 -- Verify Description Integrity

(Detailed in outputs/digest-match.md)

Digest comment found with matching format tag (`sha256-md`) and matching hex digest. Comment was not edited (created == updated). **Proceed silently.**

## Step 2 -- Verify Dependencies

Task has no dependencies (`Depends on: None`). Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition to In Progress: `jira.transition_issue("TC-9201") -> In Progress`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` or `list` method to understand the pattern (signature, transaction handling, return type)

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Identify how routes are structured (`Router::new().route(...)`)

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations

### 4.2 Inspect Reference Files

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- referenced in Implementation Notes as pattern to follow
   - `mcp__serena_backend__find_symbol` on the handler function with `include_body=true`
   - Understand `Path<Id>` extraction, service call, JSON response pattern

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- AdvisorySummary with `severity` field
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` to understand the severity field type

6. **`entity/src/sbom_advisory.rs`** -- join table for SBOM-Advisory relationship
   - `mcp__serena_backend__get_symbols_overview` to understand the entity structure

7. **`common/src/error.rs`** -- AppError enum
   - `mcp__serena_backend__find_symbol` on `AppError` to understand error handling pattern

### 4.3 Check Backward Compatibility

- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers
- Verify that adding a new method does not break existing usage

### 4.4 Convention Conformance Analysis

**Sibling files to examine:**
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- sibling endpoint handlers
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- sibling model structs
- `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling for endpoint patterns

Examine 2-3 siblings via `mcp__serena_backend__get_symbols_overview` to discover:
- **Error handling:** `Result<T, AppError>` with `.context()` wrapping
- **Naming:** Service methods follow `verb_noun` pattern
- **Endpoint structure:** `Path<Id>` extraction, service method call, `Json` response
- **Route registration:** `Router::new().route("/path", get(handler))` pattern
- **Model pattern:** Structs with `#[derive(Serialize, Deserialize)]`, doc comments

### 4.5 Test Convention Analysis

**Sibling test files:**
- `tests/api/advisory.rs` -- advisory endpoint tests
- `tests/api/sbom.rs` -- SBOM endpoint tests

Examine via `mcp__serena_backend__get_symbols_overview`:
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases:** 404 test with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming:** `test_<endpoint>_<scenario>` pattern
- **Setup:** Real PostgreSQL test database, test fixtures

### 4.6 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root. If present, read and extract:
- CI check commands (for Step 9)
- Code generation commands
- Naming rules, directory structure, code patterns

### 4.7 Documentation File Identification

Identify documentation files:
- `README.md` at repo root
- `docs/api.md` -- API documentation (may need updating for new endpoint)
- `docs/architecture.md` -- architecture overview

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file -- SeveritySummary response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns
/// without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module declaration:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` method to `modules/fundamental/src/advisory/service/advisory.rs`

Following the pattern of existing `fetch` and `list` methods in AdvisoryService:

```rust
/// Computes a severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a [`SeveritySummary`] with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not found)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Deduplicate by advisory ID
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find linked advisories
- Join with advisory entity to get severity
- Use `AdvisorySummary.severity` field for classification
- Deduplicate by advisory ID using `DISTINCT` or equivalent
- Default all counts to 0 when no advisories exist
- Return 404 via `AppError` with `.context()` when SBOM ID does not exist

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern in `get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a [`SeveritySummary`] with counts of advisories per severity level
/// (critical, high, medium, low) and a total for the given SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* extract AdvisoryService from state */,
    tx: /* extract Transactional */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following the existing pattern:

```rust
mod severity_summary;

// In the router builder, add:
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Code Quality Practices

- Every new struct (`SeveritySummary`) and function (`severity_summary`, `get_severity_summary`) has documentation comments using `///`
- All public fields have doc comments explaining their meaning
- Error handling uses `Result<T, AppError>` with `.context()` wrapping

### 6.7 Documentation Impact

- Check if `docs/api.md` documents REST endpoints -- if so, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- No architectural changes, so `docs/architecture.md` does not need updating

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Following sibling test conventions (from `tests/api/advisory.rs` and `tests/api/sbom.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_with_known_advisories() {
    // Given an SBOM with advisories at known severity levels
    // (set up test SBOM and link advisories with specific severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response has status 200 and correct counts per severity
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical);
    assert_eq!(summary.high, expected_high);
    assert_eq!(summary.medium, expected_medium);
    assert_eq!(summary.low, expected_low);
    assert_eq!(summary.total, expected_total);
}

/// Verifies that a non-existent SBOM ID returns 404, consistent with other SBOM endpoints.
#[tokio::test]
async fn test_advisory_summary_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{non_existent_id}/advisory-summary

    // Then the response has status 404
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are 0 and total is 0
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, 0);
    assert_eq!(summary.high, 0);
    assert_eq!(summary.medium, 0);
    assert_eq!(summary.low, 0);
    assert_eq!(summary.total, 0);
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary

    // Then the count reflects unique advisories only (not double-counted)
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert total matches unique advisory count, not link count
}
```

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Verified by test_advisory_summary_with_known_advisories |
| Returns 404 when SBOM ID does not exist | Verified by test_advisory_summary_sbom_not_found |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test_advisory_summary_deduplicates_advisories |
| All severity levels default to 0 when no advisories exist | Verified by test_advisory_summary_no_advisories |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified via query design (single SQL query with GROUP BY, indexed join table) |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files match the task description:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Any files outside this list require user approval.

### Untracked File Check

Run `git status --short`, filter `??` entries by proximity to modified directories. Search for code references to any flagged untracked files. Ask user before staging.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

No secrets expected in this implementation.

### Documentation Currency

If `docs/api.md` exists and describes REST endpoints, verify it includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Update if missing.

### Duplication Check

Search for existing severity aggregation or advisory counting logic:
- `mcp__serena_backend__search_for_pattern` for "severity" counting patterns
- Grep for "severity_summary", "severity_count", "advisory_summary" across the repo
- If existing logic found, refactor to reuse it

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted in Step 4. Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract Path<Id> -> call AdvisoryService.severity_summary() -> query sbom_advisory join table -> count by severity -> return Json<SeveritySummary> -- **COMPLETE**

### Contract & Sibling Parity

- SeveritySummary: standalone struct, no trait implementation required
- Endpoint handler follows same pattern as `get.rs` (Path extraction, service call, Json response)
- Error handling matches siblings (AppError with .context())
- No cross-module shared entity mutations (read-only query)

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity summary endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given SBOM.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity summary endpoint" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
advisory severity counts for a given SBOM, returning critical, high, medium, low,
and total counts.

### Changes
- New `SeveritySummary` response struct in advisory model
- New `severity_summary` method on `AdvisoryService`
- New GET endpoint handler at `/api/v2/sbom/{id}/advisory-summary`
- Integration tests covering valid SBOM, missing SBOM (404), empty advisories, and deduplication

Implements [TC-9201](<webUrl>)
"
```

If a GitHub Issue reference was extracted from `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** with PR link, summary of changes, and confirmation of no deviations:

```
jira.add_comment("TC-9201", ...)
```

Comment content:
- PR link
- Summary: Added SeveritySummary model, severity_summary service method, GET endpoint, and 4 integration tests
- Deviations: None
- Followed by the standard skill footer (with version from plugin.json)

3. **Transition to In Review:**

```
jira.transition_issue("TC-9201") -> In Review
```
