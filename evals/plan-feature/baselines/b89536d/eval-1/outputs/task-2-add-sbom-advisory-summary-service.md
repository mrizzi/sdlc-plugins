# Task 2 -- Add advisory summary aggregation to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins with the advisory table to get severity, deduplicates by advisory ID, and returns aggregated severity counts as an `AdvisorySeveritySummary`. The method must also verify that the SBOM exists and return an appropriate error if not found. An optional severity threshold parameter filters counts to only include severities at or above the specified level.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `advisory_summary` method to `SbomService` that accepts an SBOM ID and optional threshold parameter, queries `sbom_advisory` join table, deduplicates by advisory ID, aggregates severity counts, and returns `AdvisorySeveritySummary`

## API Changes
- Internal service method: `SbomService::advisory_summary(sbom_id, threshold: Option<SeverityThreshold>) -> Result<AdvisorySeveritySummary, AppError>` -- NEW

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (e.g., the `fetch` and `list` methods for error handling and database query structure)
- Use SeaORM query builder to join `sbom_advisory` (entity at `entity/src/sbom_advisory.rs`) with `advisory` (entity at `entity/src/advisory.rs`) on advisory ID
- Deduplicate by advisory ID using `DISTINCT` or `GROUP BY` in the query to count only unique advisories
- Aggregate counts using SQL `COUNT` with `CASE WHEN severity = 'critical' THEN 1 END` pattern, or alternatively fetch distinct advisories and count in Rust -- prefer the SQL approach for p95 < 200ms performance requirement
- For the threshold filter: define severity ordering (Critical > High > Medium > Low) and filter the aggregation to only include severities at or above the threshold
- Return 404 via `AppError` if the SBOM ID does not exist -- verify SBOM existence before running the aggregation query, consistent with existing SBOM endpoint behavior in `modules/fundamental/src/sbom/endpoints/get.rs`
- Use shared query helpers from `common/src/db/query.rs` if applicable for building the aggregation query
- Error handling: wrap all database errors with `.context()` per the `AppError` pattern in `common/src/error.rs`

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list methods to follow for query patterns and error handling
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `entity/src/sbom_advisory.rs` -- the join table entity connecting SBOMs to advisories
- `entity/src/advisory.rs` -- the advisory entity containing the severity field
- `common/src/error.rs::AppError` -- error type for 404 and other error responses

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` method exists and compiles
- [ ] Method returns correct severity counts for an SBOM with multiple advisories
- [ ] Method deduplicates advisories by advisory ID (same advisory linked multiple times counts once)
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Optional threshold parameter correctly filters severity counts
- [ ] Query performance supports p95 < 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Unit/integration test: SBOM with advisories at each severity level returns correct counts
- [ ] Unit/integration test: duplicate advisory links are deduplicated (advisory linked via multiple paths counts once)
- [ ] Unit/integration test: nonexistent SBOM ID returns appropriate error
- [ ] Unit/integration test: threshold parameter filters correctly (e.g., threshold=high returns only critical and high counts)
- [ ] Unit/integration test: SBOM with zero advisories returns all-zero counts

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary response model
