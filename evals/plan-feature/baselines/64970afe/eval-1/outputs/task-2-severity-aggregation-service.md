## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the `sbom_advisory` join table, groups advisories by severity level, deduplicates by advisory ID, and returns a `SeveritySummary` with the counts. This method will be called by the new advisory summary endpoint to compute severity breakdowns server-side, replacing the current client-side multi-page fetch-and-count approach.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary` method to `SbomService`

## Implementation Notes
- Add a method `pub async fn get_advisory_severity_summary(&self, sbom_id: Uuid, db: &impl ConnectionTrait) -> Result<SeveritySummary, AppError>` to `SbomService`.
- Query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with the `advisory` table (`entity/src/advisory.rs`) to retrieve advisories linked to the given SBOM ID.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT advisory_id, severity` or equivalent SeaORM query to ensure each advisory is counted only once.
- Group results by severity level (Critical, High, Medium, Low) and count each group.
- Use the `severity` field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`) to determine the severity level of each advisory.
- Compute `total` as the sum of all severity counts.
- Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist, consistent with existing SBOM service methods in `sbom.rs`.
- Per CONVENTIONS.md §Module Pattern: implement the service method within the existing `SbomService` in the `service/` subdirectory. See `modules/fundamental/src/sbom/service/sbom.rs` for existing service method patterns (fetch, list, ingest).
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service/ directory scope.
- Per CONVENTIONS.md §Query Helpers: use shared query builder helpers from `common/src/db/query.rs` for any filtering needs in the aggregation query. See `common/src/db/query.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the new method
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table
- `entity/src/advisory.rs` — SeaORM entity with the severity field
- `common/src/error.rs::AppError` — error enum for NotFound and other error variants

## Acceptance Criteria
- [ ] `get_advisory_severity_summary` method exists on `SbomService`
- [ ] Method returns correct severity counts for a given SBOM ID
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Returns 404-compatible error when SBOM ID does not exist
- [ ] Total count equals the sum of critical + high + medium + low

## Test Requirements
- [ ] Unit test: verify correct counts with known advisory-severity data
- [ ] Unit test: verify deduplication when the same advisory is linked multiple times
- [ ] Unit test: verify NotFound error for non-existent SBOM ID
- [ ] Unit test: verify zero counts when SBOM has no linked advisories

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
