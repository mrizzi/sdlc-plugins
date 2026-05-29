## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the advisory-SBOM relationship table (`sbom_advisory`), deduplicates advisories by advisory ID, counts advisories at each severity level (Critical, High, Medium, Low), and returns an `AdvisorySeveritySummary`. This method provides the core business logic for the advisory-summary endpoint. The method must also validate that the SBOM ID exists, returning an appropriate error if not found.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- `SbomService::get_advisory_summary(sbom_id)` — NEW: queries `sbom_advisory` join table, joins to `advisory` table to access severity, deduplicates by advisory ID, aggregates counts by severity level

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (fetch, list, ingest methods). All service methods return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Use the `sbom_advisory` join entity from `entity/src/sbom_advisory.rs` to query advisories linked to a given SBOM. Join to the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT` or equivalent SeaORM query to avoid counting the same advisory multiple times.
- Use the query builder helpers from `common/src/db/query.rs` if applicable for constructing the aggregation query.
- For SBOM existence validation, follow the pattern used by existing `fetch` methods in `SbomService` — check if the SBOM exists first and return a 404-compatible `AppError` if not found.
- The aggregation should be performed at the database level (SQL `COUNT` with `GROUP BY severity`) rather than fetching all rows and counting in Rust, to meet the p95 < 200ms performance requirement for SBOMs with up to 500 advisories.
- No new database tables are required — use the existing `sbom_advisory` relationship table.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods showing the query and error handling patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory-specific query patterns that may demonstrate how severity is queried
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition

## Acceptance Criteria
- [ ] `get_advisory_summary` method exists on `SbomService`
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for each severity level
- [ ] Advisories are deduplicated by advisory ID (same advisory linked multiple times is counted once)
- [ ] Method returns a 404-equivalent error when the SBOM ID does not exist
- [ ] Aggregation is performed at the database level (not in-memory)

## Test Requirements
- [ ] Test with an SBOM that has advisories at multiple severity levels — verify correct counts
- [ ] Test with an SBOM that has duplicate advisory links — verify deduplication
- [ ] Test with a non-existent SBOM ID — verify 404 error is returned
- [ ] Test with an SBOM that has zero advisories — verify all counts are 0

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model

[sdlc-workflow] Description digest: sha256:6d645c0f7b93a4180cbf39a187a84df66f2852cba3d935c4aac1b9b61df53d0b
