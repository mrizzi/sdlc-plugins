## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` table. This eliminates the join overhead from all advisory queries, reducing p95 latency on the advisory list endpoint. Update the `AdvisorySummary` and `AdvisoryDetails` model structs to use the enum type for the status field. Update query builders in the service to filter by the enum column directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` joins from queries (fetch, list, search); use `advisory::Column::Status` directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use the `AdvisoryStatusEnum` type (or its string representation) for the status field instead of joining from the lookup table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum status field
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list endpoint handler to filter by enum column; remove any status join logic
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get endpoint handler to read status from the enum column directly

## Implementation Notes
Follow the existing query patterns in `modules/fundamental/src/advisory/service/advisory.rs` for building SeaORM queries. The key change is removing `.join(advisory_status)` calls and replacing `.column(advisory_status::Column::Value)` selections with `.column(advisory::Column::Status)`.

For filtering, replace status filter logic that matches against `advisory_status.value` with direct enum column filtering:
```rust
query = query.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed));
```

Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting — these should not need changes since the status column is now directly on the advisory table.

The response shape for API consumers must remain identical — status is still returned as a string value. Use SeaORM's enum serialization or manually convert the enum to its string representation in the model mapping.

Follow the error handling pattern using `Result<T, AppError>` with `.context()` wrapping as used throughout the advisory module.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs` — existing query patterns for advisory list/fetch/search
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns without joins to lookup tables

## Acceptance Criteria
- [ ] All advisory queries (list, fetch, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint filters by `advisory::Column::Status` directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs use the enum type for status
- [ ] API response shape for advisory endpoints is unchanged — status is still a string
- [ ] No references to `advisory_status` entity remain in the advisory module
- [ ] Code compiles with `cargo check -p fundamental`

## Test Requirements
- [ ] `cargo check -p fundamental` passes with no errors
- [ ] Advisory list endpoint returns correct status values as strings
- [ ] Advisory list endpoint correctly filters by status enum values
- [ ] Advisory get endpoint returns the correct status for a specific advisory

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
