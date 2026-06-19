## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the schema change from lookup-table-based status to enum-column-based status. Remove any test setup that inserts rows into the `advisory_status` table, update test data creation to use enum values directly, and verify that all advisory endpoint tests pass with the new schema.

## Files to Modify
- `tests/api/advisory.rs` -- Update test setup to use `AdvisoryStatusEnum` values instead of `advisory_status` table inserts; update assertions to verify enum-based status values in responses; add new test cases for status filtering with enum values

## Implementation Notes
- Follow the existing test pattern in `tests/api/advisory.rs` for endpoint integration tests using a real PostgreSQL test database
- Test setup currently likely inserts rows into `advisory_status` and uses the returned IDs when creating test advisory records -- replace with direct enum column values
- Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in the test suite
- Ensure test data covers all four status values (New, Analyzing, Fixed, Rejected)
- Verify that the search endpoint (`tests/api/search.rs`) does not contain advisory-status-specific test logic; if it does, update accordingly

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Test coverage includes all four status enum values
- [ ] Status filtering tests verify correct behavior with enum values

## Test Requirements
- [ ] `tests/api/advisory.rs` -- all existing advisory tests updated and passing
- [ ] Add test: list advisories filtered by each status enum value
- [ ] Add test: create advisory with enum status and verify it appears in list results
- [ ] Verify `tests/api/search.rs` still passes (advisory search with new schema)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints
- Depends on: Task 5 -- Update ingestion pipeline
