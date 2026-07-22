# Task 2: Add advisory severity aggregation service method

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Add a method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM ID. The method joins the `sbom_advisory` join table with the `advisory` table, groups by severity, and returns an `AdvisorySeveritySummary`. Advisories must be deduplicated by advisory ID before counting. The method must return a 404-compatible error if the SBOM ID does not exist.

## Acceptance Criteria

- [ ] `SbomService` has a new async method `get_advisory_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>) -> Result<AdvisorySeveritySummary, AppError>`
- [ ] Method first validates that the SBOM exists, returning a not-found error if it does not
- [ ] Method queries `sbom_advisory` joined with `advisory` to count unique advisories per severity level
- [ ] Advisories are deduplicated by advisory ID (no double-counting if an advisory is linked multiple times)
- [ ] When `threshold` is `Some(SeverityThreshold::Critical)`, only the `critical` count is populated; others are zero
- [ ] When `threshold` is `Some(SeverityThreshold::High)`, `critical` and `high` counts are populated
- [ ] The `total` field reflects the sum of the populated severity counts
- [ ] Method uses SeaORM query builder, not raw SQL

## Test Requirements

- [ ] Unit test with mock database verifies correct aggregation for an SBOM with mixed severity advisories
- [ ] Unit test verifies deduplication: same advisory linked twice produces count of 1
- [ ] Unit test verifies not-found error when SBOM ID does not exist
- [ ] Unit test verifies threshold filtering returns only severities at or above the threshold

## Dependencies

- Task 1 (advisory severity summary model) -- requires `AdvisorySeveritySummary` and `SeverityThreshold` types

## Files to Modify

- `modules/fundamental/src/sbom/service/sbom.rs` -- add `get_advisory_summary` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` -- ensure advisory_summary model types are imported

## Implementation Notes

- Follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` where existing methods like `fetch` and `list` use SeaORM queries and return `Result<T, AppError>`.
  - Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `service/` scope.
- Use `AppError` from `common/src/error.rs` for error returns, wrapping database errors with `.context()` as done in existing service methods.
  - Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's error handling scope.
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to join SBOMs to advisories, and read the `severity` field from the `advisory` entity in `entity/src/advisory.rs`.
- Use SeaORM's `select_only()`, `column()`, and `group_by()` to build the aggregation query, following patterns from `common/src/db/query.rs` for query construction.
  - Applies: task modifies service code that uses query helpers matching the convention's query helpers scope.
