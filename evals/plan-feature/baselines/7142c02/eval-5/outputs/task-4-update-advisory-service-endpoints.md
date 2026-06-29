## Repository
trustify-backend

## Target Branch
TC-9005

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Update the advisory service layer, model structs, and API endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the status filtering logic. The API response shape remains unchanged — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to use enum status field instead of joined status
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct to use enum status field
- `modules/fundamental/src/advisory/model/mod.rs` — Update model module if it re-exports status-related types
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` join from fetch, list, and search queries; filter on `status` column directly
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter parameter handling to use enum comparison
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update single advisory fetch to use enum status

## Implementation Notes
- In `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`), remove all `JOIN advisory_status` clauses from queries. Replace `advisory_status.name` references with `advisory.status` direct column access
- For status filtering in list queries, change from `advisory_status.name = ?` (with join) to `advisory.status = ?::advisory_status_enum` (direct enum comparison)
- In `AdvisorySummary` and `AdvisoryDetails` model structs, replace any `status_name: String` field that was populated via join with a `status: AdvisoryStatusEnum` field, and implement `Display` or `Serialize` to return the string representation for API responses
- The API response shape must remain identical — the `status` field in JSON responses must still be a string (e.g., `"Fixed"`, `"New"`). Use serde serialization attributes to ensure the enum serializes as its string variant name
- Follow the existing query patterns in `common/src/db/query.rs` for filtering and pagination
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for list responses
- Follow the error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping, as defined in `common/src/error.rs`
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, sorting; reuse for advisory list queries without the join
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by advisory list endpoint
- `common/src/error.rs` — `AppError` enum with `IntoResponse` implementation; follow existing error handling patterns
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for service layer query patterns without complex joins

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Advisory list endpoint supports filtering by `status` enum column directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` use enum status field
- [ ] API response JSON shape is unchanged — `status` field is still a string
- [ ] Advisory list endpoint p95 latency is reduced (join eliminated)

## Test Requirements
- [ ] Advisory list query returns correct results with status filter using enum comparison
- [ ] Advisory detail fetch returns correct status as string in response
- [ ] Status filtering works for all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response shape validation — status field is a string, not an object

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:518f5dd664113a7c15160cc052db82d1617165443dd4cf6b6fe2f1654723363f
