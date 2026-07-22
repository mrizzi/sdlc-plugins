# Task 4 -- Update advisory service and endpoints to use enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. Update the model structs (`AdvisorySummary`, `AdvisoryDetails`) to carry the enum value, and update the list and get endpoints to filter by the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/mod.rs` -- update any re-exports or type aliases related to status
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` join from all queries; use `advisory::Column::Status` for filtering and selection; update query builder calls to filter on the enum column directly
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory fetch to use the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if filter parameter types change

## Implementation Notes
- In `AdvisoryService`, replace all instances of `.join(advisory_status::Entity)` or equivalent with direct column access on `advisory::Column::Status`.
- For filtering, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table.
- The response shape to the frontend must remain identical -- status should still serialize as a string (e.g., "New", "Fixed"). SeaORM's `DeriveActiveEnum` with `string_value` attributes handles this automatically when the enum is serialized with serde.
- Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` for list and fetch operations as a reference for how services interact with entities.
- Use the shared query helpers in `common/src/db/query.rs` for pagination and filtering -- check if any status-specific filtering logic exists there and update it.
- The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` should continue to work without changes since it is generic over the item type.

Per CONVENTIONS.md &sect;Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping for error-producing operations.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service/endpoint scope.

Per CONVENTIONS.md &sect;Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint scope.

Per CONVENTIONS.md &sect;Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` for query construction.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service scope.

Per CONVENTIONS.md &sect;Module Pattern: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task modifies `modules/fundamental/src/advisory/model/`, `modules/fundamental/src/advisory/service/`, and `modules/fundamental/src/advisory/endpoints/` matching the convention's module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference service pattern for entity queries without joins
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper (no changes needed, but verify compatibility)
- `common/src/error.rs` -- `AppError` enum implementing `IntoResponse` for error handling

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint correctly filters by enum status values
- [ ] Advisory responses still include status as a string field (no API shape change)
- [ ] The advisory list endpoint compiles and serves requests successfully
- [ ] The `advisory_status` join is completely eliminated from the advisory module

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results with status filter applied
- [ ] Verify advisory get endpoint returns the correct status value
- [ ] Verify that no query in the advisory module references `advisory_status`

## Verification Commands
- `cargo check -p fundamental` -- module compiles without errors
- `cargo test -p fundamental -- advisory` -- advisory-related tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
