# Task 2 — Add Advisory Severity Aggregation Query to SbomService

## Repository
trustify-backend

## Description
Add a new method to `SbomService` that queries the database to compute advisory severity counts for a given SBOM ID. The method must join the `sbom_advisory` table with the `advisory` table, group by severity, and count unique advisories (deduplicated by advisory ID) at each severity level (Critical, High, Medium, Low). It must return a 404 error if the SBOM does not exist, consistent with existing SBOM service methods.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add a new method `advisory_severity_summary(&self, sbom_id: Uuid, db: &DbConn) -> Result<AdvisorySeveritySummary, AppError>` (or similar signature matching existing patterns)
- `modules/fundamental/src/sbom/service/mod.rs` — ensure new method is accessible (if service uses re-exports)

## API Changes
- No external API changes — this is an internal service method consumed by the endpoint (Task 3)

## Implementation Notes
- Follow the query pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods like fetch and list) for database connection handling, error wrapping, and return types.
- Use SeaORM query builder to construct the aggregation. The query should:
  1. Verify the SBOM exists (return 404 via `AppError` if not, matching `common/src/error.rs` patterns)
  2. Join `sbom_advisory` (see `entity/src/sbom_advisory.rs`) with `advisory` (see `entity/src/advisory.rs`)
  3. Filter by `sbom_id`
  4. Group by severity field from the advisory entity
  5. Count distinct advisory IDs per severity group
  6. Map the grouped counts into an `AdvisorySeveritySummary` struct
- Reference `common/src/db/query.rs` for shared query builder helpers that may assist with filtering.
- The method should use `.context()` error wrapping consistent with existing service methods (see `common/src/error.rs` for `AppError` enum).
- No new database tables are needed — the `sbom_advisory` join table already provides the SBOM-to-advisory relationship.
- Per constraints doc section 5.2: inspect existing service methods before writing to ensure pattern consistency.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the join query
- `entity/src/advisory.rs` — Advisory entity with severity field for grouping
- `common/src/error.rs::AppError` — error handling enum for 404 responses
- `common/src/db/query.rs` — shared query helpers for building database queries
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods as pattern reference for error handling and DB access

## Acceptance Criteria
- [ ] New aggregation method exists on `SbomService`
- [ ] Method returns `AdvisorySeveritySummary` with correct severity counts for a given SBOM
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method uses existing SeaORM entities without creating new database tables
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit/integration test: verify correct severity counts for an SBOM with known advisory data
- [ ] Unit/integration test: verify deduplication — same advisory linked twice should count once
- [ ] Unit/integration test: verify 404 is returned for a non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary Response Model
