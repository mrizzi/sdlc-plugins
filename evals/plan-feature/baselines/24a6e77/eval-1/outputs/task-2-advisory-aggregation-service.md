# Task 2 — Add advisory severity aggregation query to SbomService

## Repository
trustify-backend

## Description
Extend `SbomService` with a method that queries the database for advisory severity counts associated with a given SBOM ID. The method must join the `sbom_advisory` join table with the `advisory` table, deduplicate by advisory ID, group by severity level, and return an `AdvisorySeveritySummary`. It must also support an optional severity threshold parameter that filters to counts at or above the specified severity level. If the SBOM ID does not exist, the method must return an appropriate error that the endpoint layer can map to a 404 response.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Uuid, threshold: Option<Severity>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — update if necessary to expose the new method

## API Changes
- `SbomService::get_advisory_summary` — NEW: aggregation query returning severity counts for a given SBOM

## Implementation Notes
- Use the existing `sbom_advisory` entity at `entity/src/sbom_advisory.rs` to join SBOMs to advisories, and the `advisory` entity at `entity/src/advisory.rs` to access the severity field
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use this to understand how severity is stored and represented in the database
- Deduplicate advisories by advisory ID before counting — use `SELECT DISTINCT advisory_id` or equivalent SeaORM query to avoid double-counting advisories linked multiple times
- For the threshold filter: define severity ordering (Critical > High > Medium > Low) and filter to include only severities at or above the threshold. If threshold is `None`, include all severities
- Return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist — verify SBOM existence before running the aggregation query, following the pattern in the existing `get` method in `sbom.rs`
- Use SeaORM's `select`, `join`, `group_by`, and `count` query builder methods — reference the query helpers in `common/src/db/query.rs` for established patterns
- The `total` field should equal the sum of all (filtered) severity counts
- Per constraints (Section 5.2): inspect the existing `SbomService` methods before implementing to follow their error handling, transaction, and query patterns
- Per constraints (Section 5.4): reuse existing query helpers from `common/src/db/query.rs` rather than writing new query logic

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods demonstrate the query pattern, error handling with `AppError`, and database access style
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `NotFound` variant and `IntoResponse` implementation
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity for SeaORM queries
- `entity/src/advisory.rs` — advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Query deduplicates advisories by advisory ID before counting
- [ ] Query correctly groups by severity level and returns counts for critical, high, medium, low
- [ ] `total` field equals the sum of all severity counts in the response
- [ ] Returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Optional threshold parameter correctly filters to severities at or above the specified level
- [ ] Method follows existing `SbomService` patterns for error handling and database access

## Test Requirements
- [ ] Unit/integration test: SBOM with advisories at all four severity levels returns correct counts
- [ ] Unit/integration test: SBOM with no advisories returns all zeros
- [ ] Unit/integration test: non-existent SBOM ID returns NotFound error
- [ ] Unit/integration test: duplicate advisories (same advisory linked to SBOM multiple times) are counted only once
- [ ] Unit/integration test: threshold=high filters out medium and low, returns only critical and high counts
- [ ] Unit/integration test: threshold=critical returns only critical count

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
