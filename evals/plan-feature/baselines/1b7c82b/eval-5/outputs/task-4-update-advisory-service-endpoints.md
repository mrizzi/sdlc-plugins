# Task 4 — Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `advisory` table using the new `status` enum column directly, instead of joining the `advisory_status` lookup table. This eliminates the join overhead from all advisory queries and is expected to reduce advisory list endpoint p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove all joins to `advisory_status` table in fetch, list, and search methods; replace `status_id`-based filtering with direct `status` enum column filtering using `WHERE status = <AdvisoryStatusEnum>` conditions
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to populate the `status` field directly from the `advisory.status` enum column instead of from the joined `advisory_status` row
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly if it references status via the join
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update query parameter handling for status filtering to use enum values instead of status IDs
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update single-advisory fetch to use the enum column if it references the join
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if filter parameter types change

## Implementation Notes
- In `advisory.rs` service, replace any `join` or `find_related(advisory_status::Entity)` calls with direct column access on `advisory::Column::Status`
- For filtering, use SeaORM's `ColumnTrait::eq()` with `AdvisoryStatusEnum` values (e.g., `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)`)
- The response shape must remain identical — status is still serialized as a string in the API response. Use `serde(rename_all = "PascalCase")` or explicit `rename` on the enum variants if needed to match the current string format
- Follow the query patterns in `common/src/db/query.rs` for filtering and pagination — these shared helpers should still work with the new column type
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/` for reference on service-to-endpoint integration
- The `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` remains unchanged
- All handlers must continue to return `Result<T, AppError>` with `.context()` wrapping per the error handling pattern in `common/src/error.rs`
- Per docs/constraints.md: inspect existing code before modifying; keep changes scoped to listed files
- Per docs/constraints.md: commits must reference Jira issue ID, follow Conventional Commits, and include AI attribution trailer
- Per docs/constraints.md: PR must specify `--base TC-9005`

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; verify these work with enum column types
- `modules/fundamental/src/sbom/service/sbom.rs` — Reference for service method patterns (fetch, list) without join-based status lookup
- `modules/fundamental/src/advisory/service/advisory.rs` — Existing advisory service with current join logic to be refactored
- `common/src/model/paginated.rs` — PaginatedResults wrapper used by list endpoints

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) use the `status` enum column directly without joining `advisory_status`
- [ ] Status filtering on the list endpoint works with enum values (New, Analyzing, Fixed, Rejected)
- [ ] API response shape is unchanged — status is still returned as a string
- [ ] No references to `advisory_status` entity or `status_id` column remain in the advisory module
- [ ] All handlers continue to return `Result<T, AppError>` with proper error context

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by each status value
- [ ] Verify advisory get endpoint returns the correct status for a single advisory
- [ ] Verify API response format has not changed (status remains a string field)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
