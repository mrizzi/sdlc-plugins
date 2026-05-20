## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory HTTP endpoints (list and get) to work with the new enum-based status column. The endpoint handlers should pass status filter parameters as enum values to the service layer instead of status IDs. The response shape remains unchanged -- status is still serialized as a string.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update status filter query parameter handling to accept and parse enum string values (e.g., `?status=Fixed`) instead of status IDs; pass enum values to the updated AdvisoryService
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update the get handler if it references status_id in any path parameter or response construction
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- Update route registration if query parameter types change for status filtering

## Implementation Notes
- The list endpoint likely accepts a status filter as a query parameter. If it previously accepted a numeric `status_id`, it should now accept the status string (e.g., `?status=Fixed`). If it already accepted a string and resolved it to an ID internally, simplify to pass the string directly as an enum value
- Follow the endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction and handler structure
- Use Axum's `Query` extractor for filter parameters -- define a query params struct that accepts `status: Option<AdvisoryStatusEnum>` or `status: Option<String>` depending on how filtering is implemented
- Response types should use `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` -- no change to response shape
- All handlers return `Result<T, AppError>` with `.context()` wrapping per project conventions
- No external API contract changes -- the response JSON shape is identical

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference for endpoint handler patterns and query parameter extraction
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Reference for get-by-ID handler patterns
- `common/src/model/paginated.rs` -- PaginatedResults wrapper used in list responses

## Acceptance Criteria
- [ ] Advisory list endpoint accepts status filter as a string matching enum values
- [ ] Advisory list endpoint returns filtered results using the enum column
- [ ] Advisory get endpoint returns the correct status from the enum column
- [ ] Response JSON shape is unchanged (backward compatible)
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Verify `GET /api/v2/advisory?status=Fixed` returns only advisories with Fixed status
- [ ] Verify `GET /api/v2/advisory/{id}` returns the correct enum status as a string
- [ ] Verify invalid status filter values return an appropriate error response

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 5 -- Update AdvisoryService to use enum status column
