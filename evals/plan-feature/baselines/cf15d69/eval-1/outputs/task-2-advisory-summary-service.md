## Repository
trustify-backend

## Target Branch
main

## Description
Add an aggregation method to `SbomService` that queries the `sbom_advisory` join table to count unique advisories by severity level for a given SBOM ID. This method performs the server-side aggregation that replaces client-side counting, grouping advisories by their severity field and deduplicating by advisory ID. It also supports optional threshold filtering to return only counts at or above a specified severity level.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
The new method in `modules/fundamental/src/sbom/service/sbom.rs` should follow the existing query patterns in `SbomService` (fetch, list, ingest methods). Use SeaORM to join `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs` to access the severity field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`). Group by severity, count distinct advisory IDs, and map results into `AdvisorySeveritySummary`. Use the query helpers from `common/src/db/query.rs` for building the query. Before aggregating, verify the SBOM exists by querying `entity/src/sbom.rs` — return `AppError::NotFound` (from `common/src/error.rs`) if it does not exist. If a `SeverityThreshold` is provided, zero out counts below the threshold.

Per Key Conventions (Error handling): All service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` files scope.

Per Key Conventions (Query helpers): Use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service files scope.

Per Key Conventions (Framework): Use SeaORM for database queries. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` files scope.

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` method is implemented and returns `AdvisorySeveritySummary`
- [ ] Advisory IDs are deduplicated before counting (unique advisories only)
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] Optional `threshold` parameter filters counts to only include severities at or above the threshold
- [ ] Query uses existing `sbom_advisory` join table — no new database tables created
- [ ] Method compiles and integrates with existing `SbomService`

## Test Requirements
- [ ] Unit test for aggregation logic with mock data covering all severity levels
- [ ] Unit test verifying deduplication of advisory IDs (same advisory linked multiple times)
- [ ] Unit test for threshold filtering (e.g., threshold=High returns only critical and high counts, zeros for medium and low)
- [ ] Unit test for non-existent SBOM returning appropriate error

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental sbom::service` — service unit tests pass

## Dependencies
- Depends on: Task 1 — advisory severity summary model

[sdlc-workflow] Description digest: sha256-md:533373401e86f4af6c34f4edaca6e4f415a49627d8dc75cbe5cc77722ea815d2
