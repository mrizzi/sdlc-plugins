# Task 5 — Update advisory endpoints to filter by enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory list and get endpoints to use the new enum-based status filtering instead of the join-based approach. The endpoint handlers must pass enum values to the updated service layer and ensure the API response shape remains unchanged for consumers.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the query parameter parsing for status filter to convert string input to `AdvisoryStatusEnum` values; pass enum values to the updated `AdvisoryService::list` method
- `modules/fundamental/src/advisory/endpoints/get.rs` — update any status-related logic in the get endpoint to use the enum field directly
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any route definitions reference the old status query parameter type or join-based filter configuration

## Implementation Notes
- The list endpoint (`GET /api/v2/advisory`) likely accepts a `status` query parameter as a string. Update the handler to parse this string into an `AdvisoryStatusEnum` value before passing it to the service layer. Return a 400 Bad Request if the provided status string does not match any enum variant.
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for the established query parameter handling and response wrapping approach.
- The response must continue to use `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` — only the internal query mechanism changes, not the response wrapper.
- All handlers return `Result<T, AppError>` with `.context()` wrapping — maintain this error handling pattern.
- Verify that the status filter works with the shared filtering helpers in `common/src/db/query.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint for query parameter handling, pagination, and response wrapping
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used for list endpoint responses
- `common/src/error.rs` — `AppError` enum for error handling in endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` supports filtering by status using the enum column (no join to advisory_status)
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed
- [ ] Invalid status filter values return a 400 Bad Request with a descriptive error message
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with the status field populated from the enum column
- [ ] API response shape is identical to the previous implementation — no breaking changes for consumers

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` returns filtered results correctly
- [ ] Integration test: `GET /api/v2/advisory?status=InvalidValue` returns 400 Bad Request
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns advisory with correct status string

## Verification Commands
- `cargo check -p modules-fundamental` — module compiles
- `cargo test -p modules-fundamental -- advisory::endpoints` — endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and models to use enum status
