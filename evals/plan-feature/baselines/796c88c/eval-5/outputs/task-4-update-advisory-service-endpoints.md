## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column instead of the `status_id` foreign key join. Remove all joins to the now-dropped `advisory_status` table from query construction, filtering, and response mapping. Update the model structs to carry the enum value directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove `advisory_status` table joins from fetch, list, and search queries; filter and sort on `advisory.status` column directly
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string or status_id
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` for the status field
- `modules/fundamental/src/advisory/model/mod.rs` -- Update model module imports if needed
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filter parameter handling to use enum values instead of status_id
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update response construction to use the enum status field
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Update route registration if filter parameter types change
- `common/src/db/query.rs` -- Update shared query helpers if they contain advisory_status-specific join logic

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/advisory/service/advisory.rs` for query construction using SeaORM
- The `AdvisoryService::list` method likely constructs a query with `.join(advisory_status)` -- remove this join and select `advisory.status` directly
- Status filtering should use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` pattern instead of joining and filtering on the lookup table
- Response types (`AdvisorySummary`, `AdvisoryDetails`) should serialize the enum as a string to maintain API compatibility -- the response shape must remain identical per the feature requirements
- Use `common/src/db/query.rs` patterns for any shared filtering logic that references advisory status
- Error handling must continue to use `Result<T, AppError>` with `.context()` wrapping

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) use `advisory.status` column directly without joining `advisory_status`
- [ ] Status filtering works with enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response shape is unchanged -- status is still returned as a string
- [ ] No references to `advisory_status` table remain in the advisory module
- [ ] All handlers continue to return `Result<T, AppError>`

## Test Requirements
- [ ] Advisory list endpoint returns correct status values from the enum column
- [ ] Status filter query parameter correctly filters by enum value
- [ ] Advisory detail endpoint returns the correct status string
- [ ] Verify API response shape matches the pre-migration format

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update entity definitions
