## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. Update the AdvisorySummary and AdvisoryDetails model structs to source status from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` table join from fetch, list, and search queries; query the `status` enum column directly; update any status filtering logic to compare against `AdvisoryStatusEnum` values
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate the status field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate the status field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list handler to use the new status field for filtering (e.g., `WHERE status = 'Fixed'` instead of joining)
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get handler to read status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update model module if it re-exports advisory_status types

## Implementation Notes
Follow the existing query pattern in `common/src/db/query.rs` for building filtered queries with pagination and sorting. The status filter should use a direct column comparison (`advisory::Column::Status.eq(value)`) instead of a join-based filter.

Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct field mapping from query results.

Ensure the API response shape remains identical — the status field should still be serialized as a string (e.g., `"Fixed"`, `"New"`). The change is internal to the query layer; the external API contract does not change.

Use `Result<T, AppError>` with `.context()` wrapping for error handling, following the pattern established in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting that should be reused for the updated advisory queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs` — example service implementation showing query patterns without complex joins

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) no longer join the `advisory_status` table
- [ ] Status filtering in the list endpoint uses direct column comparison on the `status` enum column
- [ ] AdvisorySummary and AdvisoryDetails structs source status from the enum column
- [ ] API response shape for advisory endpoints remains unchanged (status is still a string)
- [ ] No references to `advisory_status` entity remain in the advisory module

## Test Requirements
- [ ] Advisory list endpoint returns correct results with status filter applied
- [ ] Advisory get endpoint returns the correct status value from the enum column
- [ ] Advisory search returns results with correct status values
- [ ] Status filtering works for all four enum values (New, Analyzing, Fixed, Rejected)

## Verification Commands
- `cargo check -p fundamental` — module compiles cleanly
- `cargo test -p fundamental` — existing tests pass with the updated queries

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:e525afe8d3931e5dba894211901014d840ad8f847d936092baa057fb65f823d9
