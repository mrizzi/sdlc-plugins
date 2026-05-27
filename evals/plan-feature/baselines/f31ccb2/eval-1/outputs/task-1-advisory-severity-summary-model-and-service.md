## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` response model and a service method on `SbomService` that aggregates unique advisory severity counts for a given SBOM. This provides the data layer for the new advisory summary endpoint, querying the existing `sbom_advisory` join table and `advisory` entity to count advisories grouped by severity level (Critical, High, Medium, Low), deduplicating by advisory ID.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new summary model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct definition, derives, and serialization attributes.
- The new struct should derive `serde::Serialize`, `serde::Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` (matching sibling model patterns).
- The service method should query `entity::sbom_advisory` joined with `entity::advisory` to count distinct advisory IDs grouped by the severity field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- Use SeaORM query builder patterns from `common/src/db/query.rs` for constructing the aggregation query.
- Return `Result<AdvisorySeveritySummary, AppError>` following the error handling pattern in `common/src/error.rs`.
- Before querying advisories, verify the SBOM exists by attempting to fetch it (reuse the existing `SbomService::fetch` method). Return a 404 `AppError` if the SBOM ID does not exist, consistent with `modules/fundamental/src/sbom/endpoints/get.rs`.
- No new database tables are needed — use existing `sbom_advisory` relationship table per non-functional requirements.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — struct pattern to follow for derives and serialization
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition to reference
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods to extend
- `common/src/db/query.rs` — shared query builder helpers for constructing the aggregation query
- `common/src/error.rs::AppError` — error type for 404 handling
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-Advisory relationships

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] `SbomService` has an `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method counts only unique advisories (deduplicated by advisory ID)
- [ ] The method returns a 404 error when the SBOM ID does not exist
- [ ] The `total` field equals the sum of `critical + high + medium + low`

## Test Requirements
- [ ] Unit test: `advisory_severity_summary` returns correct counts for an SBOM with advisories at mixed severity levels
- [ ] Unit test: `advisory_severity_summary` returns all zeros for an SBOM with no linked advisories
- [ ] Unit test: `advisory_severity_summary` returns 404 error for a non-existent SBOM ID
- [ ] Unit test: `advisory_severity_summary` deduplicates advisories (same advisory linked multiple times counts once)
