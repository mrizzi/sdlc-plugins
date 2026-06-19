# Task 4 — Update advisory service and endpoints to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, reducing the advisory list endpoint p95 latency by approximately 40ms. The advisory model structs (summary and details) must also be updated to use the enum type.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` table joins from all advisory queries (fetch, list, search); use `advisory.status` column directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to use `AdvisoryStatusEnum` or its string representation for the status field
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` or its string representation for the status field
- `modules/fundamental/src/advisory/model/mod.rs` — Update module-level type re-exports if needed
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter handling in the list endpoint to filter by enum value instead of join
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update advisory detail retrieval if it references the status join

## Implementation Notes
- The `AdvisoryService` in `advisory.rs` currently joins `advisory_status` to fetch/display the status name. Replace all such joins with direct reads of `advisory.status`
- For the list endpoint's status filter: change from joining `advisory_status` and filtering by `advisory_status.name` to filtering directly with `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` (or equivalent)
- Use SeaORM's built-in enum filtering — `Column::Status.eq(enum_value)` should work with `DeriveActiveEnum`
- The query builder helpers in `common/src/db/query.rs` may need inspection to ensure they support enum column filtering; if filtering is done at a higher level, update accordingly
- Ensure the API response shape remains identical — the status field should still serialize to a string (e.g., `"Fixed"`, `"New"`). Use serde `rename` or `to_string()` if needed to maintain backward compatibility
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` — maintain this pattern
- Per docs/constraints.md §5.2: inspect existing service and endpoint code before modifying
- Per docs/constraints.md §5.4: reuse existing query helpers rather than duplicating logic
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; verify enum column compatibility
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `common/src/error.rs` — `AppError` enum and `IntoResponse` implementation for error handling
- `modules/fundamental/src/sbom/service/sbom.rs` — Sibling service implementation demonstrating query patterns without status joins (reference pattern for clean queries)
- `modules/fundamental/src/sbom/endpoints/list.rs` — Sibling list endpoint demonstrating filtering and pagination patterns

## Acceptance Criteria
- [ ] All advisory queries no longer join `advisory_status` table
- [ ] Advisory list endpoint filters by `status` enum column directly
- [ ] Advisory detail endpoint reads `status` from enum column
- [ ] API response shape is unchanged — status is still returned as a string
- [ ] No performance regression — join elimination should reduce p95 latency

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by status
- [ ] Advisory detail endpoint returns correct status value
- [ ] All existing advisory endpoint tests pass after refactor (tests in `tests/api/advisory.rs`)

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles cleanly
- `cargo test -p tests --test advisory` — advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
