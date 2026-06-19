## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to query the database for advisory severity counts linked to a specific SBOM. The method joins `sbom_advisory` with `advisory` to count advisories grouped by severity level, deduplicating by advisory ID. It returns an `AdvisorySeveritySummary` struct. The method also verifies the SBOM exists and returns an appropriate error if not found.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Service function for advisory severity aggregation query

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service module

## Implementation Notes
Follow the service pattern used in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for the function signature and database connection handling. The service should:

1. Accept a database connection/pool and SBOM ID as parameters
2. First verify the SBOM exists by querying `entity/src/sbom.rs` — return `AppError` (from `common/src/error.rs`) with 404 status if not found
3. Build a SeaORM query joining `sbom_advisory` (from `entity/src/sbom_advisory.rs`) to `advisory` (from `entity/src/advisory.rs`)
4. Filter by the given SBOM ID
5. Use `SELECT COUNT(DISTINCT advisory.id)` grouped by `advisory.severity` to get per-severity counts
6. Map the query results into `AdvisorySeveritySummary` fields
7. Optionally support a `threshold` parameter that filters to severities at or above the given level

Use `.context()` error wrapping as required by the error handling convention. The query helpers in `common/src/db/query.rs` provide shared filtering and pagination utilities — review them for any reusable query-building patterns.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Query helpers: review `common/src/db/query.rs` for shared filtering utilities before writing custom query logic.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reference for service method patterns, DB connection handling, and error wrapping
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference for querying advisory entities
- `common/src/error.rs::AppError` — Error type for 404 and internal errors
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `entity/src/sbom_advisory.rs` — Join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] Service method accepts SBOM ID and optional threshold parameter
- [ ] Returns `AdvisorySeveritySummary` with correct severity counts
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] Deduplicates advisories by advisory ID before counting
- [ ] Threshold parameter filters to severities at or above the given level
- [ ] Uses `.context()` wrapping on all fallible operations

## Test Requirements
- [ ] Unit test for severity count aggregation logic
- [ ] Test that non-existent SBOM ID returns 404 error
- [ ] Test that duplicate advisories are not double-counted

## Dependencies
- Depends on: Task 1 — Create AdvisorySeveritySummary response model
- Depends on: Task 2 — Verify sbom_advisory entity supports severity aggregation