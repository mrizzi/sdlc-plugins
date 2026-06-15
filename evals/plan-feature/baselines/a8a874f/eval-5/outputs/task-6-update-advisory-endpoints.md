# Task 6: Update advisory endpoints and integration tests

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory REST endpoints to work with the new enum-based status field and update all integration tests to verify the endpoints function correctly with the migrated schema. The endpoint handlers should not need significant changes since the service layer (updated in Task 4) abstracts the data access, but any direct entity references or status-specific query parameter handling in the endpoint layer must be updated. The integration tests must verify end-to-end correctness.

## Acceptance Criteria

- `GET /api/v2/advisory` returns advisory list with correct status values from the enum column
- `GET /api/v2/advisory/{id}` returns advisory details with correct status value
- Status filter query parameter on the list endpoint works correctly with enum values
- All existing advisory integration tests pass with the new schema
- No references to `advisory_status` entity remain in the endpoint code

## Test Requirements

- Update `tests/api/advisory.rs` integration tests to verify:
  - Advisory list endpoint returns status as a string (New, Analyzing, Fixed, Rejected)
  - Status filtering works correctly (e.g., `?status=Fixed` returns only fixed advisories)
  - Advisory detail endpoint includes the correct status value
- Add a test that verifies the response shape has not changed (status is still a string field in the JSON response)

## Files to Modify

- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling if it references the old lookup table or `status_id`
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update if there are direct entity references to `advisory_status`
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if status-related routes reference old types
- `tests/api/advisory.rs` -- update integration tests to reflect the new schema; remove any test setup that creates `advisory_status` rows

## Implementation Notes

- The endpoint handlers in `modules/fundamental/src/advisory/endpoints/` likely delegate to `AdvisoryService` methods, so most changes should be minimal if Task 4 is complete
- The status filter query parameter may need to deserialize directly to `AdvisoryStatusEnum` instead of an integer `status_id`
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` for reference
- Integration tests in `tests/api/advisory.rs` may have test fixtures that insert into `advisory_status` -- these must be updated to use the enum column directly
- All handlers should continue to return `Result<T, AppError>` as per project conventions

## Dependencies

- Task 1: Create feature branch TC-9005 from main
- Task 4: Update advisory service and model to use enum status
- Task 5: Update advisory ingestion pipeline to write enum values directly

[Description digest: sha256-md:f8d6c2b3a7e49d1b56kb3f9c2a8d7e645b1c3d9f0a2b5c6d7e8f9a0b1c2d3e45 would be posted as a comment]
