# Task 7 -- Update integration tests for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema. Tests must seed advisory data using the enum column instead of the lookup table, verify that status filtering works against the enum column, and confirm that the API response shape is unchanged. Any test helpers that insert into the `advisory_status` table must be updated or removed.

## Files to Modify
- `tests/api/advisory.rs` -- Update all advisory integration tests: replace `advisory_status` table seeding with direct enum column values; update status filter assertions; verify response shape stability; add tests for the new enum-based filtering edge cases

## Implementation Notes
- In `tests/api/advisory.rs`, the existing tests likely seed test data by:
  1. Inserting rows into `advisory_status` table
  2. Inserting advisory rows with `status_id` foreign key references
  3. Querying the API and asserting on the response

  Replace this with:
  1. Insert advisory rows directly with `status: AdvisoryStatusEnum::New` (or other variants)
  2. Query the API and assert on the response

- Follow the existing test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:
  - Use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
  - Tests hit a real PostgreSQL test database
  - Use the project's test database setup/teardown utilities

- Verify the response JSON `status` field contains the expected string values (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`) -- the API contract must remain stable.

- Add test coverage for:
  - Listing advisories without status filter returns all statuses
  - Filtering by each valid status enum value returns correct results
  - Filtering by an invalid status string returns an error response
  - Single advisory GET returns the correct status string

- Remove any test helper functions that create `advisory_status` lookup table entries.

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references `advisory_status` table or entity
- [ ] Tests verify correct status string values in API responses for all four enum variants
- [ ] Tests cover status filter queries on the list endpoint
- [ ] Tests cover invalid status filter error handling
- [ ] `cargo test -p tests` passes with all advisory tests green

## Test Requirements
- [ ] Integration test: list advisories returns correct status strings for all four enum variants
- [ ] Integration test: filter by `status=New` returns only matching advisories
- [ ] Integration test: filter by `status=Rejected` returns only matching advisories
- [ ] Integration test: filter by invalid status returns error
- [ ] Integration test: single advisory GET returns correct status string
- [ ] All pre-existing advisory tests continue to pass (API contract stability)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and model layers
- Depends on: Task 5 -- Update advisory endpoints for enum status
- Depends on: Task 6 -- Update advisory ingestion pipeline for enum status
