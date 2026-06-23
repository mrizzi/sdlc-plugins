# Task 6 — Update advisory integration tests for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Tests that set up advisory fixtures must create advisories with enum status values directly, and test assertions on status filtering must use the enum values. Remove any test setup code that inserts rows into the now-dropped `advisory_status` table.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory test fixtures to use `AdvisoryStatusEnum` values instead of `advisory_status` table inserts; update status filter assertions to use enum string values; remove any test helpers that set up the `advisory_status` lookup table

## Implementation Notes
Review each test function in `tests/api/advisory.rs` and identify:

1. Test setup code that inserts into the `advisory_status` table -- replace with direct enum value assignment on the advisory entity
2. Assertions that check status via a joined value -- update to check the enum string directly
3. Filter parameters in test HTTP requests that reference status -- ensure they pass enum string values (e.g., `?status=Fixed`)

Add or update these test scenarios:

1. **List with status filter**: Insert advisories with different statuses, filter by `?status=Fixed`, verify only matching advisories are returned
2. **Detail endpoint status**: Fetch a single advisory by ID, verify the `status` field in the JSON response is the correct string value
3. **All enum values**: Insert one advisory per status value (New, Analyzing, Fixed, Rejected), list all, verify each status appears correctly
4. **Backward compatibility**: Verify the response JSON structure has not changed -- `status` is a string field at the same path as before the migration

Follow the existing test patterns in `tests/api/sbom.rs` for test setup, HTTP request construction, and assertion patterns.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference integration test patterns for fixture setup and HTTP request assertions
- `tests/api/advisory.rs` -- existing advisory test code to modify in-place

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Test coverage includes filtering by each of the four status values
- [ ] Test fixtures create advisories with enum status values directly
- [ ] Tests confirm backward-compatible API response shape

## Test Requirements
- [ ] All existing advisory integration tests pass after modification
- [ ] Integration test verifying advisory list endpoint status filter returns only matching advisories
- [ ] Integration test verifying advisory detail endpoint returns the correct status string
- [ ] Tests covering advisory list with status filter (UC-1 from the feature) pass

## Verification Commands
- `cargo test --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status

`[sdlc-workflow] Description digest: sha256-md:b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0`
