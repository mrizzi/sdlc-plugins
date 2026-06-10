# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

- **Jira Issue**: TC-9201
- **Summary**: Add advisory severity aggregation service and endpoint
- **Repository**: trustify-backend
- **Target Branch**: main
- **Parent Feature**: TC-9001 (linked via "is incorporated by")
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (standard flow -- create new branch and PR)

## Step 0 -- Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry**: Present -- contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration**: Present -- Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142
3. **Code Intelligence**: Present -- tool naming convention documented, `serena_backend` instance configured with rust-analyzer

All sections validated. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback decision.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)` and parse the structured description:

| Section | Content |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (advisory service, endpoints mod, model mod) |
| Files to Create | 3 files (severity_summary model, severity_summary endpoint, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Implementation Notes | Follow existing endpoint patterns, use sbom_advisory join table |
| Acceptance Criteria | 5 criteria |
| Test Requirements | 4 test cases |
| Target PR | Not present |
| Bookend Type | Not present |
| Dependencies | None |

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in PR description.

### GitHub Issue extraction

Look up `customfield_10747` (GitHub Issue custom field) from the fetched issue fields. If present, extract the GitHub issue URL and parse `owner/repo#number`. If absent, skip silently.

## Step 1.5 -- Verify Description Integrity

(See `digest-match.md` for the full detailed walkthrough.)

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate comment with marker `[sdlc-workflow] Description digest:`
3. Found: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment edit check: `created` == `updated` -- not edited, no warning
5. Extract format tag: `sha256-md`, hex digest: `a1b2c3d4e5f67890...`
6. Not a legacy format (would be `sha256:<hex>` without `-md` or `-adf` tag) -- proceed
7. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
8. Format tags match (both `sha256-md`) -- compare hex digests
9. **Hex digests match** -- proceed silently to Step 2. No user prompt, no warning, no delay.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress: `jira.transition_issue(TC-9201) -> In Progress`

## Step 4 -- Understand the Code

Use the `serena_backend` Serena instance for code intelligence.

### 4.1 Inspect Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on a method like `fetch` to understand the pattern (parameters, return type, transaction handling)
   - Note the method signature pattern: `&self, id: Id, tx: &Transactional<'_>`

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Identify how routes are registered (`Router::new().route("/path", get(handler))`)

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Read to see existing `pub mod` declarations (e.g., `pub mod summary;`, `pub mod details;`)

### 4.2 Inspect Reference Patterns

1. **`modules/fundamental/src/advisory/endpoints/get.rs`**
   - Read to understand the endpoint handler pattern: Path parameter extraction via `Path<Id>`, calling service method, returning JSON
   - Note error handling pattern (`Result<T, AppError>` with `.context()`)

2. **`modules/fundamental/src/advisory/model/summary.rs`**
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type and structure

3. **`entity/src/sbom_advisory.rs`**
   - Inspect the join table entity to understand how SBOMs and advisories are linked

4. **`common/src/error.rs`**
   - Inspect `AppError` enum and `IntoResponse` implementation for error handling pattern

### 4.3 Inspect Sibling Files for Convention Conformance

1. Examine `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` as sibling endpoint patterns
2. Examine `modules/fundamental/src/sbom/model/summary.rs` as a sibling model pattern
3. Examine `modules/fundamental/src/sbom/service/sbom.rs` as a sibling service pattern

### 4.4 Documentation File Identification

- `README.md` at repository root
- `docs/api.md` (API reference -- may need updating for new endpoint)
- `CONVENTIONS.md` at repository root -- read and follow its conventions

### 4.5 CONVENTIONS.md Lookup

Read `CONVENTIONS.md` at repository root. Extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands (if any)
- Naming conventions, directory structure rules

### 4.6 Convention Conformance Analysis

**Expected discovered conventions (from sibling analysis):**
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Service methods**: Take `&self`, entity ID, and `tx: &Transactional<'_>` as parameters
- **Endpoint handlers**: Use `Path<Id>` extractor, call service method, return `Json<T>`
- **Route registration**: `Router::new().route("/path", get(handler))` in endpoints/mod.rs
- **Model structs**: Derive `Serialize`, `Deserialize`, optionally `Debug`, `Clone`
- **Module registration**: `pub mod <name>;` in parent mod.rs files

### 4.7 Test Convention Analysis

Examine sibling test files in `tests/api/`:
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/advisory.rs` -- Advisory endpoint integration tests

**Expected discovered test conventions:**
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Tests hit a real PostgreSQL test database
- **Organization**: Grouped by endpoint and scenario (success, not found, edge cases)

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

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
/// Provides a breakdown of advisory counts per severity level,
/// enabling dashboard widgets to render severity distributions
/// without client-side counting.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

### 6.2 Register the Model Module

In `modules/fundamental/src/advisory/model/mod.rs`, add:

```rust
pub mod severity_summary;
```

### 6.3 Add `severity_summary` Method to AdvisoryService

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method following the existing `fetch` and `list` pattern:

```rust
/// Computes aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for each severity level and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID
    // Fetch AdvisorySummary for each, read severity field
    // Count by severity level (Critical, High, Medium, Low)
    // Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use the `sbom_advisory` join table in `entity/src/sbom_advisory.rs` to find linked advisories
- Use `AdvisorySummary.severity` field to classify each advisory
- Deduplicate by advisory ID before counting
- Default all severity levels to 0 when no advisories exist
- Wrap errors with `.context()` matching the pattern in `common/src/error.rs`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::service::AdvisoryService;
use common::error::AppError;

/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM, enabling dashboard severity breakdown widgets.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Key implementation details:
- Extract path params via `Path<Id>`
- Call `AdvisoryService::severity_summary`
- Return `Json<SeveritySummary>` directly (Axum handles serialization)
- Return `AppError` with `.context()` wrapping on errors
- Return 404 when SBOM ID does not exist (consistent with existing SBOM endpoints)

### 6.5 Register the Route

In `modules/fundamental/src/advisory/endpoints/mod.rs`, add the new route:

```rust
mod severity_summary;

// In the router builder:
Router::new()
    // ... existing routes ...
    .route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Documentation Impact

- No Documentation Updates section in the task description
- Check if `docs/api.md` needs updating for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- If yes, add the endpoint documentation following existing patterns

### 6.7 Code Quality Practices

- Every new struct (`SeveritySummary`) has documentation comments
- Every new public function (`severity_summary`, `get_severity_summary`) has documentation comments
- Documentation explains what each symbol does and its purpose

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following test cases:

### Test 1: Valid SBOM with known advisories returns correct severity counts

```rust
/// Verifies that an SBOM with known linked advisories returns the correct
/// severity count breakdown.
#[tokio::test]
async fn test_advisory_summary_returns_correct_counts() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM + linked advisories)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, expected_critical)
    // assert_eq!(body.high, expected_high)
    // etc.
}
```

### Test 2: Non-existent SBOM returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM ID
/// returns a 404 Not Found response.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}
```

### Test 3: SBOM with no advisories returns all zeros

```rust
/// Verifies that an SBOM with no linked advisories returns a summary
/// with all severity counts set to zero.
#[tokio::test]
async fn test_advisory_summary_empty_returns_zeros() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}
```

### Test 4: Duplicate advisory links are deduplicated

```rust
/// Verifies that duplicate advisory links in the sbom_advisory join table
/// are deduplicated when computing severity counts.
#[tokio::test]
async fn test_advisory_summary_deduplicates() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary endpoint
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, expected_unique_count)
}
```

All tests follow discovered conventions:
- Use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND` pattern
- Follow `test_<endpoint>_<scenario>` naming
- Hit real PostgreSQL test database
- Each test function has a `///` doc comment explaining what it verifies
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments

Run tests: `cargo test`

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` | Verified by test 1 and endpoint implementation |
| Returns 404 when SBOM ID does not exist | Verified by test 2 |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by test 4 and service implementation |
| All severity levels default to 0 when no advisories exist | Verified by test 3 and `Default` derive on SeveritySummary |
| Response time under 200ms for SBOMs with up to 500 advisories | Verified by efficient SQL query design (single query with GROUP BY) |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are in scope:

**Expected files:**
- `modules/fundamental/src/advisory/service/advisory.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` -- in Files to Modify
- `modules/fundamental/src/advisory/model/severity_summary.rs` -- in Files to Create
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- in Files to Create
- `tests/api/advisory_summary.rs` -- in Files to Create

Any out-of-scope files require user approval.

### Untracked File Check

Run `git status --short` and check for `??` entries in directories where implementation occurred. Flag any untracked files that are referenced by code (e.g., via `include_str!`) for user review.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets are committed.

### Documentation Currency

Check if `docs/api.md` needs updating for the new endpoint. If so, update it.

### Duplication Check

Search for existing severity aggregation or counting logic in the codebase to ensure no duplication.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md. Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param -> call `AdvisoryService::severity_summary` -> query sbom_advisory join table -> count by severity -> return `SeveritySummary` JSON -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` struct: standalone response type, no trait/interface contract to implement
- Sibling parity with `get.rs` endpoint: error handling pattern, path extraction, JSON response -- all aligned
- Service method parity with `fetch`/`list`: same parameter pattern, same error handling

### Cross-Section Reference Consistency

- `AdvisoryService` referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- Route registration referenced in Files to Modify (`advisory/endpoints/mod.rs`) and Implementation Notes -- consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- Add \`SeveritySummary\` response model with counts per severity level
- Add \`severity_summary\` method to \`AdvisoryService\`
- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint
- Add integration tests for success, 404, empty, and deduplication cases

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add Jira comment** with PR link, summary of changes, and any deviations from plan. Include the plugin footer with version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.

3. **Transition to In Review**:

```
jira.transition_issue(TC-9201) -> In Review
```
