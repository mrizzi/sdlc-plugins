## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer method that queries the database to aggregate advisory severity counts for a given SBOM. This method joins the `sbom_advisory` table with the `advisory` table, groups by severity, counts distinct advisory IDs, and returns an `AdvisorySeveritySummary`. It also verifies the SBOM exists, returning an appropriate error if not found.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — New file containing `impl SbomService` method `fn advisory_summary(&self, sbom_id: Uuid, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>` that performs the aggregation query

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service method

## Implementation Notes
- Follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` which shows how `SbomService` methods are structured: they accept a database connection trait reference and return `Result<T, AppError>`.
- Use SeaORM's `Entity::find()` on `entity::sbom_advisory` joined with `entity::advisory` to perform the aggregation.
- First check SBOM existence using `entity::sbom::Entity::find_by_id(sbom_id)`. If `None`, return `AppError::NotFound` (following the pattern in `common/src/error.rs`).
- Use `.group_by(advisory::Column::Severity)` and `.count()` to aggregate counts per severity level.
- Deduplicate by advisory ID: use `COUNT(DISTINCT advisory_id)` to avoid counting the same advisory multiple times for the same SBOM.
- Map severity string values ("critical", "high", "medium", "low") to the corresponding struct fields.
- Use `.context()` for error wrapping as per project conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service methods showing query patterns, error handling, and database access conventions
- `entity/src/sbom_advisory.rs` — The join table entity linking SBOMs to advisories
- `entity/src/advisory.rs` — Advisory entity with the severity column
- `common/src/error.rs::AppError` — Error type with `NotFound` variant for 404 responses
- `common/src/db/query.rs` — Shared query builder helpers for filtering

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct severity counts from the database
- [ ] Method returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Advisory IDs are deduplicated (COUNT DISTINCT) so the same advisory is not counted twice
- [ ] Total field equals the sum of critical + high + medium + low counts

## Test Requirements
- [ ] Unit test with mock database verifying correct aggregation of severity counts
- [ ] Unit test verifying `NotFound` error when SBOM does not exist

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental sbom::service::advisory_summary` — unit tests pass

## Dependencies
- Depends on: Task 1 — Advisory summary model

## Applicable Conventions
- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `service/` scope.
- **Error handling**: Applies: task modifies service code matching the convention's `Result<T, AppError>` with `.context()` scope.

[sdlc-workflow] Description digest: sha256-md:766173b53b700d24f583e318d3c2c71844f94b85b6e39072a8be387ac992b0e1
