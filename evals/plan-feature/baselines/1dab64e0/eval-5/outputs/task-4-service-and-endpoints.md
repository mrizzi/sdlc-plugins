## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model types, and HTTP endpoints to use the new `status` enum column instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, simplifying the query logic and reducing latency on the advisory list endpoint. The advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) must map the enum value directly. The list endpoint's status filter must use `WHERE status = '<value>'` instead of joining the lookup table.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — replace the status field type from a joined lookup value to the `AdvisoryStatusEnum` (or its string representation); remove any status-related join mapping
- `modules/fundamental/src/advisory/model/details.rs` — replace the status field mapping from a joined lookup value to the direct enum column
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` table join from `fetch`, `list`, and `search` queries; filter by `advisory::Column::Status` directly using the enum value
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filtering to use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining the lookup table
- `modules/fundamental/src/advisory/endpoints/get.rs` — update status field mapping in the response to use the direct enum value
- `modules/fundamental/src/advisory/endpoints/mod.rs` — verify route registration is unaffected (no changes expected, but confirm)

## Implementation Notes
Remove all `advisory_status` table joins from the advisory service queries. The `AdvisoryService::list` method currently joins `advisory_status` to resolve the status name; replace this with a direct column select on `advisory::Column::Status`.

For status filtering in the list endpoint, use SeaORM's `ColumnTrait::eq` with the `AdvisoryStatusEnum` variant:
```rust
query = query.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed));
```

The `AdvisorySummary` and `AdvisoryDetails` structs should serialize the enum value as a string in the JSON response to maintain backward compatibility with the frontend (the response shape must remain identical per the customer considerations).

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error-producing operations in service and endpoint methods.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` for query construction.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use these instead of building custom query logic
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for service query patterns without lookup table joins
- `common/src/error.rs` — `AppError` enum implementing `IntoResponse` for error handling

## Acceptance Criteria
- [ ] All advisory queries (`fetch`, `list`, `search`) no longer join the `advisory_status` table
- [ ] The advisory list endpoint filters by status using the direct enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` serialize the status as a string in the JSON response
- [ ] The response shape of all advisory endpoints remains identical (no breaking API changes)
- [ ] Status filtering on the advisory list endpoint produces correct results for all four enum values

## Test Requirements
- [ ] Advisory list endpoint returns advisories filtered by each status value (`New`, `Analyzing`, `Fixed`, `Rejected`)
- [ ] Advisory detail endpoint returns the correct status string for an advisory
- [ ] Advisory list endpoint with no status filter returns all advisories regardless of status
- [ ] Response JSON shape matches the previous format (status is a string, not an object)

## Verification Commands
- `cargo build -p fundamental` — fundamental module compiles without errors
- `cargo test -p fundamental` — module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
