# Task 2 — Add severity aggregation query to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new method to `SbomService` that queries the database to compute advisory severity counts for a given SBOM ID. The method must join the `sbom_advisory` table with the `advisory` table, deduplicate by advisory ID, group by severity level, and return an `AdvisorySeveritySummary` with the counts. It must return a not-found error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add a new method `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` to `SbomService`

## API Changes
- Internal service API: NEW `SbomService::advisory_severity_summary(sbom_id)` method returning `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing query patterns in `SbomService` (see `modules/fundamental/src/sbom/service/sbom.rs`) for database access, connection handling, and error wrapping with `.context()`.
- Use SeaORM query builder to join `sbom_advisory` and `advisory` entities. The join table entity is at `entity/src/sbom_advisory.rs` and the advisory entity at `entity/src/advisory.rs`.
- Deduplicate advisories by advisory ID before counting — use `DISTINCT` or `GROUP BY` on the advisory ID to avoid counting the same advisory multiple times.
- Group results by the severity field from the `advisory` entity (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for how severity is modeled).
- Use `common/src/db/query.rs` for any shared query helpers that apply to filtering or aggregation.
- Return `AppError::NotFound` (see `common/src/error.rs`) if the SBOM does not exist — check SBOM existence before running the aggregation query, consistent with how `GET /api/v2/sbom/{id}` handles missing SBOMs.
- Per constraints doc section 5.2: read the existing service file to understand method signatures, return types, and error handling patterns before implementing.
- Per constraints doc section 5.4: reuse existing query helpers and error types rather than creating new ones.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods for connection handling, error wrapping, and SBOM existence checks
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `NotFound` variant and `IntoResponse` implementation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the join query
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary(sbom_id)` method exists and compiles
- [ ] Method returns correct severity counts by querying the `sbom_advisory` + `advisory` tables
- [ ] Advisories are deduplicated by advisory ID (no double-counting)
- [ ] Method returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Method returns zero counts for severity levels with no matching advisories

## Test Requirements
- [ ] Unit/integration test: SBOM with known advisories at various severity levels returns correct counts
- [ ] Unit/integration test: SBOM with no advisories returns all-zero counts with total=0
- [ ] Unit/integration test: SBOM with duplicate advisory links returns deduplicated counts
- [ ] Unit/integration test: non-existent SBOM ID returns not-found error

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
