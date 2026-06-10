## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the `sbom_advisory` join table to aggregate advisory severity counts for a given SBOM ID. The method must deduplicate advisories by advisory ID before counting, ensuring each advisory is counted only once regardless of how many times it is linked to the SBOM. The method must also return a 404-compatible error when the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(&self, sbom_id: Id, threshold: Option<String>, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest methods) for error handling and database access patterns.
- Use SeaORM query builder to join `sbom_advisory` with `advisory` entities and aggregate counts grouped by severity level. The relevant entities are:
  - `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity
  - `entity/src/advisory.rs` — Advisory entity with severity field
- Apply `SELECT DISTINCT advisory_id` or equivalent deduplication to ensure unique advisory counting per the requirement.
- Use SQL `COUNT` with `CASE WHEN severity = 'critical' THEN 1 END` pattern (or equivalent SeaORM expressions) to compute per-severity counts in a single query for performance.
- Return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist — first verify SBOM existence before running the aggregation query, consistent with existing SBOM endpoint behavior in `modules/fundamental/src/sbom/endpoints/get.rs`.
- The `threshold` parameter is optional (non-MVP). When provided, filter the counts to only include severities at or above the given threshold. Severity ordering: critical > high > medium > low.
- Use shared query helpers from `common/src/db/query.rs` where applicable for filtering logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct where the new method will be added; follow its patterns for database access and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how advisory-related queries are structured
- `common/src/error.rs::AppError` — error enum with NotFound variant for 404 responses
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct counts for critical, high, medium, and low severities
- [ ] Method returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Method accepts optional `threshold` parameter to filter severity counts
- [ ] Total field equals the sum of all severity counts (after threshold filtering if applied)

## Test Requirements
- [ ] Test that aggregation returns correct counts for an SBOM with known advisory severities
- [ ] Test that advisories linked multiple times to the same SBOM are deduplicated (counted only once)
- [ ] Test that a non-existent SBOM ID returns a NotFound error
- [ ] Test that threshold parameter filters counts correctly (e.g., threshold=high returns only critical and high counts)
- [ ] Test that an SBOM with zero advisories returns all-zero counts

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental sbom` — service tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model struct
