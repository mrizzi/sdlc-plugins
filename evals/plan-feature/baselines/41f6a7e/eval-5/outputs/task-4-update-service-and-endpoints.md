# Task 4 — Update advisory service and endpoints to use enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly on the `advisory` table, eliminating all joins to the now-removed `advisory_status` lookup table. This includes updating the model structs (`AdvisorySummary`, `AdvisoryDetails`), the `AdvisoryService` query logic, and the list/get endpoint handlers.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use the `AdvisoryStatusEnum` directly instead of a status field populated via join
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly
- `modules/fundamental/src/advisory/model/mod.rs` — update any model re-exports or helper functions related to status mapping
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` joins from queries; use `advisory::Column::Status` for filtering and selection; update `fetch`, `list`, and `search` methods
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list handler to filter by `advisory::Column::Status` enum value directly (e.g., `WHERE status = 'Fixed'`) instead of joining `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get handler to select `status` directly from `advisory` without joining
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any query parameter types change for status filtering

## Implementation Notes
- The `AdvisoryService` methods currently join `advisory_status` to resolve the status string. After this change, the status is directly available as an enum column on `advisory` — no join needed.
- For status filtering in the list endpoint, use SeaORM's `column.eq(AdvisoryStatusEnum::Fixed)` pattern instead of the previous `advisory_status::Column::Name.eq("Fixed")` join-based filter.
- The response shape to API consumers must remain identical — status is still serialized as a string (e.g., "New", "Fixed"). Use `serde(rename_all = ...)` or explicit `Serialize` implementation on `AdvisoryStatusEnum` to ensure the enum serializes to the same string format as before.
- Reference the query builder helpers in `common/src/db/query.rs` — if there are advisory-specific filtering helpers that reference the old join, update them too.
- Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` for how the project structures SeaORM queries in service methods.
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure and `PaginatedResults<T>` usage from `common/src/model/paginated.rs`.
- Per docs/constraints.md §5.4: reuse existing query helpers from `common/src/db/query.rs` for pagination and sorting rather than implementing new logic.
- Per docs/constraints.md §5.8: compare the updated advisory endpoints against the sibling SBOM and package endpoints for parity on error handling, response wrapping, and logging.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse these rather than writing advisory-specific query logic
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by all list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for SeaORM query construction patterns in service methods
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler structure

## Acceptance Criteria
- [ ] All advisory queries use `advisory::Column::Status` directly — no joins to `advisory_status` remain anywhere in the codebase
- [ ] The advisory list endpoint supports filtering by status using the enum column (e.g., `?status=Fixed`)
- [ ] The advisory get endpoint returns the status as a string in the response without any join
- [ ] The API response shape is unchanged — status is still a string field in the JSON response
- [ ] The advisory list endpoint p95 latency is reduced by eliminating the join (measurable in production, verified structurally by confirming no join exists)
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify the module compiles: `cargo check -p fundamental`
- [ ] Integration tests for advisory list and get endpoints pass (covered by Task 6)

## Verification Commands
- `cargo check -p fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
