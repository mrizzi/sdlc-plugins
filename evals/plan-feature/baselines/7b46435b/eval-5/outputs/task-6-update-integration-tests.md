## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify correct behavior with the new enum-based status column. Existing tests that reference the advisory_status table join or status_id column must be updated to work with the new schema. Add test coverage for status filtering using the enum column to confirm the p95 latency improvement path works correctly.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory endpoint tests to work with the enum status column; add tests for status enum filtering

## Implementation Notes
- Follow the existing test patterns in `tests/api/sbom.rs` for integration test structure — tests hit a real PostgreSQL test database
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status assertions
- Test that the advisory list endpoint's status filter parameter works with enum values (e.g., `?status=Fixed`)
- Verify that advisory responses contain status as a string field with valid enum values
- Remove any test setup code that inserts into the advisory_status lookup table — test data should use the enum column directly
- Ensure test fixtures create advisories with all four status values to verify completeness

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating the test structure and assertion patterns used in this project

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new schema
- [ ] Tests verify advisory list endpoint with status filter returns correct results
- [ ] Tests verify advisory detail endpoint returns status as a string
- [ ] No references to advisory_status table or status_id in test code
- [ ] Test suite compiles and passes: cargo test -p trustify-tests

## Test Requirements
- [ ] Test advisory list endpoint without filter returns advisories with status field populated
- [ ] Test advisory list endpoint with status=Fixed filter returns only fixed advisories
- [ ] Test advisory detail endpoint returns correct status value
- [ ] Test advisory ingestion end-to-end produces correct status enum value

## Verification Commands
- `cargo test -p trustify-tests` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 4 — Update advisory service and endpoints (tests verify endpoint behavior)
- Depends on: Task 5 — Update ingestion pipeline (tests verify ingestion behavior)
