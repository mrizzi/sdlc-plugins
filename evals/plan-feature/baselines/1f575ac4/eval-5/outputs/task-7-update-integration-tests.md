# Task 7 — Update advisory integration tests for enum-based status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based status schema. Tests must no longer reference the `advisory_status` lookup table and must verify that status filtering, advisory retrieval, and advisory ingestion all work correctly with the enum column. This task ensures the test suite validates the complete migration from lookup table to enum column.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory endpoint integration tests: remove any test setup code that inserts rows into the `advisory_status` table; update test fixtures to create advisories with enum status values directly; update assertions to verify status is returned as the expected string; add tests for status filtering by enum value

## Implementation Notes
- Follow the existing test pattern in `tests/api/sbom.rs` for the established integration test structure in this project — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` patterns.
- Update test setup/fixture code: instead of inserting into `advisory_status` and creating advisories with `status_id`, create advisories directly with `status: AdvisoryStatusEnum::Fixed` (or similar).
- Test the complete user workflow from UC-1: create advisories with various statuses, filter by status via the API endpoint, verify the correct results are returned.
- Test the ingestion workflow from UC-2: ingest an advisory with a status, verify the stored advisory has the correct enum status value.
- Verify that the search module's integration with advisories (if any) still works — check `tests/api/search.rs` for any advisory-status-related search tests.
- Ensure no test references the `advisory_status` table or entity — grep the test file for `advisory_status` after changes.

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test file showing the established test patterns (test setup, API calls, assertions)
- `tests/api/search.rs` — check for any advisory-related search tests that may reference status

## Acceptance Criteria
- [ ] All advisory integration tests pass against the new enum-based schema
- [ ] No test references the `advisory_status` lookup table or entity
- [ ] Tests cover status filtering: querying advisories with `?status=Fixed` returns only fixed advisories
- [ ] Tests cover all four status enum values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the API response shape is unchanged (status is a string in JSON output)

## Test Requirements
- [ ] Integration test: create advisories with each status, list with status filter, verify correct filtering
- [ ] Integration test: create an advisory, retrieve by ID, verify status field is present and correct
- [ ] Integration test: verify advisory list without status filter returns all advisories with their statuses

## Verification Commands
- `cargo test -p tests -- advisory` — all advisory integration tests pass
- `cargo test -p tests` — full integration test suite passes (no regressions in search or other modules)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and models to use enum status
- Depends on: Task 5 — Update advisory endpoints to filter by enum status column
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum status directly
