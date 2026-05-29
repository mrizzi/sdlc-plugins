## Repository
trustify-backend

## Target Branch
main

## Description
Add a new method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method queries the `sbom_advisory` join table to find all advisories linked to the SBOM, groups them by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. If the SBOM does not exist, the method returns an appropriate error that the endpoint layer can map to a 404 response.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` — methods like `fetch` and `list` demonstrate the query structure, error handling with `.context()`, and return type conventions.
- Use the `sbom_advisory` join table entity from `entity/src/sbom_advisory.rs` to query advisories linked to the given SBOM. Join with the `advisory` entity from `entity/src/advisory.rs` to access the severity field.
- Deduplicate advisories by advisory ID before counting — the join table may contain duplicate links. Use `SELECT DISTINCT advisory_id, severity FROM sbom_advisory JOIN advisory ...` or equivalent SeaORM query.
- Use SeaORM's `group_by` and `count` capabilities, or fetch distinct advisory severities and count in Rust — choose the approach that keeps the computation in the database for performance (p95 < 200ms for 500 advisories).
- Return `AppError` (from `common/src/error.rs`) with appropriate context when the SBOM ID is not found. Follow the same error pattern used by the `fetch` method in `SbomService`.
- Use `common/src/db/query.rs` helpers if applicable for query construction.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct where the new method will be added; follow its method signatures and error handling patterns
- `entity/src/sbom_advisory.rs` — the join table entity relating SBOMs to advisories; use this for the aggregation query
- `entity/src/advisory.rs` — the advisory entity containing the severity field to group by
- `common/src/error.rs::AppError` — the shared error type to return for SBOM-not-found cases

## Acceptance Criteria
- [ ] `SbomService` has a new `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method queries advisories via the `sbom_advisory` join table and counts by severity
- [ ] Advisory IDs are deduplicated before counting (no double-counting)
- [ ] Returns an error mappable to 404 when the SBOM ID does not exist
- [ ] The aggregation is performed in the database query, not by fetching all rows into memory
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit or integration test: given an SBOM with known advisories at various severities, verify the returned counts are correct
- [ ] Test: given an SBOM with duplicate advisory links in the join table, verify deduplication (each advisory counted once)
- [ ] Test: given a non-existent SBOM ID, verify the method returns an error

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

[sdlc-workflow] Description digest: sha256:2417803c2952d068570b0b2ca26e9d8ee971736881d3f39823e8205d0f76174a
