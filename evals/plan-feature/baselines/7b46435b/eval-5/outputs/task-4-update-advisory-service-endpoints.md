## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to query the new status enum column directly instead of joining the advisory_status lookup table. This eliminates the join overhead that added ~40ms to advisory list endpoint p95 latency. The response shape remains identical — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove advisory_status table join from all query methods (fetch, list, search); filter by status enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update AdvisorySummary struct to source status from the enum column instead of a joined field
- `modules/fundamental/src/advisory/model/details.rs` — update AdvisoryDetails struct to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update any shared model imports or type aliases related to status
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against the enum column
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory retrieval to use enum column

## Implementation Notes
- Remove all `join(advisory_status)` or equivalent SeaORM `find_also_related(AdvisoryStatus)` calls from AdvisoryService methods in `modules/fundamental/src/advisory/service/advisory.rs`
- For status filtering, use `Column::Status.eq(AdvisoryStatus::Fixed)` pattern instead of joining and filtering on the related table
- Follow the query builder patterns in `common/src/db/query.rs` for filtering and pagination
- Return types remain `PaginatedResults<AdvisorySummary>` using the wrapper from `common/src/model/paginated.rs`
- Error handling must use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`
- The string representation of status in API responses must remain unchanged (New, Analyzing, Fixed, Rejected)

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper
- `common/src/error.rs` — AppError enum implementing IntoResponse

## Acceptance Criteria
- [ ] All advisory queries use the status enum column directly — no joins to advisory_status
- [ ] Advisory list endpoint supports filtering by status using the enum column
- [ ] Advisory detail endpoint returns the status from the enum column
- [ ] API response shape is unchanged — status is still a string value
- [ ] No remaining references to advisory_status entity in the fundamental module
- [ ] Module compiles without errors

## Test Requirements
- [ ] Advisory list with status filter returns correctly filtered results
- [ ] Advisory detail returns status as a string matching the enum value
- [ ] Advisory list without status filter returns all advisories with status populated

## Verification Commands
- `cargo build -p trustify-fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 3 — Update SeaORM entity definitions (service layer uses the updated entities)
