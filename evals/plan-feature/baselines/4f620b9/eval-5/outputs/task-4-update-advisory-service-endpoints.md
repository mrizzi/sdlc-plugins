# Task 4 — Update advisory service and endpoints to use enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join overhead and simplifies all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from all advisory queries (fetch, list, search); query `advisory.status` enum column directly; update status filtering to use enum comparison (`WHERE status = 'Fixed'`) instead of join-based filtering
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the status field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source the status field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/mod.rs` — update module re-exports if the status type changes
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list handler to use the new service query pattern for status filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get handler to use the new service query returning enum status

## Implementation Notes
- The key change in `advisory.rs` service is replacing `join(advisory_status)` calls with direct column access on `advisory.status`. SeaORM queries will use the `AdvisoryStatusEnum` type defined in the entity crate.
- Status filtering in list queries should use `Column::Status.eq(AdvisoryStatusEnum::Fixed)` or equivalent SeaORM enum column filtering.
- The `AdvisorySummary` and `AdvisoryDetails` structs likely have a `status: String` field — this can remain as `String` if the enum's `Display` impl provides the string representation, or change to use the `AdvisoryStatusEnum` type directly for stronger typing.
- Ensure `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` continues to work with the updated summary struct.
- Shared query helpers in `common/src/db/query.rs` may be used for filtering and pagination — verify compatibility with enum column filtering.
- Error handling: all handlers must continue returning `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention.
- Per docs/constraints.md §5 (Code Change Rules): inspect each file before modifying; follow existing patterns in the service and endpoint layers.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that should be reused for enum-based status filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints
- `common/src/error.rs` — `AppError` enum for consistent error handling pattern
- `modules/fundamental/src/sbom/service/sbom.rs` — reference service implementation demonstrating query patterns without join-based lookups

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` use the `status` enum column directly — no joins to `advisory_status`
- [ ] Advisory list endpoint supports status filtering via the enum column
- [ ] Advisory get endpoint returns the status from the enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly represent the enum status
- [ ] No references to `advisory_status` table remain in the advisory module
- [ ] All advisory endpoints return the same response shape (status as a string) for API backward compatibility

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by status
- [ ] Verify advisory get endpoint returns the correct enum status value
- [ ] Verify that the response shape has not changed (status field is still a string in JSON)
- [ ] Verify compilation: `cargo check -p fundamental`

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles cleanly
- `cargo test -p fundamental` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:98fdba1a5fbd9d2be8540def15df9cf79809718da9f5fab15e16e2dae6011997
