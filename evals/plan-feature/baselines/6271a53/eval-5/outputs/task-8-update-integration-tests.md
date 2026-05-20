## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based schema. Remove any test setup code that inserts into the `advisory_status` lookup table. Update test assertions and fixtures to use enum status values directly. Ensure all existing test scenarios continue to pass with the new schema.

## Files to Modify
- `tests/api/advisory.rs` -- Update all advisory integration tests: remove advisory_status table setup/fixtures; update advisory creation to use enum status values; update status filter assertions to use string enum values instead of status IDs; verify response shape is unchanged

## Implementation Notes
- Integration tests in `tests/api/` hit a real PostgreSQL test database per the project conventions
- Test setup code likely inserts rows into `advisory_status` before creating advisories. Remove this setup -- the enum type is created by the migration and does not need runtime seeding
- Update advisory insertion in tests to set `status: AdvisoryStatusEnum::New` (or equivalent) instead of `status_id: 1`
- Update filter test cases: if tests filter by `status_id=1`, change to filter by `status=New`
- Follow the existing test pattern: `assert_eq!(resp.status(), StatusCode::OK)` style assertions
- Verify that the response body still contains the status as a string (e.g., `"status": "New"`) -- this should not change
- Reference the test patterns in `tests/api/sbom.rs` for integration test structure

## Reuse Candidates
- `tests/api/sbom.rs` -- Reference for integration test structure and assertion patterns
- `tests/api/advisory.rs` -- The existing advisory tests to update (understand current patterns before modifying)

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Advisory creation in tests uses enum status values
- [ ] Status filter tests use string enum values
- [ ] Response shape assertions confirm backward compatibility

## Test Requirements
- [ ] Run full advisory integration test suite and verify all tests pass
- [ ] Verify status filtering tests cover all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Verify advisory list test returns correct status strings in response body

## Verification Commands
- `cargo test -p tests --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 6 -- Update advisory endpoints for enum status
- Depends on: Task 7 -- Update advisory ingestion pipeline for enum status
