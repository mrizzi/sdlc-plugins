# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

## Step 0 - Validate Project Configuration

Verify the project's CLAUDE.md contains the required sections:

1. **Repository Registry** - Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** - Present. Project key: TC, Cloud ID configured, Feature issue type ID: 10142.
3. **Code Intelligence** - Present. Tool naming convention documented, `serena_backend` instance configured with rust-analyzer.

All required sections are present. Proceed.

## Step 0.5 - JIRA Access Initialization

Attempt MCP for all Jira operations. If MCP fails, prompt the user for REST API fallback.

## Step 1 - Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")` and parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` - add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` - register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` - add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` - SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` - GET handler
  - `tests/api/advisory_summary.rs` - integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` - NEW
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add service method following `fetch`/`list` pattern, use `sbom_advisory` join table, count by severity level using `AdvisorySummary.severity` field, register route in endpoints `mod.rs`, use `AppError` with `.context()` for errors, return struct directly via Axum `Json`.
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 test cases
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Dependencies**: None

Capture `webUrl` for use in PR description (e.g., `https://redhat.atlassian.net/browse/TC-9201`).

**GitHub Issue extraction**: Check `customfield_10747` on the issue. If present, parse `owner/repo#number` for use in PR description's `Closes` line.

## Step 1.5 - Verify Description Integrity

See `digest-match.md` for full details. The digest comment is found, timestamps match (no edit), format tags match (`sha256-md`), and hex digests match. **Proceed silently** -- no user prompt needed.

## Step 2 - Verify Dependencies

The task lists "Dependencies: None". No dependency checks are required. Proceed.

## Step 3 - Transition to In Progress and Assign

1. Retrieve current user's account ID via `jira.user_info()`.
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`.
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`.

## Step 4 - Understand the Code

### 4.1 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir` or Read/Glob. If present, read it and extract CI check commands (formatting, linting, compilation) for use in Step 9. Also extract any code generation commands.

### 4.2 Inspect Files to Modify

Use the `serena_backend` Serena instance:

**`modules/fundamental/src/advisory/service/advisory.rs`** (AdvisoryService):
- `mcp__serena_backend__get_symbols_overview` to see the struct and all methods.
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand the pattern for `severity_summary`.
- Note parameter patterns: `&self`, ID parameter, `tx: &Transactional<'_>`.
- Note return type pattern: `Result<T, AppError>`.

**`modules/fundamental/src/advisory/endpoints/mod.rs`** (route registration):
- `mcp__serena_backend__get_symbols_overview` to see how existing routes are registered.
- Identify the `Router::new().route(...)` pattern for adding the new endpoint.

**`modules/fundamental/src/advisory/model/mod.rs`** (module registration):
- Read to see existing `pub mod` declarations.

**`modules/fundamental/src/advisory/endpoints/get.rs`** (reference endpoint):
- `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function to understand the endpoint pattern: path param extraction via `Path<Id>`, service call, JSON response.

### 4.3 Inspect Reference Types

**`modules/fundamental/src/advisory/model/summary.rs`** (AdvisorySummary):
- `mcp__serena_backend__get_symbols_overview` to see the `severity` field type and struct shape.

**`entity/src/sbom_advisory.rs`** (join table):
- `mcp__serena_backend__get_symbols_overview` to understand the SBOM-Advisory join table schema.

**`common/src/error.rs`** (AppError):
- `mcp__serena_backend__get_symbols_overview` to confirm error type pattern and `.context()` usage.

### 4.4 Convention Conformance Analysis

Identify siblings for each file being modified or created:

- **Service methods**: sibling methods `fetch` and `list` in `advisory.rs` -- examine parameter types, return types, error wrapping pattern.
- **Endpoint handlers**: sibling handlers in `endpoints/get.rs` and `endpoints/list.rs` -- examine path extraction, service invocation, response serialization.
- **Model structs**: sibling structs in `model/summary.rs` and `model/details.rs` -- examine derive macros, field documentation, serialization attributes.

Expected discovered conventions:
- **Error handling**: All handlers use `Result<T, AppError>` with `.context()` wrapping.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`).
- **Route registration**: `Router::new().route("/path", get(handler))` pattern.
- **Response types**: Structs derive `Serialize` and use Axum's `Json` extractor.
- **Path parameters**: Extracted via `Path<Id>` or `Path<(Id,)>`.

### 4.5 Test Convention Analysis

Inspect sibling test files:

- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- examine test structure, assertion patterns, setup/teardown.

Expected discovered test conventions:
- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization.
- **Error cases**: 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.
- **Test naming**: `test_<endpoint>_<scenario>` pattern.
- **Setup**: Uses test database with fixture data.

### 4.6 Check Backward Compatibility

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService`) to identify all callers and ensure the new method addition does not break existing callers. Adding a new method to a struct is non-breaking.

### 4.7 Documentation File Identification

Identify documentation files:
- `README.md` at repository root
- `docs/api.md` (API reference)
- `CONVENTIONS.md` (if present)

Record these for documentation impact evaluation in Step 6 and currency check in Step 9.

## Step 5 - Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 - Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::Serialize;

/// Summary of advisory severity counts for an SBOM.
///
/// Aggregates the number of linked advisories at each severity level,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Debug, Clone, Serialize, Default)]
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

Follow the derive macro pattern from sibling model structs (`summary.rs`, `details.rs`). All fields default to 0 via `Default` derive, satisfying the acceptance criterion for zero defaults.

### 6.2 Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

Place it alongside existing `pub mod summary;` and `pub mod details;` declarations.

### 6.3 Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`, following the `fetch`/`list` pattern:

```rust
/// Computes an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Returns counts of advisories at each severity level (Critical, High, Medium, Low)
/// and a total count. Deduplicates advisories by ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Join with advisory table to get severity field
    // 4. Deduplicate by advisory ID
    // 5. Count by severity level
    // 6. Build and return SeveritySummary
}
```

Implementation details:
- Use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM.
- Join with the advisory entity to access the severity field referenced in `AdvisorySummary`.
- Use `HashSet` or SQL `DISTINCT` to deduplicate by advisory ID.
- Map severity values to the four levels (Critical, High, Medium, Low) and count.
- Wrap errors with `.context("Failed to compute severity summary")` following `AppError` pattern.

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern in `endpoints/get.rs`:

```rust
use axum::extract::Path;
use axum::Json;

/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns an aggregated severity summary for all advisories linked to the
/// specified SBOM, with counts per severity level and a total.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    service: /* injected AdvisoryService */,
    tx: /* transactional context */,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to get advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact parameter extraction and response pattern from `get.rs`.

### 6.5 Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route alongside existing route registrations:

```rust
use severity_summary::get_severity_summary;

// Add to Router::new() chain:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

Note: `server/src/main.rs` does not need changes -- routes auto-mount via module registration as stated in the task.

### 6.6 Documentation Impact

After implementing code changes:
- No Documentation Updates section exists in the task.
- Check `docs/api.md` -- if it documents API endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with its request/response schema.
- Keep updates lightweight and scoped.

### 6.7 Code Quality Practices

Verify that every new struct, public function, and endpoint handler has a documentation comment using Rust's `///` convention. This has been included in the code sketches above.

## Step 7 - Write Tests

### Create `tests/api/advisory_summary.rs`

Follow the test conventions discovered in Step 4 (assertion style, naming, setup patterns from sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`).

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with known advisories at various severity levels
    // (set up test database with fixture data)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the response is 200 OK with correct severity counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, /* expected count */);
    assert_eq!(summary.high, /* expected count */);
    assert_eq!(summary.medium, /* expected count */);
    assert_eq!(summary.low, /* expected count */);
    assert_eq!(summary.total, /* expected total */);
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_advisory_summary_nonexistent_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{nonexistent-id}/advisory-summary").await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}

/// Verifies that an SBOM with no advisories returns all zeros.
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
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client.get("/api/v2/sbom/{id}/advisory-summary").await;

    // Then the count reflects unique advisories only
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    // Assert counts match expected unique advisory counts, not duplicated counts
    assert_eq!(summary.total, /* expected unique count, not duplicate count */);
}
```

Each test function has a `///` documentation comment. Non-trivial tests include given-when-then section comments. Assertions check specific field values, not just response status or collection length.

Run tests:

```bash
cargo test
```

Fix any failures before proceeding.

## Step 8 - Verify Acceptance Criteria

1. **GET /api/v2/sbom/{id}/advisory-summary returns correct shape** - Verified by `test_advisory_summary_valid_sbom` test asserting all five fields (critical, high, medium, low, total).
2. **Returns 404 for non-existent SBOM ID** - Verified by `test_advisory_summary_nonexistent_sbom` test.
3. **Counts only unique advisories** - Verified by `test_advisory_summary_deduplication` test using fixture data with duplicate links.
4. **All severity levels default to 0** - Verified by `test_advisory_summary_no_advisories` test asserting all fields are 0. Also guaranteed by `Default` derive on `SeveritySummary`.
5. **Response time under 200ms for up to 500 advisories** - Verify by inspecting the query plan (ensure index usage on `sbom_advisory` join table). Consider adding a performance note if the query requires optimization.

## Step 9 - Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are in scope:

Expected files:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (Files to Create)
- `tests/api/advisory_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/service/advisory.rs` (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (Files to Modify)
- `modules/fundamental/src/advisory/model/mod.rs` (Files to Modify)

Any files outside this list require user approval.

### Untracked File Check

Run `git status --short` to find untracked files (`??` entries). Filter by proximity to directories with modified files. Search for code references (e.g., `include_str!`, `use`, `mod`). Flag any referenced untracked files for user review.

### Sensitive-Pattern Check

Run:

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

Check whether `docs/api.md` needs updating to reflect the new endpoint. If the file documents existing endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### Documentation Scope Preservation

If any documentation was modified, verify that replaced text still covers all original use cases.

### Cross-Section Reference Consistency

Verify file paths are consistent across the task description sections:
- `AdvisoryService` referenced in Files to Modify (`service/advisory.rs`) and Implementation Notes (`service/advisory.rs`) -- consistent.
- `AdvisorySummary` referenced in Implementation Notes (`model/summary.rs`) -- this is a reference file, not the new file -- consistent.
- `SeveritySummary` referenced in Files to Create (`model/severity_summary.rs`) -- consistent.

### Duplication Check

Search for existing severity aggregation logic in the codebase. Use Grep/Serena to look for functions with "severity", "summary", "aggregate", or "count" in their names to ensure no duplication.

### CI Checks from CONVENTIONS.md

If CI commands were extracted from `CONVENTIONS.md` in Step 4, run all of them. Hard stop on any failure.

Fallback: run `cargo build` and `cargo clippy` to check for compilation errors and lint warnings.

### Data-Flow Trace

Trace the complete data flow:

- **Input**: `GET /api/v2/sbom/{id}/advisory-summary` request with SBOM ID path parameter
- **Processing**: Handler extracts path param -> calls `AdvisoryService.severity_summary()` -> queries `sbom_advisory` join table -> joins with advisory entity -> deduplicates by advisory ID -> counts by severity level -> builds `SeveritySummary`
- **Output**: JSON response with `{ critical, high, medium, low, total }` -- **COMPLETE**

### Contract & Sibling Parity

- **Contract verification**: `SeveritySummary` is a standalone struct (no trait implementation required). Handler returns `Result<Json<SeveritySummary>, AppError>` matching the Axum handler contract.
- **Sibling parity**: Compare with `get.rs` endpoint -- path extraction, service call, error wrapping, JSON response all follow the same pattern. No gaps.
- **Cross-module shared entity**: The `sbom_advisory` join table is used read-only (no inserts/updates/deletes), so cross-module write pattern analysis is not applicable.

## Step 10 - Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated severity counts (critical, high, medium, low, total)
for advisories linked to a given SBOM. Includes deduplication by
advisory ID and 404 handling for non-existent SBOMs.

Implements TC-9201"

git push -u origin TC-9201
```

Create PR:

```bash
gh pr create --base main \
  --title "feat(api): add advisory severity aggregation endpoint" \
  --body "## Summary

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM.

- New endpoint: GET /api/v2/sbom/{id}/advisory-summary
- Returns { critical, high, medium, low, total } counts
- Deduplicates advisories by ID before counting
- Returns 404 for non-existent SBOM IDs
- All severity levels default to 0 when no advisories exist

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [x] Valid SBOM with known advisories returns correct severity counts
- [x] Non-existent SBOM ID returns 404
- [x] SBOM with no advisories returns all zeros
- [x] Duplicate advisory links are deduplicated in the count"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 - Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:

```
jira.update_issue("TC-9201", fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes: added `SeveritySummary` model, `severity_summary` service method, GET endpoint at `/api/v2/sbom/{id}/advisory-summary`, and integration tests
   - No deviations from the plan
   - Comment ends with the standard footnote (horizontal rule + "This comment was AI-generated by sdlc-workflow/implement-task v{version}." with link)

3. **Transition** TC-9201 to "In Review".
