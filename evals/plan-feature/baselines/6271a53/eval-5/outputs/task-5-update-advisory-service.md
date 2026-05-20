## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the `AdvisoryService` (fetch, list, search operations) to query the `status` enum column directly instead of joining the `advisory_status` lookup table. All advisory queries that previously required a JOIN to resolve status should now use a simple WHERE clause on the enum column. This eliminates the join overhead that added ~40ms to p95 latency on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove all joins to `advisory_status` table; update fetch, list, and search methods to filter/select using the `status` enum column directly
- `modules/fundamental/src/advisory/service/mod.rs` -- Update any service re-exports or shared query construction if they reference the old advisory_status join

## Implementation Notes
- The `AdvisoryService` methods (fetch, list, search) likely construct queries using SeaORM's `find()` with `.join()` or `.find_also_related()` to the `advisory_status` entity. Replace these with direct column access on `advisory::Column::Status`
- For list/search filtering by status, replace the join-based filter with a direct `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` style filter
- Follow the query patterns in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) as a reference for SeaORM query construction without unnecessary joins
- Use the shared query builder helpers in `common/src/db/query.rs` for filtering and pagination -- these may need minor updates if they have advisory-status-specific filter logic
- Ensure the service methods still return the same data shape (the model changes from Task 4 handle the struct mapping)
- Error handling should continue to use `Result<T, AppError>` with `.context()` wrapping per the project conventions

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- Reference for SeaORM query patterns without joins
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and pagination
- `common/src/error.rs` -- AppError enum and error handling patterns

## Acceptance Criteria
- [ ] All advisory service methods (fetch, list, search) query the `status` enum column directly
- [ ] No advisory service method joins the `advisory_status` table
- [ ] Status-based filtering uses the enum column with direct equality checks
- [ ] All existing advisory service functionality is preserved (no behavioral regression)
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list with status filter returns correct results using enum column
- [ ] Verify advisory fetch by ID returns correct status from enum column
- [ ] Verify advisory search with status criteria works without joins

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory model structs for enum status
