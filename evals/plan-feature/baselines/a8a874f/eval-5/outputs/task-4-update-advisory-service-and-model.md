# Task 4: Update advisory service and model to use enum status

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory service layer and model structs to use the new `status` enum column instead of joining the `advisory_status` table. The `AdvisoryService` must be updated to query the `status` column directly, removing all joins to the dropped lookup table. The `AdvisorySummary` and `AdvisoryDetails` model structs must be updated to source the status field from the enum column. The query helpers used for status filtering must be updated accordingly.

## Acceptance Criteria

- `AdvisoryService::list` and `AdvisoryService::fetch` no longer join the `advisory_status` table
- Status filtering in advisory list queries uses `WHERE advisory.status = 'value'` pattern instead of a join
- `AdvisorySummary` and `AdvisoryDetails` populate the status field from the enum column
- All existing service method signatures remain unchanged (no API contract change)
- The advisory list endpoint continues to support status-based filtering

## Test Requirements

- Unit test that `AdvisoryService::list` with a status filter returns only matching advisories
- Unit test that `AdvisoryService::fetch` returns the correct status value from the enum column
- Verify that the advisory list query no longer includes a JOIN to `advisory_status`

## Files to Modify

- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` join from all queries; filter on `advisory.status` column directly
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` to read status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` to read status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- update any status-related type re-exports if needed

## Implementation Notes

- The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` currently performs a join with `advisory_status` entity -- remove all references to this entity
- Use SeaORM's `Column::Status` enum variant for filtering instead of joining
- Follow the existing query builder pattern in `common/src/db/query.rs` for constructing filtered queries
- The response shape to the API consumer does not change; `AdvisorySummary.status` remains a string field but is now sourced from the enum column's string representation
- Check `modules/fundamental/src/sbom/service/sbom.rs` for the established service query pattern

## Dependencies

- Task 1: Create feature branch TC-9005 from main
- Task 3: Update SeaORM entity definitions for advisory status enum

[Description digest: sha256-md:d6b4a0f1e5c27b8934if1d7a0e6b5c423f9a1b7d8e0f3a4b5c6d7e8f9a0b1c23 would be posted as a comment]
