# Task 2 — Add severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method queries the existing `sbom_advisory` join table, joins to the `advisory` table to access severity, deduplicates advisories by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. It must also support an optional severity threshold filter to return only counts at or above a specified severity level.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Id, threshold: Option<Severity>) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
- Follow the query patterns established in `modules/fundamental/src/sbom/service/sbom.rs` for existing methods (fetch, list, ingest). Use the same error handling pattern: `Result<T, AppError>` with `.context()` wrapping.
- Use the shared query builder helpers from `common/src/db/query.rs` for constructing the aggregation query if applicable.
- The query must JOIN `sbom_advisory` with `advisory` on advisory ID, filter by the given SBOM ID, apply DISTINCT on advisory ID to deduplicate, and then COUNT grouped by severity.
- Use SeaORM query builder to construct the aggregation. Reference the `entity/sbom_advisory.rs` (SBOM-Advisory join table entity) and `entity/advisory.rs` (Advisory entity with severity field) for column definitions.
- For the optional `threshold` parameter: severity levels have a natural ordering (Critical > High > Medium > Low). When a threshold is specified, filter to only include advisories at or above that severity level before counting.
- Return a 404 error (consistent with existing SBOM endpoints in `modules/fundamental/src/sbom/endpoints/get.rs`) when the SBOM ID does not exist. Check SBOM existence before running the aggregation query.
- The `total` field should be the sum of all returned severity counts (after threshold filtering if applied).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend; follow its method signatures and error handling patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how advisory queries are constructed with SeaORM
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/error.rs::AppError` — error type with IntoResponse implementation; use for 404 and other error cases
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/advisory.rs` — Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and compiles
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct severity counts grouped by level (critical, high, medium, low)
- [ ] Method returns 404 AppError when SBOM ID does not exist
- [ ] Method supports optional threshold parameter that filters counts to only include severities at or above the threshold
- [ ] The total field equals the sum of all counted severity levels

## Test Requirements
- [ ] Unit test: verify correct aggregation for an SBOM with advisories at mixed severity levels
- [ ] Unit test: verify deduplication — same advisory linked to SBOM multiple times is counted once
- [ ] Unit test: verify 404 is returned for a non-existent SBOM ID
- [ ] Unit test: verify threshold filtering correctly excludes lower severity levels
- [ ] Unit test: verify an SBOM with zero advisories returns all counts as 0

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model
