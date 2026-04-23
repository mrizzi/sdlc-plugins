## Repository
trustify-backend

## Description
Implement the service-layer method that queries the database to aggregate advisory severity counts for a given SBOM ID. This method performs a SQL GROUP BY query on the sbom_advisory join table, deduplicates by advisory ID, groups by severity level, and returns an AdvisorySeveritySummary. It also validates that the SBOM exists, returning an appropriate error if not found.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Contains the `advisory_summary` method on SbomService (or as a standalone function taking a database connection) that queries sbom_advisory joined with advisory, groups by severity, counts distinct advisory IDs, and returns `Result<AdvisorySeveritySummary, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service module

## Implementation Notes
- Follow the query and service patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). Specifically, look at how `fetch` validates an SBOM ID exists and returns a 404 via `AppError` if not found.
- Use SeaORM query builder to join `entity/src/sbom_advisory.rs` (sbom_advisory entity) with `entity/src/advisory.rs` (advisory entity) to access the severity field.
- Apply `COUNT(DISTINCT advisory.id)` grouped by `advisory.severity` to deduplicate advisories. Map each severity string (Critical, High, Medium, Low) to the corresponding field on `AdvisorySeveritySummary`.
- Reference `common/src/db/query.rs` for shared query helpers if filtering is needed.
- Use `common/src/error.rs` AppError for error propagation; return `AppError::NotFound` when the SBOM ID does not exist.
- Compute `total` as the sum of all four severity counts rather than a separate query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — Reuse the SBOM existence check pattern before running the aggregation query
- `common/src/db/query.rs` — Query builder helpers for constructing SeaORM queries
- `common/src/error.rs::AppError` — Error type for 404 and internal error responses

## Acceptance Criteria
- [ ] `advisory_summary` method exists and accepts an SBOM ID parameter plus database connection
- [ ] Method returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Returns `AppError::NotFound` (or equivalent) when the SBOM ID does not exist in the database
- [ ] Counts are deduplicated by advisory ID (same advisory linked to multiple packages in the SBOM is counted once)
- [ ] Severity counts are correctly grouped into critical, high, medium, low fields
- [ ] Total field equals the sum of all four severity counts
- [ ] `cargo check -p trustify-module-fundamental` passes

## Test Requirements
- [ ] Unit/integration test that creates an SBOM with known advisories at various severity levels and verifies the returned counts match expected values
- [ ] Test that an SBOM with no linked advisories returns all-zero counts
- [ ] Test that a non-existent SBOM ID returns a NotFound error
- [ ] Test that duplicate advisories (same advisory linked via multiple packages) are counted only once
- [ ] Test with advisories at all four severity levels to verify correct grouping

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — all service tests pass

## Dependencies
- Depends on: Task 1 — Advisory summary model (requires AdvisorySeveritySummary struct)
