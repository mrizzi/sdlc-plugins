## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_severity_summary` method to `SbomService` that queries the database for advisory severity counts associated with a given SBOM. The method must deduplicate advisories by advisory ID, group by severity level, and return an `AdvisorySeveritySummary`. It must return a 404-equivalent error if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- Add the `advisory_severity_summary` method to `SbomService`

## Implementation Notes
The method should:
1. First verify the SBOM exists by querying the `sbom` entity. If not found, return `AppError::NotFound` (follow the pattern in existing `SbomService` methods in `modules/fundamental/src/sbom/service/sbom.rs`).
2. Query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to get all advisories linked to the SBOM.
3. Use a SQL `GROUP BY` on the advisory severity field with `COUNT(DISTINCT advisory_id)` to deduplicate and aggregate in the database rather than in application memory. This is critical for the p95 < 200ms performance target.
4. Map the grouped results into the `AdvisorySeveritySummary` struct, computing `total` as the sum of all severity counts.

Use SeaORM query builder patterns consistent with existing service methods in `modules/fundamental/src/sbom/service/sbom.rs`. Error handling should use `Result<AdvisorySeveritySummary, AppError>` with `.context()` wrapping, consistent with `common/src/error.rs::AppError`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Extend this existing service; follow its patterns for database access and error handling
- `common/src/error.rs::AppError` -- Reuse for 404 and internal error responses
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and pagination (reference for SeaORM patterns)
- `entity/src/sbom_advisory.rs` -- The SBOM-Advisory join table entity for the aggregation join
- `entity/src/advisory.rs` -- The Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService` has a public `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method deduplicates advisories by advisory ID (no double-counting)
- [ ] The method groups and counts by severity level (Critical, High, Medium, Low)
- [ ] The `total` field equals the sum of all four severity counts
- [ ] The method returns a 404-mapped error when the SBOM ID does not exist
- [ ] Aggregation is performed in SQL (GROUP BY), not in application memory

## Test Requirements
- [ ] Unit test: service returns correct severity counts for an SBOM with known advisory data
- [ ] Unit test: service returns 404 error for a nonexistent SBOM ID
- [ ] Unit test: advisories with duplicate IDs are counted only once

## Verification Commands
- `cargo check -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental` -- all tests pass

## Dependencies
- Depends on: Task 1 -- Severity summary model (provides the `AdvisorySeveritySummary` struct)
