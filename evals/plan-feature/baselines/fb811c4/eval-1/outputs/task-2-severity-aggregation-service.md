## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table to read severity, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. This method encapsulates the database aggregation logic so the endpoint handler remains thin.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
The service method should be added to the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the patterns already established there for `fetch` and `list` methods.

1. **Query construction**: Use SeaORM's `Select` builder with `entity::sbom_advisory::Entity::find()` to query the join table defined in `entity/src/sbom_advisory.rs`. Join to `entity::advisory::Entity` (defined in `entity/src/advisory.rs`) to access the severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.

2. **Deduplication**: Apply `.group_by(advisory::Column::Id)` before counting to ensure each advisory is counted only once, as the requirement specifies unique advisory deduplication.

3. **SBOM existence check**: Before running the aggregation query, verify the SBOM exists using the existing fetch pattern in `SbomService`. Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID is not found, consistent with other SBOM endpoints.

4. **Threshold filtering**: If the `threshold` parameter is provided (e.g., `"critical"`), filter the query to include only advisories at or above that severity level. Map severity strings to an ordering (critical=4, high=3, medium=2, low=1) and apply a `WHERE severity_rank >= threshold_rank` condition.

5. **Aggregation**: Use `COUNT(*)` with `CASE WHEN severity = 'critical' THEN 1 END` style conditional aggregation to compute all counts in a single query, following query patterns from `common/src/db/query.rs`.

6. **Error handling**: Wrap all database errors with `.context()` to produce `AppError` responses, matching the error handling convention in `common/src/error.rs`.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service layer scope.

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method supports optional threshold parameter for filtering by minimum severity
- [ ] All counts are computed in a single database query (no N+1)
- [ ] Crate compiles without errors

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

[sdlc-workflow] Description digest: sha256-md:09c069be186a1ea2df17b6b4ae30b59d76bd7a6630f0ca4ea99341b94c3dffbf
