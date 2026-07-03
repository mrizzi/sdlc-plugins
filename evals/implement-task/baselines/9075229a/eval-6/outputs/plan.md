# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (linked via "is incorporated by")

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured

All sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API fallback as documented in the skill.

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`. Parse the structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add severity aggregation service method and REST endpoint for SBOM advisory summaries |
| Files to Modify | 3 files (advisory service, endpoints/mod.rs, model/mod.rs) |
| Files to Create | 3 files (severity_summary model, severity_summary endpoint, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` (NEW) |
| Bookend Type | Not present (standard implementation flow) |
| Target PR | Not present (new branch/PR flow) |
| Dependencies | None |

Capture the issue's `webUrl` for the PR description link.

Extract the GitHub Issue custom field (`customfield_10747`) value if present.

## Step 1.5 -- Verify Description Integrity

See `outputs/digest-match.md` for the full analysis. The digest comment is found, uses format-tagged format (`sha256-md`), the comment has not been edited (created == updated), and the computed digest matches the stored digest. Proceed silently.

## Step 2 -- Verify Dependencies

The task description states "Depends on: None". No dependency checks needed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user account ID: `jira.user_info()`
2. Assign TC-9201 to current user: `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. Transition to In Progress: `jira.transition_issue(TC-9201, "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

Use `mcp__serena_backend__get_symbols_overview` on:

- `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService structure, existing methods (`fetch`, `list`, `search`), method signatures and patterns
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
- `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern

### 4.2 Inspect reference files (Implementation Notes)

Use `mcp__serena_backend__find_symbol` with `include_body=true` on:

- `modules/fundamental/src/advisory/endpoints/get.rs` -- understand endpoint handler pattern (Path extraction, service call, JSON response)
- `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct, locate the `severity` field
- `entity/src/sbom_advisory.rs` -- understand the SBOM-Advisory join table schema
- `common/src/error.rs` -- understand AppError and `.context()` wrapping pattern

### 4.3 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on AdvisoryService to identify all callers and ensure the new method doesn't conflict.

### 4.4 Convention conformance analysis (sibling inspection)

Inspect 2-3 sibling files for patterns:

**Endpoint siblings** (in `modules/fundamental/src/advisory/endpoints/`):
- `get.rs` -- handler function signature, Path extraction, service invocation, error handling
- `list.rs` -- if present, pagination pattern

**Model siblings** (in `modules/fundamental/src/advisory/model/`):
- `summary.rs` -- struct definition pattern, derives, serde attributes
- `details.rs` -- struct definition pattern

**Service siblings** (in `modules/fundamental/src/advisory/service/`):
- `advisory.rs` -- method patterns (parameter types, return types, transaction usage)

**Cross-module siblings** (in `modules/fundamental/src/sbom/`):
- `endpoints/get.rs` -- compare SBOM endpoint pattern since the new endpoint is under SBOM path
- `service/sbom.rs` -- SbomService patterns for reference

Expected discovered conventions:
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping
- **Endpoint pattern**: Extract path params via `Path<Id>`, call service method, return `Json(result)`
- **Service pattern**: Methods take `&self, id: Id, tx: &Transactional<'_>`, return `Result<T, AppError>`
- **Model pattern**: Structs derive `Serialize, Deserialize, Debug, Clone` with serde attributes
- **Route registration**: `Router::new().route("/path", get(handler))` in `endpoints/mod.rs`

### 4.5 Test convention analysis

Inspect test siblings in `tests/api/`:
- `advisory.rs` -- assertion patterns, response validation, error case coverage
- `sbom.rs` -- SBOM-related test patterns, setup/teardown

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Error cases**: 404 tests with `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`
- **Test naming**: `test_<endpoint>_<scenario>` pattern
- **Setup**: Real PostgreSQL test database with fixture data

### 4.6 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the trustify-backend repository root. If present, read it and extract CI check commands for use in Step 9.

### 4.7 Documentation file identification

Look for:
- `docs/api.md` -- REST API reference (will need updating with new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` at repository root

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

New file defining the SeveritySummary response struct:

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for an SBOM.
///
/// Provides counts per severity level (Critical, High, Medium, Low) and a total,
/// enabling dashboard widgets to render severity breakdowns without client-side counting.
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

Follow model struct patterns from `summary.rs` and `details.rs` siblings (derive macros, serde attributes, documentation comments).

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add module registration:

```rust
pub mod severity_summary;
```

Following the pattern of existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to AdvisoryService following the pattern of `fetch` and `list`:

```rust
/// Computes a severity summary by aggregating advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories linked to the specified SBOM,
/// deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for advisories linked to sbom_id
    // 2. Join with advisory table to get severity field
    // 3. Deduplicate by advisory ID
    // 4. Count by severity level (Critical, High, Medium, Low)
    // 5. Return SeveritySummary with counts and total
}
```

Implementation details:
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find linked advisories
- Use `AdvisorySummary.severity` field to classify each advisory
- Deduplicate by advisory ID (use `HashSet` or SQL `DISTINCT`)
- Default all severity counts to 0 when no advisories exist
- Wrap errors with `.context("Failed to compute severity summary for SBOM")`

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New endpoint handler following the pattern from `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handles GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns a severity summary with counts of advisories per severity level
/// for the specified SBOM.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transaction */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact pattern from the existing `get.rs` handler for parameter extraction, service invocation, and error handling.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))
```

### 6.6 Verify no changes needed in `server/src/main.rs`

The task description confirms no changes are needed (routes auto-mount via module registration). Verify this is accurate by checking the server setup.

### 6.7 Code quality verification

- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_severity_summary`) have documentation comments
- Follow naming conventions from siblings

### 6.8 Documentation impact

- Check if `docs/api.md` needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- Update API documentation if it exists and covers endpoint listings

## Step 7 -- Write Tests

### Create `tests/api/advisory_summary.rs`

Integration tests following the patterns discovered from `tests/api/advisory.rs` and `tests/api/sbom.rs`:

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (seed test database with SBOM + linked advisories)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response status is 200 OK and counts match expected values
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(summary.critical, expected_critical)
    // assert_eq!(summary.high, expected_high)
    // etc.
}

/// Verifies that a non-existent SBOM ID returns 404 Not Found.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary

    // Then the response status is 404 NOT_FOUND
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_no_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary

    // Then all severity counts are 0 and total is 0
    // assert_eq!(summary.critical, 0)
    // assert_eq!(summary.high, 0)
    // assert_eq!(summary.medium, 0)
    // assert_eq!(summary.low, 0)
    // assert_eq!(summary.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the severity count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate links to the same advisory

    // When requesting the advisory summary

    // Then each advisory is counted only once
    // (total should reflect unique advisories, not link count)
}
```

Each test function has:
- A `///` documentation comment explaining what it verifies
- Given/When/Then section comments for non-trivial tests
- Value-based assertions (not just length checks)
- Pattern matching the sibling test conventions

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by `test_advisory_summary_valid_sbom` |
| Returns 404 for non-existent SBOM ID | Verified by `test_advisory_summary_nonexistent_sbom` |
| Counts only unique advisories (deduplicates by advisory ID) | Verified by `test_advisory_summary_deduplication` |
| All severity levels default to 0 when no advisories exist | Verified by `test_advisory_summary_no_advisories` |
| Response time under 200ms for up to 500 advisories | Verified by efficient query design (SQL aggregation, not in-memory); would require load testing for full verification |

## Step 9 -- Self-Verification

### 9.1 Scope containment

Run `git diff --name-only` and compare against:

**Files to Modify** (expected):
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Files to Create** (expected):
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### 9.2 Untracked file check

Run `git status --short`, filter `??` entries by proximity to modified directories. Search for code references to any untracked files (e.g., `include_str!`, imports).

### 9.3 Sensitive-pattern check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### 9.4 Documentation currency

Check if `docs/api.md` accurately reflects the new endpoint. Update if needed.

### 9.5 CI checks from CONVENTIONS.md

Run all CI check commands extracted from CONVENTIONS.md (if found). Hard stop on any failure.

### 9.6 Data-flow trace

Trace the complete data flow:

```
GET /api/v2/sbom/{id}/advisory-summary
  -> severity_summary endpoint handler (parse Path<Id>)
  -> AdvisoryService.severity_summary(id, tx)
  -> Query sbom_advisory join table (filter by sbom_id)
  -> Join advisory table (get severity field)
  -> Deduplicate by advisory ID
  -> Count by severity level
  -> Return SeveritySummary struct
  -> Serialize to JSON response
```

All stages connected: input (HTTP request) -> processing (service query + aggregation) -> output (JSON response). **COMPLETE**.

### 9.7 Contract & sibling parity

- **SeveritySummary**: standalone response struct, no trait implementation needed
- **Endpoint handler**: follows same `Result<Json<T>, AppError>` pattern as siblings
- **Service method**: follows same `&self, id, tx -> Result<T, AppError>` pattern as siblings
- **Error handling**: uses `.context()` wrapping like all siblings

### 9.8 Duplication check

Search for existing severity aggregation logic in the repository to ensure no duplication.

### 9.9 Cross-section reference consistency

Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes:
- AdvisoryService referenced in both Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent
- Route registration referenced in both Files to Modify (`endpoints/mod.rs`) and Implementation Notes (`endpoints/mod.rs`) -- consistent

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs
git add modules/fundamental/src/advisory/model/mod.rs
git add modules/fundamental/src/advisory/service/advisory.rs
git add modules/fundamental/src/advisory/endpoints/severity_summary.rs
git add modules/fundamental/src/advisory/endpoints/mod.rs
git add tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint GET /api/v2/sbom/{id}/advisory-summary that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New SeveritySummary response struct in advisory model
- New severity_summary method on AdvisoryService
- New GET endpoint handler at /api/v2/sbom/{id}/advisory-summary
- Integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](<webUrl>)
"
```

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes (new endpoint, model, service method, tests)
   - Any deviations from the plan (none expected)
   - Comment footnote with plugin version and link
3. **Transition** TC-9201 to **In Review**
