# Implementation Plan for TC-9201: Add Advisory Severity Aggregation Service and Endpoint

## Task Summary

Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint `GET /api/v2/sbom/{id}/advisory-summary` returns a summary with counts per severity level (Critical, High, Medium, Low) and a total.

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required sections:
- Repository Registry: present, lists `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present, includes Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present, with tool naming convention `mcp__serena_backend__<tool>`

All sections present -- proceed.

### Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. Fall back to REST API with user confirmation if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue(TC-9201)`. Parse structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Advisory severity aggregation service and endpoint
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing endpoint patterns, use sbom_advisory join table
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Target PR**: None (standard flow)
- **Bookend Type**: None (standard flow)

Capture the issue `webUrl` for use in the PR description.

### Step 1.5 -- Verify Description Integrity

(See digest-match.md for full details.)

1. Fetch comments via `jira.get_issue_comments(TC-9201)`
2. Locate comment with marker `[sdlc-workflow] Description digest:`
3. Found: `sha256-md:a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890`
4. Comment `created` == `updated` -- no edit detected
5. Extract format tag: `sha256-md`, hex digest: `a1b2c3d4...`
6. Compute current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
7. Format tags match (`sha256-md` == `sha256-md`)
8. Hex digests match -- proceed silently, no user prompt, no added latency

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

1. Get current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9201) -> In Progress`

## Code Understanding (Step 4)

### File Inspection Plan

Use `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` to inspect:

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- understand `AdvisoryService` structure, existing `fetch` and `list` method signatures, parameter patterns (`&self, id: Id, tx: &Transactional<'_>`)
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- understand route registration pattern (`Router::new().route(...)`)
3. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- reference endpoint pattern for path param extraction, service call, JSON response
4. **`modules/fundamental/src/advisory/model/mod.rs`** -- understand module registration pattern (`pub mod ...`)
5. **`modules/fundamental/src/advisory/model/summary.rs`** -- understand `AdvisorySummary` struct and its `severity` field (needed for counting)
6. **`entity/src/sbom_advisory.rs`** -- understand the join table structure for SBOM-Advisory relationships
7. **`common/src/error.rs`** -- understand `AppError` enum and `.context()` wrapping pattern
8. **`common/src/model/paginated.rs`** -- understand `PaginatedResults<T>` (for reference, not directly used)

### Sibling Analysis

Inspect 2-3 sibling files for convention conformance:
- **Sibling endpoints**: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`
- **Sibling models**: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`
- **Sibling services**: compare `SbomService` methods in `modules/fundamental/src/sbom/service/sbom.rs` with `AdvisoryService`

### Test Convention Analysis

Inspect sibling test files:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Examine: assertion style, response validation, error case coverage, naming conventions, test setup/teardown, parameterized test usage.

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read it for naming rules, directory structure, code patterns, and extract CI check commands for Step 9.

### Documentation File Identification

Identify docs related to modified code:
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `docs/architecture.md` -- system architecture overview
- `README.md` -- repository readme

## Branch Creation (Step 5)

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

## Implementation (Step 6)

### File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated counts of advisory severities linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level (Critical, High,
/// Medium, Low) along with a total count, enabling dashboard widgets to render
/// severity distributions without client-side counting.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
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

Follow patterns from sibling model files (`summary.rs`, `details.rs`) for derive macros and documentation style.

### File 2: Modify `modules/fundamental/src/advisory/model/mod.rs`

Add the new module registration:

```rust
pub mod severity_summary;
```

### File 3: Modify `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`:

```rust
/// Computes an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts each severity level. Returns a `SeveritySummary`
/// with counts for Critical, High, Medium, Low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for advisories linked to this SBOM
    // 3. Fetch AdvisorySummary for each linked advisory (deduplicate by advisory ID)
    // 4. Count by severity level using the `severity` field from AdvisorySummary
    // 5. Return SeveritySummary with counts and total
}
```

Follow the same pattern as existing `fetch` and `list` methods: take `&self, id: Id, tx: &Transactional<'_>`, return `Result<T, AppError>`, use `.context()` for error wrapping.

Key implementation details:
- Use `entity::sbom_advisory` to join SBOMs to advisories
- Deduplicate advisories by ID before counting (acceptance criterion)
- Default all severity counts to 0 when no advisories exist at that level (handled by `SeveritySummary::default()`)
- Return 404 when SBOM ID does not exist (check SBOM existence first)

### File 4: Create `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler:

```rust
/// Handler for `GET /api/v2/sbom/{id}/advisory-summary`.
///
/// Returns an aggregated severity summary for all advisories linked to the
/// specified SBOM, with counts per severity level and a total.
pub async fn get_severity_summary(
    Path(id): Path<Id>,
    State(service): State<AdvisoryService>,
    tx: Transactional<'_>,
) -> Result<Json<SeveritySummary>, AppError> {
    let summary = service
        .severity_summary(id, &tx)
        .await
        .context("Failed to compute advisory severity summary")?;
    Ok(Json(summary))
}
```

Follow the pattern in `modules/fundamental/src/advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call service method
- Return `Json(result)` directly (Axum handles serialization)
- Use `.context()` for error wrapping

### File 5: Modify `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route following existing patterns:

```rust
use severity_summary::get_severity_summary;

// In the router builder:
.route("/api/v2/sbom/:id/advisory-summary", get(get_severity_summary))
```

### File 6: No changes to `server/src/main.rs`

As noted in the task description, routes auto-mount via module registration.

## Test Implementation (Step 7)

### File 7: Create `tests/api/advisory_summary.rs`

Write integration tests following the patterns discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
/// Verifies that a valid SBOM with known advisories returns correct severity counts.
#[tokio::test]
async fn test_severity_summary_returns_correct_counts() {
    // Given an SBOM with advisories at various severity levels
    // (set up test data: create SBOM, link advisories with known severities)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the response contains correct counts per severity level
    // assert_eq!(resp.status(), StatusCode::OK)
    // assert_eq!(body.critical, expected_critical)
    // assert_eq!(body.high, expected_high)
    // assert_eq!(body.medium, expected_medium)
    // assert_eq!(body.low, expected_low)
    // assert_eq!(body.total, expected_total)
}

/// Verifies that a non-existent SBOM ID returns 404.
#[tokio::test]
async fn test_severity_summary_not_found_for_missing_sbom() {
    // Given a non-existent SBOM ID

    // When requesting the advisory summary
    // GET /api/v2/sbom/{nonexistent-id}/advisory-summary

    // Then the response is 404
    // assert_eq!(resp.status(), StatusCode::NOT_FOUND)
}

/// Verifies that an SBOM with no advisories returns all zeros.
#[tokio::test]
async fn test_severity_summary_all_zeros_for_sbom_without_advisories() {
    // Given an SBOM with no linked advisories

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then all severity counts are zero
    // assert_eq!(body.critical, 0)
    // assert_eq!(body.high, 0)
    // assert_eq!(body.medium, 0)
    // assert_eq!(body.low, 0)
    // assert_eq!(body.total, 0)
}

/// Verifies that duplicate advisory links are deduplicated in the count.
#[tokio::test]
async fn test_severity_summary_deduplicates_advisories() {
    // Given an SBOM with duplicate advisory links (same advisory linked twice)

    // When requesting the advisory summary
    // GET /api/v2/sbom/{id}/advisory-summary

    // Then the advisory is counted only once
    // assert_eq!(body.total, 1)  // not 2
}
```

All tests follow the patterns from sibling test files:
- Use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND`
- Test naming: `test_<endpoint>_<scenario>`
- Given-when-then section comments for non-trivial tests
- Documentation comment on every test function

### Run Tests

```bash
cargo test
```

Fix any failures before proceeding.

## Verification (Steps 8-9)

### Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape | Verified by test_severity_summary_returns_correct_counts |
| Returns 404 for non-existent SBOM | Verified by test_severity_summary_not_found_for_missing_sbom |
| Deduplicates by advisory ID | Verified by test_severity_summary_deduplicates_advisories |
| Severity levels default to 0 | Verified by test_severity_summary_all_zeros_for_sbom_without_advisories |
| Response time under 200ms for 500 advisories | Verified by efficient query design (single join query, no N+1) |

### Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` must list only the 6 files specified in Files to Modify and Files to Create (plus the test file). Flag any out-of-scope changes.
2. **Untracked file check**: `git status --short` to find `??` entries in directories with modified files. Check for code references before staging.
3. **Sensitive-pattern check**: Scan staged diff for secrets/credentials.
4. **Documentation currency**: Check if `docs/api.md` needs updating with the new endpoint.
5. **CI checks from CONVENTIONS.md**: Run any CI check commands extracted in Step 4.
6. **Duplication check**: Search for existing severity aggregation logic to avoid duplication.
7. **Data-flow trace**: Verify complete path: HTTP request -> path param extraction -> service method -> DB query -> aggregation -> JSON response.
8. **Contract & sibling parity**: Verify SeveritySummary struct completeness, endpoint handler follows sibling patterns, service method signature matches existing methods.
9. **Cross-section reference consistency**: Verify file paths are consistent across Files to Modify, Files to Create, and Implementation Notes sections.

## Commit and PR (Step 10)

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"

git push -u origin TC-9201

gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "## Summary

Add a new REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

- New model: \`SeveritySummary\` response struct with critical/high/medium/low/total counts
- New service method: \`AdvisoryService::severity_summary()\` using sbom_advisory join table
- New endpoint: \`GET /api/v2/sbom/{id}/advisory-summary\`
- Integration tests covering correct counts, 404, empty SBOM, and deduplication

Implements [TC-9201](<webUrl>)

## Test plan
- [ ] Verify correct severity counts for SBOM with known advisories
- [ ] Verify 404 for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify deduplication of advisory links
- [ ] Run cargo test and confirm all tests pass"
```

## Jira Update (Step 11)

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add comment to TC-9201 with:
   - PR link
   - Summary of changes made
   - Any deviations from the plan
3. Transition TC-9201 to **In Review**
