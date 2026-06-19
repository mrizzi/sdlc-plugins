# Implementation Plan -- TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, and GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation passes. Proceeding.

## Step 0.5 -- JIRA Access Initialization

JIRA access method established. MCP is the preferred method; REST API fallback via `scripts/jira-client.py` is available if MCP fails.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue using `jira.get_issue("TC-9201")`. Parse the structured description:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify:**
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
- **Files to Create:**
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes:** `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes:** Follow existing endpoint pattern in `get.rs`, use `Path<Id>`, call service, return JSON. Add `severity_summary` method to `AdvisoryService` following `fetch`/`list` pattern. Use `sbom_advisory` join table. Use `AdvisorySummary.severity` field for counting. Register route in `endpoints/mod.rs`. Error handling via `AppError` with `.context()`. Return struct directly via Axum's `Json` extractor.
- **Acceptance Criteria:** 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements:** 4 tests (valid counts, 404, empty SBOM, deduplication)
- **Target PR:** not present (default flow)
- **Bookend Type:** not present (default flow)
- **Dependencies:** None
- **Linked Issues:** is incorporated by TC-9001

Capture the issue's `webUrl` for use in the PR description.

### GitHub Issue Extraction

Check the GitHub Issue custom field (`customfield_10747`) on the fetched issue. If a URL is present, parse `owner`, `repo`, and `number` for the `Closes` line in the PR description. If empty, skip silently.

## Step 1.5 -- Verify Description Integrity

(See outputs/digest-match.md for full details.)

The digest comment is found with marker `[sdlc-workflow] Description digest:`. The stored digest is `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`. The comment's `created` and `updated` timestamps are identical (no edit warning needed). The computed digest matches the stored digest. Proceeding silently.

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No dependency verification needed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue("TC-9201", assignee=<account-id>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code

### 4.1 Inspect Files to Modify

Using Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see AdvisoryService struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the pattern for the new `severity_summary` method (parameters, return type, error handling, transaction usage)

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern
   - Understand how `Router::new().route(...)` registrations are structured

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - `mcp__serena_backend__get_symbols_overview` to see existing module declarations and confirm where to add `pub mod severity_summary;`

### 4.2 Inspect Related Files for Pattern Reference

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference endpoint pattern
   - `mcp__serena_backend__get_symbols_overview` then `find_symbol` on the handler function to see `Path<Id>` extraction, service call, JSON response pattern

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- AdvisorySummary struct with `severity` field
   - `mcp__serena_backend__find_symbol` on `AdvisorySummary` with `include_body=true` to understand the severity field type and structure

6. **`entity/src/sbom_advisory.rs`** -- join table for SBOM-Advisory relationships
   - `mcp__serena_backend__get_symbols_overview` to understand the entity structure and available columns

7. **`common/src/error.rs`** -- AppError pattern
   - `mcp__serena_backend__get_symbols_overview` to confirm error type structure and `.context()` wrapping

### 4.3 Convention Conformance Analysis

**Sibling identification for endpoints:**
- Siblings: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`
- Also check: `modules/fundamental/src/sbom/endpoints/get.rs` for SBOM-scoped endpoint pattern

**Sibling identification for models:**
- Siblings: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`

**Sibling identification for service methods:**
- Siblings: existing methods in `modules/fundamental/src/advisory/service/advisory.rs` (`fetch`, `list`)

Use `mcp__serena_backend__get_symbols_overview` on 2-3 siblings per category to discover:
- Naming conventions (function names, struct names, field names)
- Error handling strategies (Result types, `.context()` usage)
- Parameter patterns (`&self`, `id: Id`, `tx: &Transactional<'_>`)
- Import organization
- Response type conventions

### 4.4 Test Convention Analysis

**Sibling test files:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Use `mcp__serena_backend__get_symbols_overview` on both to discover:
- Assertion style (`assert_eq!` with `StatusCode::OK`, body deserialization)
- Response validation patterns
- Error case coverage (404 tests)
- Test naming conventions (`test_<endpoint>_<scenario>`)
- Test setup and teardown patterns (database seeding, test fixtures)
- Whether parameterized tests (`#[rstest]`) are used

### 4.5 CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (path `./` from Registry). If present, read it for:
- CI check commands (for Step 9)
- Code generation commands
- Additional project-specific conventions

### 4.6 Documentation File Identification

Identify documentation files related to the changes:
- `README.md` at repository root
- `docs/api.md` (API reference, if it exists)
- `docs/architecture.md` (system architecture)

Record these for documentation impact evaluation in Steps 6 and 9.

### 4.7 Backward Compatibility Check

Use `mcp__serena_backend__find_referencing_symbols` on:
- `AdvisoryService` -- to confirm adding a method won't break any consumers
- The `endpoints/mod.rs` router -- to understand how route registration affects downstream

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Target Branch is `main`.

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implement Changes

### 6.1 Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct:

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Provides counts per severity level and a total, enabling dashboard widgets
/// to render severity breakdowns without client-side counting.
#[derive(Debug, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u64,
    /// Count of advisories with High severity.
    pub high: u64,
    /// Count of advisories with Medium severity.
    pub medium: u64,
    /// Count of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

Follow the pattern from sibling models (`summary.rs`, `details.rs`) for derive macros, documentation, and field conventions.

### 6.2 Register the Model Module in `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to the module declarations, following the existing pattern of module registration in the file.

### 6.3 Add `severity_summary` Method to `AdvisoryService`

In `modules/fundamental/src/advisory/service/advisory.rs`, add a new method following the `fetch`/`list` pattern:

```rust
/// Computes aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not found)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, load AdvisorySummary and read severity field
    // 5. Count by severity level (Critical, High, Medium, Low)
    // 6. Return SeveritySummary with counts and total
}
```

Key implementation details:
- Use `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find linked advisories
- Deduplicate by advisory ID to satisfy acceptance criteria
- Use the `severity` field from `AdvisorySummary` for classification
- Return 404 via `AppError` with `.context()` wrapping when SBOM does not exist
- Default all severity counts to 0 when no advisories exist at a level (handled by `SeveritySummary::default()`)

### 6.4 Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Define the GET handler:

```rust
/// Handler for GET /api/v2/sbom/{id}/advisory-summary.
///
/// Returns aggregated advisory severity counts for the specified SBOM.
pub async fn get_advisory_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("fetching advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/get.rs` for:
- `Path<Id>` extraction
- `State` injection
- `Transactional` parameter
- `Result<Json<T>, AppError>` return type
- `.context()` error wrapping

### 6.5 Register the Route in `modules/fundamental/src/advisory/endpoints/mod.rs`

Add the new route registration following the existing `Router::new().route(...)` pattern:

```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))
```

Import the new endpoint module at the top of the file.

### 6.6 Code Quality Verification

Verify:
- All new structs (`SeveritySummary`) have documentation comments
- All new public functions (`severity_summary`, `get_advisory_summary`) have documentation comments
- Documentation comments explain what the symbol does and its purpose

### 6.7 Documentation Impact

- No Documentation Updates section in the task
- Check if `docs/api.md` exists and documents endpoints -- if so, add the new endpoint
- The change adds a new endpoint but does not modify existing behavior, so existing docs remain accurate

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with the following tests, following the patterns discovered from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

### Test 1: Valid SBOM with Known Advisories

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_advisory_summary_valid_sbom() {
    // Given an SBOM with advisories at known severity levels
    // (set up test database with SBOM, linked advisories at Critical, High, Medium, Low)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then the response is 200 OK with correct counts
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.critical, expected_critical_count);
    assert_eq!(summary.high, expected_high_count);
    assert_eq!(summary.medium, expected_medium_count);
    assert_eq!(summary.low, expected_low_count);
    assert_eq!(summary.total, expected_total);
}
```

### Test 2: Non-Existent SBOM Returns 404

```rust
/// Verifies that requesting an advisory summary for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_advisory_summary_not_found() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{nonexistent-id}/advisory-summary")
        .send()
        .await;

    // Then the response is 404 Not Found
    assert_eq!(resp.status(), StatusCode::NOT_FOUND);
}
```

### Test 3: SBOM with No Advisories Returns All Zeros

```rust
/// Verifies that an SBOM with no linked advisories returns all zero counts.
#[tokio::test]
async fn test_advisory_summary_empty() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

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

### Test 4: Duplicate Advisory Links Are Deduplicated

```rust
/// Verifies that duplicate advisory links in the join table are deduplicated in the count.
#[tokio::test]
async fn test_advisory_summary_deduplication() {
    // Given an SBOM with duplicate advisory links (same advisory linked multiple times)

    // When requesting the advisory summary
    let resp = client
        .get("/api/v2/sbom/{id}/advisory-summary")
        .send()
        .await;

    // Then each advisory is counted only once
    assert_eq!(resp.status(), StatusCode::OK);
    let summary: SeveritySummary = resp.json().await;
    assert_eq!(summary.total, expected_unique_count);
    // (not the duplicate count)
}
```

All tests follow the assertion patterns and naming conventions from sibling test files. Each test has a doc comment explaining what it verifies and given-when-then section comments.

Run tests: `cargo test` -- fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct shape | Test 1 validates response fields and values |
| Returns 404 for non-existent SBOM | Test 2 validates 404 status |
| Deduplicates by advisory ID | Test 4 validates unique counting |
| Severity levels default to 0 | Test 3 validates all-zero response; `SeveritySummary::default()` ensures zero defaults |
| Response time under 200ms for 500 advisories | Verify query uses efficient join and grouping; consider adding index on `sbom_advisory.sbom_id` if not present |

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

Flag any out-of-scope files for user approval.

### Untracked File Check

Run `git status --short`, filter `??` entries by proximity to modified directories. Check for code references (e.g., `include_str!`, `mod` declarations) to untracked files. Flag any referenced untracked files for user approval.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- flag any matches.

### Documentation Currency

Verify that API documentation (if it exists at `docs/api.md`) reflects the new endpoint. If it documents existing endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

### Documentation Scope Preservation

If any documentation was modified, verify replacement text covers all original use cases.

### Cross-Section Reference Consistency

Verify file paths are consistent across task description sections:
- `AdvisoryService` referenced in both Files to Modify (`advisory/service/advisory.rs`) and Implementation Notes (`advisory/service/advisory.rs`) -- consistent
- `endpoints/mod.rs` referenced in both Files to Modify and Implementation Notes -- consistent
- `AdvisorySummary` referenced in Implementation Notes at `advisory/model/summary.rs` -- consistent with repo structure

### Duplication Check

Search for existing severity aggregation or counting logic in the codebase that could be reused. Use Grep for patterns like `severity`, `count`, `aggregate`, `summary`.

### CI Checks from CONVENTIONS.md

If CI check commands were extracted from `CONVENTIONS.md` in Step 4, run all of them. Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(id, tx)` -> query `sbom_advisory` join table -> load advisory severities -> count by level -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract and Sibling Parity

- `SeveritySummary` -- standalone struct, no trait/interface to implement. Derives match siblings (`Serialize`, `ToSchema`).
- `get_advisory_summary` handler -- follows same `Result<Json<T>, AppError>` pattern as `get.rs` handler. Parity confirmed.
- `severity_summary` service method -- follows same `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern as `fetch`. Parity confirmed.

## Step 10 -- Commit and Push

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
advisory severity counts (critical, high, medium, low, total) for
a given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

Push and create PR targeting `main`:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

PR description includes:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- `Closes <owner>/<repo>#<number>` if GitHub Issue was extracted
- List of files changed and created

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9201 with the PR URL using ADF inlineCard format
2. **Add comment** to TC-9201 with:
   - PR link
   - Summary of changes (new endpoint, model, service method, tests)
   - Confirmation that implementation follows the task description with no deviations
   - Footnote with sdlc-workflow/implement-task attribution and version from plugin.json
3. **Transition** TC-9201 to "In Review"
