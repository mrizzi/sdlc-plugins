# Implementation Plan for TC-9201

## Summary

Add an advisory severity aggregation service method and REST endpoint that returns
severity counts (Critical, High, Medium, Low, Total) for a given SBOM. This enables
dashboard widgets to render severity breakdowns without client-side counting.

## Task Validation

- **Repository:** trustify-backend
- **Dependencies:** None
- **Target PR:** None (default flow -- new branch and PR)
- **Jira Issue:** TC-9201

## Cross-Section Reference Consistency Check

- Entity `AdvisoryService` -- Files to Modify says `modules/fundamental/src/advisory/service/advisory.rs`, Implementation Notes also references `modules/fundamental/src/advisory/service/advisory.rs` -- **CONSISTENT**
- Entity `AdvisorySummary` -- Implementation Notes references `modules/fundamental/src/advisory/model/summary.rs` -- consistent with repo structure
- Entity `sbom_advisory` join table -- Implementation Notes references `entity/src/sbom_advisory.rs` -- consistent with repo structure
- Entity `endpoints/mod.rs` -- Files to Modify says `modules/fundamental/src/advisory/endpoints/mod.rs`, Implementation Notes also references this path -- **CONSISTENT**

## Branch

```
git checkout -b TC-9201
```

## Files to Modify (3)

| # | File | Change Description |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |

## Files to Create (3)

| # | File | Description |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
- Response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- Returns 404 when SBOM ID does not exist
- All severity levels default to 0 when no advisories exist at that level

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary`
  - Input: HTTP request with SBOM ID path param --> `Path<Id>` extraction in handler -- **CONNECTED**
  - Processing: Handler calls `AdvisoryService::severity_summary(sbom_id, tx)` -- **CONNECTED**
  - Service queries `sbom_advisory` join table for the given SBOM ID -- **CONNECTED**
  - Service loads linked `AdvisorySummary` records and reads `severity` field -- **CONNECTED**
  - Service deduplicates by advisory ID and counts per severity level -- **CONNECTED**
  - Output: Returns `Json<SeveritySummary>` with counts -- **CONNECTED**
  - Status: **COMPLETE**

## Acceptance Criteria Verification Plan

| # | Criterion | Verification Method |
|---|---|---|
| 1 | GET returns `{ critical, high, medium, low, total }` | Implemented in handler + struct; tested in `test_severity_summary_valid_sbom` |
| 2 | Returns 404 for non-existent SBOM | Service checks SBOM existence first; tested in `test_severity_summary_nonexistent_sbom` |
| 3 | Counts only unique advisories | Service deduplicates by advisory ID; tested in `test_severity_summary_deduplication` |
| 4 | All levels default to 0 | `SeveritySummary::default()` initializes all to 0; tested in `test_severity_summary_empty_sbom` |
| 5 | Response time under 200ms for 500 advisories | Single query with GROUP BY; no N+1 |

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService method, endpoint
handler, and integration tests.

Implements TC-9201
```

With `--trailer="Assisted-by: Claude Code"`.

## Post-Implementation Steps

1. Run `cargo test` to verify all tests pass
2. Run `cargo clippy` and `cargo fmt --check` for linting/formatting
3. Verify scope containment via `git diff --name-only`
4. Check for sensitive patterns in staged diff
5. Push branch and open PR with description referencing TC-9201
6. Update Jira: set custom field with PR URL, add comment, transition to In Review
