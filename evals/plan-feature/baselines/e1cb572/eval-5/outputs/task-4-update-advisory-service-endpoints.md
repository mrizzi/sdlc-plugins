# Task 4 — Update advisory service and endpoints to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. Update the model structs (`AdvisorySummary`, `AdvisoryDetails`) to carry the enum value, and update the list and get endpoints to filter by the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` join from all queries (fetch, list, search); use `advisory::Column::Status` for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` instead of a joined status string
- `modules/fundamental/src/advisory/model/mod.rs` -- update any re-exports or type aliases related to status
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory fetch to use the enum column

## Implementation Notes
In `modules/fundamental/src/advisory/service/advisory.rs`, replace all instances of `.join()` or `.find_also_related()` calls against the `advisory_status` entity with direct column access:

Before (conceptual):
```rust
Advisory::find()
    .find_also_related(AdvisoryStatus)
    .filter(advisory_status::Column::Name.eq(status_filter))
```

After:
```rust
Advisory::find()
    .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
```

For the model structs in `modules/fundamental/src/advisory/model/summary.rs` and `details.rs`, the status field should be typed as `AdvisoryStatusEnum` internally. The serialization to string in API responses should happen automatically via SeaORM's `DeriveActiveEnum` with `string_value` attributes and serde -- the response shape to the frontend must remain identical.

Use the shared query helpers in `common/src/db/query.rs` for filtering and pagination. The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` continues to work without changes since it is generic.

Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` for list and fetch operations as a reference for how services interact with entities.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's handler scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint scope.

Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query scope.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- reference service pattern for entity queries without joins
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper (no changes needed, verify compatibility)
- `common/src/error.rs` -- `AppError` enum for error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint correctly filters by enum status values
- [ ] `AdvisorySummary` and `AdvisoryDetails` read status from `advisory.status` enum column
- [ ] Advisory responses still include status as a string field (no API shape change)
- [ ] All handlers continue to return `Result<T, AppError>`
- [ ] The advisory module compiles and serves requests successfully

## Test Requirements
- [ ] Advisory list endpoint returns correct results with status filter applied
- [ ] Advisory get endpoint returns the correct status value
- [ ] Verify that no query in the advisory module references `advisory_status`
- [ ] Response JSON shape matches the pre-migration format (backward compatibility)

## Verification Commands
- `cargo check -p fundamental` -- module compiles without errors
- `cargo test -p fundamental -- advisory` -- advisory-related tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

`[sdlc-workflow] Description digest: sha256-md:e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6`
