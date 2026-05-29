# Task 6 -- Update advisory integration tests for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where `advisory.status` is an enum column instead of a foreign key to the `advisory_status` lookup table. Test fixtures and assertions must use enum values directly. Add test coverage for status filtering via the enum column to verify the performance improvement (eliminated join) does not change behavior.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory endpoint integration tests: replace any test setup that inserts into `advisory_status` table with direct enum values; update assertions to verify status is returned as a string from the enum; add tests for status filtering via `?status=Fixed` query parameter

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs` for test structure and assertion style (e.g., `assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Test data setup must change: instead of inserting rows into `advisory_status` table and using `status_id` FK, insert advisories with the `status` enum value directly.
- Ensure tests cover all four enum variants: New, Analyzing, Fixed, Rejected.
- Add a dedicated test for the status filter query parameter on the list endpoint to verify that `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed.
- Verify that the response JSON shape is unchanged -- the `status` field should still serialize as a plain string (not a nested object).
- Reference the SBOM integration tests at `tests/api/sbom.rs` for endpoint test patterns including pagination and filtering.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test patterns (setup, request building, response assertions)
- `tests/api/advisory.rs` -- existing advisory tests to update (not rewrite from scratch)

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] Test coverage exists for all four status enum values (New, Analyzing, Fixed, Rejected)
- [ ] Status filtering test verifies correct behavior of `?status=<value>` query parameter
- [ ] Response shape assertions confirm status is serialized as a string
- [ ] No test references to `advisory_status` lookup table remain

## Test Requirements
- [ ] Test advisory list endpoint returns all advisories with correct status values
- [ ] Test advisory list endpoint filters by each status enum value correctly
- [ ] Test advisory get endpoint returns correct status for a single advisory
- [ ] Test advisory ingestion creates advisory with correct enum status
- [ ] All tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern per project convention

## Verification Commands
- `cargo test -p tests --test advisory` -- all advisory integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
