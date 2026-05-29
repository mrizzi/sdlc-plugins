# Task 6 — Update advisory integration tests for enum-based status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. Tests must no longer seed or reference the `advisory_status` lookup table. Update test fixtures and assertions to use `AdvisoryStatusEnum` values directly. Ensure test coverage for status filtering on the advisory list endpoint and correct status representation in advisory detail responses.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests: remove `advisory_status` table seeding; update advisory fixture creation to use enum values directly; update status filter test cases to filter by enum string values; verify response status field contains correct string values

## Implementation Notes
- In `tests/api/advisory.rs`, the existing tests likely seed the `advisory_status` table with status rows and then create advisories with `status_id` FK references. Replace this with direct `status: AdvisoryStatusEnum::Fixed` (or equivalent string value) in the advisory creation.
- Follow the existing integration test pattern: tests use a real PostgreSQL test database and assert `resp.status() == StatusCode::OK`. See `tests/api/sbom.rs` for the established pattern.
- Test the status filter on the list endpoint: `GET /api/v2/advisory?status=Fixed` should return only advisories with that status.
- Verify that the response JSON includes the status field as a plain string (e.g., `"status": "Fixed"`) matching the enum variant name.
- Remove any test helper functions that interact with the `advisory_status` table.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, HTTP client setup, and assertion patterns
- `tests/api/advisory.rs` — existing advisory tests to modify (not rewrite from scratch)

## Acceptance Criteria
- [ ] All advisory integration tests pass without referencing the `advisory_status` table
- [ ] Tests verify status filtering works with enum values on the list endpoint
- [ ] Tests verify the correct status string is returned in advisory detail responses
- [ ] No test code references `advisory_status` table or entity
- [ ] All existing test scenarios continue to pass with the new schema

## Test Requirements
- [ ] Test advisory list with status filter for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Test advisory detail endpoint returns correct status string in response body
- [ ] Test advisory list without status filter returns advisories with all status values
- [ ] Test advisory creation via ingestion produces correct status in subsequent queries

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly

[sdlc-workflow] Description digest: sha256:feea633a8aaee107ffca3d4a0affe0f644a43d549343ee87ede76001f62d5935
