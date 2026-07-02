# Task 4 — Update advisory service, model, and endpoints for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and REST endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. The external API response shape remains unchanged — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the enum column instead of a joined field
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update module-level type re-exports if they reference the status join
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` table join from all queries; use `advisory::Column::Status` for filtering and selection
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against the enum column directly
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single-advisory fetch to read status from enum column

## Implementation Notes
- In `AdvisoryService`, replace all `.join(advisory_status)` calls with direct column access on `advisory::Column::Status`. The status filter should use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on `advisory_status::Column::Name`.
- The `AdvisorySummary` and `AdvisoryDetails` structs should read `status` as a `String` (serialized from the enum) or as `AdvisoryStatusEnum` and convert to string for the API response. The response shape must remain identical — `status` is still a string field in JSON.
- Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's domain module structure scope.
- Per CONVENTIONS.md §Error handling: all endpoint handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response types: the list endpoint must continue to return `PaginatedResults<AdvisorySummary>`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination — do not implement custom filtering logic.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query helper scope.
- Follow the patterns established in the SBOM service layer (`modules/fundamental/src/sbom/service/sbom.rs`) for how entity queries are structured without joins.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the pattern for querying entities without joins, including pagination and filtering
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — shows model struct pattern for mapping entity fields to API response fields
- `modules/fundamental/src/sbom/endpoints/list.rs` — list endpoint pattern with `PaginatedResults<T>` return type and filter parameter handling
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that should be reused in the updated advisory queries

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns status as a string from the enum column
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns status from the enum column
- [ ] Status filtering on the list endpoint works correctly with enum values (`?status=Fixed`)
- [ ] The API response shape is unchanged — no breaking changes to consumers
- [ ] The advisory module compiles without errors (`cargo check -p fundamental`)

## Test Requirements
- [ ] Verify the list endpoint returns correct status values from the enum column
- [ ] Verify status filtering works for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify the detail endpoint returns the correct status for a single advisory
- [ ] Verify the API response JSON shape is identical to the previous format

## Verification Commands
- `cargo check -p fundamental` — compiles without errors
- `cargo test -p fundamental` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
