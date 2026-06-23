# Task 2: Add advisory severity aggregation query to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer method that queries the database for advisory severity counts associated with a given SBOM. This method joins the `sbom_advisory` table with the `advisory` table, groups by severity, counts unique advisory IDs, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists (returning an error for 404 handling) and supports an optional severity threshold filter.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- The query should join `entity::sbom_advisory` with `entity::advisory` to access the severity field. Use SeaORM's `Select` and `JoinType::InnerJoin` pattern.
- First validate the SBOM exists by querying `entity::sbom` -- if not found, return `AppError::NotFound` consistent with the pattern in existing methods in `modules/fundamental/src/sbom/service/sbom.rs` (the `fetch` method likely does this).
- Deduplicate by advisory ID before counting -- the `sbom_advisory` join table may have multiple rows per advisory if an advisory affects multiple packages within the same SBOM. Use `DISTINCT` on advisory ID or `GROUP BY advisory.id` before the severity grouping.
- For the threshold filter: when `SeverityThreshold::High` is provided, include only `Critical` and `High` severities in the counts. Map severity levels to a numeric ordering (Critical=4, High=3, Medium=2, Low=1) and filter `WHERE severity_ordinal >= threshold_ordinal`.
- Use SeaORM raw SQL via `DatabaseConnection::query_all` or build the aggregation using SeaORM's `Column::count()` and `QuerySelect::group_by()` methods. Reference the query patterns in `common/src/db/query.rs` for SeaORM query building style.
- Wrap all database errors with `.context()` per the error handling convention, using `AppError` from `common/src/error.rs`.
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service files scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to add the new method to; reference `fetch` method for SBOM existence validation pattern
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for SeaORM query patterns involving the advisory entity
- `entity/src/sbom_advisory.rs` — join table entity needed for the aggregation query
- `entity/src/advisory.rs` — advisory entity with severity column
- `common/src/db/query.rs` — shared query builder helpers for filtering patterns
- `common/src/error.rs::AppError` — error enum for NotFound and context wrapping

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and compiles
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method returns correct severity counts by querying `sbom_advisory` joined with `advisory`
- [ ] Advisory IDs are deduplicated before counting (no double-counting)
- [ ] Optional threshold parameter filters severity levels correctly
- [ ] `total` field equals the sum of included severity counts

## Test Requirements
- [ ] Integration test: call `advisory_severity_summary` for an SBOM with known advisories, verify counts match
- [ ] Integration test: call with non-existent SBOM ID, verify error is returned
- [ ] Integration test: call with `threshold=High`, verify only Critical and High counts are included, Medium and Low are 0
- [ ] Integration test: verify deduplication -- SBOM with same advisory linked multiple times returns count of 1 for that advisory

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- sbom::service` — service tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

---

> [sdlc-workflow] Description digest: sha256-md:b8e2d5a14c3f097642e1b7835a6c9e0d12f8bf93e5c72168d9f4a30b5e8c7f21
