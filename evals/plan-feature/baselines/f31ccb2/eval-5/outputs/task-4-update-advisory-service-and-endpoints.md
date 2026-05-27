## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoints to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that was adding ~40ms to the advisory list endpoint p95 latency. Update the AdvisorySummary and AdvisoryDetails model structs to source status from the enum column, update AdvisoryService query methods, and update the list and get endpoint handlers to filter by the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string; remove any status join mapping logic
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum column directly
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` table join from all query methods (fetch, list, search); update filter logic to use `WHERE status = 'value'` instead of joining
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filtering in the list endpoint to use the enum column directly
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to return status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any status-related query parameter types changed

## Implementation Notes
- The response shape must remain identical — status is still returned as a string in the API response. Use SeaORM's enum serialization or implement `Display`/`Serialize` for `AdvisoryStatusEnum` to maintain the same JSON output.
- In `AdvisoryService`, replace all `.join(advisory_status::Entity)` calls with direct column access on `advisory::Column::Status`. This is the core change that eliminates the join overhead.
- For status filtering in list queries, change from `advisory_status::Column::Name.eq(value)` to `advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(value))`. Consider adding a `FromStr` implementation on `AdvisoryStatusEnum` if one does not already exist.
- Follow the existing query patterns in `common/src/db/query.rs` for filtering and pagination. Check if the query builder helpers need updating to handle enum column filtering.
- Look at how the SBOM module's service (`modules/fundamental/src/sbom/service/sbom.rs`) handles field filtering for reference on the established query pattern.
- The `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` should continue to work unchanged since the response shape is not changing.
- All handlers should continue returning `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting — check if enum column filtering is already supported
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper, should work unchanged
- `common/src/error.rs` — `AppError` enum for error handling pattern
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns in this project

## Acceptance Criteria
- [ ] All advisory queries use the `status` enum column directly — no joins to `advisory_status`
- [ ] Advisory list endpoint supports status filtering via the enum column
- [ ] Advisory get endpoint returns status from the enum column
- [ ] API response shape is unchanged — status is still a string field in JSON responses
- [ ] `cargo check -p modules-fundamental` compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results with status filtering
- [ ] Verify advisory get endpoint returns the correct status string
- [ ] Verify that no query references the `advisory_status` table

## Verification Commands
- `cargo check -p modules-fundamental` — compiles without errors
- `cargo test -p tests --test advisory` — all advisory endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
