## Repository
trustify-backend

## Description
Add an `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table to aggregate advisory severity counts for a given SBOM ID. The method must deduplicate advisories by advisory ID before counting, and return an `AdvisorySeveritySummary` struct. It must return a 404-compatible error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_summary` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods for fetch, list, ingest) — each method takes a database connection parameter and returns `Result<T, AppError>`.
- The query should join `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) with `entity/src/advisory.rs` (Advisory entity) to access the severity field.
- Use SeaORM query builder to perform a `GROUP BY severity` aggregation with `COUNT(DISTINCT advisory_id)` to ensure deduplication when multiple SBOM-advisory relationships exist for the same advisory.
- Before aggregating, verify the SBOM exists by looking it up via `entity/src/sbom.rs`. If not found, return `AppError` with 404 status — consistent with the error handling pattern in `common/src/error.rs` using `.context()` wrapping.
- Use the shared query helpers in `common/src/db/query.rs` if applicable for building the query.
- The severity field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` defines the enum values to match against when grouping (Critical, High, Medium, Low).
- Map the grouped counts into the `AdvisorySeveritySummary` struct created in Task 1, computing `total` as the sum of all severity counts.
- Per the repository's key conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping throughout service methods.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct; add the new method here following the established patterns for database queries and error handling.
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse if the aggregation query benefits from shared filter logic.
- `common/src/error.rs::AppError` — Error enum implementing `IntoResponse`; use for 404 when SBOM is not found.
- `entity/src/sbom_advisory.rs` — Join table entity for SBOM-Advisory relationships; the primary data source for the aggregation query.

## Acceptance Criteria
- [ ] `SbomService` has an `advisory_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method counts unique advisories per severity level (deduplicates by advisory ID)
- [ ] The method returns a 404 error if the SBOM ID does not exist
- [ ] The `total` field equals the sum of critical + high + medium + low counts
- [ ] No new database tables are created — only existing entity tables are used

## Test Requirements
- [ ] Unit test: `advisory_summary` returns correct counts when SBOM has advisories at multiple severity levels
- [ ] Unit test: `advisory_summary` deduplicates advisories that appear multiple times in the join table
- [ ] Unit test: `advisory_summary` returns all-zero counts when SBOM exists but has no linked advisories
- [ ] Unit test: `advisory_summary` returns 404 error when SBOM ID does not exist

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct
