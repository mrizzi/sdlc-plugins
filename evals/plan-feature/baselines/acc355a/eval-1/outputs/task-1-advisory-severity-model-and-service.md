## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` response model and a severity aggregation query method to `SbomService`. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The service method queries the `sbom_advisory` join table, joins to the `advisory` table for severity data, deduplicates by advisory ID, and returns counts grouped by severity level (critical, high, medium, low) plus a total.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to expose the new model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(sbom_id)` method to `SbomService` that queries severity counts

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct definition, derives, and serde attributes.
- The `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` to match sibling model structs.
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` as the join table to find advisories linked to a given SBOM.
- Use the `advisory` entity from `entity/src/advisory.rs` to access the severity field on each advisory.
- Deduplicate advisories by advisory ID before counting (the requirement specifies unique advisory counts).
- The aggregation query should use SeaORM's `select` with `group_by` on the severity column and `count` to compute counts server-side in SQL rather than fetching all rows into memory.
- Follow the query builder patterns from `common/src/db/query.rs` for building the query.
- The service method should return `Result<AdvisorySeveritySummary, AppError>`, following the error handling pattern used by existing methods in `modules/fundamental/src/sbom/service/sbom.rs` (e.g., `SbomService::fetch`).
- Check that the SBOM exists before querying advisories; return a 404-equivalent error if the SBOM ID is not found, consistent with existing SBOM service methods.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition patterns, derives, and serde configuration
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service method signatures, error handling with `AppError`, and SeaORM query patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for building the aggregation query
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity; use as the base relation for the aggregation query
- `common/src/error.rs::AppError` — the standard error enum; reuse for 404 and internal error responses

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields `critical`, `high`, `medium`, `low`, `total`
- [ ] `SbomService` has a `get_advisory_severity_summary` method that returns severity counts for a given SBOM ID
- [ ] Advisories are deduplicated by advisory ID in the count
- [ ] Method returns an error when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test or service-level test verifying `get_advisory_severity_summary` returns correct counts for an SBOM with known advisory data
- [ ] Test verifying that duplicate advisory links are counted only once
- [ ] Test verifying that a non-existent SBOM ID returns an appropriate error
