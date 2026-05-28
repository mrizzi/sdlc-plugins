## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that was adding ~40ms to the advisory list endpoint p95 latency. The advisory list and get endpoints, the advisory service, and the advisory model structs all need to be updated to work with the enum field.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to use the `AdvisoryStatusEnum` type directly for the status field instead of a joined string value
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct to use the `AdvisoryStatusEnum` type directly for the status field
- `modules/fundamental/src/advisory/model/mod.rs` — Update any shared model type definitions or re-exports related to status
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove all `advisory_status` table joins from advisory queries; query the `status` enum column directly; update status filtering to use `WHERE status = <enum_value>` instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update the list endpoint handler to pass enum-based status filter parameters to the service layer
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update the get endpoint handler to map the enum status field to the response
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if any query parameter types changed for status filtering

## Implementation Notes
- The response shape must remain identical to the current API — status is still serialized as a string in JSON responses. Use serde's `rename_all` or explicit `#[serde(rename = "...")]` attributes on the enum variants if needed to preserve the existing casing.
- Remove all `.join()` or `.find_also_related(advisory_status::Entity)` calls in the service layer. Replace with direct column access on the advisory entity.
- For status filtering in the list endpoint, change from joining the lookup table and filtering on `advisory_status.name` to filtering directly with `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` (or whichever variant).
- Follow the existing query builder pattern in `common/src/db/query.rs` for filtering and pagination. The SBOM service (`modules/fundamental/src/sbom/service/sbom.rs`) demonstrates the standard query pattern without a status join.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — Demonstrates the service query pattern (fetch, list, search) without a status join — use as reference for the simplified advisory queries
- `modules/fundamental/src/sbom/model/summary.rs` — Shows the model struct pattern with serde derives for JSON serialization
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns results without joining the `advisory_status` table
- [ ] Advisory get endpoint (`GET /api/v2/advisory/{id}`) returns the status field from the enum column directly
- [ ] Status filtering on the list endpoint works with enum values (e.g., `?status=Fixed`)
- [ ] The JSON response shape is unchanged — status is still a string field in the response body
- [ ] No references to `advisory_status` entity remain in the advisory module

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from the enum column
- [ ] Verify advisory list endpoint supports status filtering with enum values
- [ ] Verify advisory get endpoint returns correct status for a single advisory
- [ ] Verify the response JSON shape is unchanged (backward compatibility)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
