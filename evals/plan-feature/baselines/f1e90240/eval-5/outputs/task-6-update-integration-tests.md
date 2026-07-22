# Task 6 -- Update advisory integration tests for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Tests that set up advisory fixtures must create advisories with enum status values directly, and test assertions on status filtering must use the enum values. Remove any test setup code that inserts rows into the now-dropped `advisory_status` table.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory test fixtures to use `AdvisoryStatusEnum` values instead of `advisory_status` table inserts; update status filter assertions to use enum string values; remove any test helpers that set up the `advisory_status` lookup table

## Implementation Notes
- Review each test function in `tests/api/advisory.rs` and identify:
  1. Test setup code that inserts into the `advisory_status` table -- replace with direct enum value assignment on the advisory entity
  2. Assertions that check status via a joined value -- update to check the enum string directly
  3. Filter parameters in test HTTP requests that reference status -- ensure they pass enum string values (e.g., `?status=Fixed`)
- Follow the existing test pattern in `tests/api/sbom.rs` for how integration tests set up fixtures and make assertions.
- Ensure test data covers all four status values (New, Analyzing, Fixed, Rejected) to validate the enum mapping is complete.

Per CONVENTIONS.md &sect;Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference integration test patterns for fixture setup and HTTP request assertions
- `tests/api/advisory.rs` -- existing advisory test code to modify in-place

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Test coverage includes filtering by each of the four status values
- [ ] Test fixtures create advisories with enum status values directly

## Test Requirements
- [ ] All existing advisory integration tests pass after modification
- [ ] Add or update test cases that filter by status to verify enum-based filtering works correctly
- [ ] Verify that tests covering advisory list with status filter (UC-1 from the feature) pass

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
