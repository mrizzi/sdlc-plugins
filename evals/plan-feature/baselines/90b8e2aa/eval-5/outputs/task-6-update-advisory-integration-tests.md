# Task 6 — Update advisory endpoint integration tests

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Test fixtures must create advisories with enum status values directly, and assertions must verify that status filtering and retrieval work correctly with the enum column. The test database setup must no longer seed the `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to insert advisories with enum status values instead of FK references; update status filter tests to use enum values; remove any `advisory_status` table seeding from fixtures

## Implementation Notes
- Remove all test fixture code that inserts rows into the `advisory_status` table or references `status_id`.
- Update advisory insertion in test fixtures to set the `status` field directly using `AdvisoryStatusEnum` values.
- Add or update test cases that filter by each status value (New, Analyzing, Fixed, Rejected) to verify the enum column filtering works correctly.
- Per CONVENTIONS.md §Testing: use the integration test pattern established in `tests/api/` — hit a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test file scope.
- Follow the test patterns in `tests/api/sbom.rs` for how integration tests set up fixtures, make HTTP requests, and assert on responses.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrating the project's test fixture setup, HTTP request patterns, and assertion style
- `tests/api/search.rs` — search endpoint tests showing additional integration test patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` table or `status_id` column
- [ ] Tests verify status filtering for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the advisory list response includes the correct status string
- [ ] Tests verify the advisory detail response includes the correct status string

## Test Requirements
- [ ] Test listing advisories returns correct status strings from the enum column
- [ ] Test filtering advisories by status `Fixed` returns only fixed advisories
- [ ] Test filtering advisories by status `New` returns only new advisories
- [ ] Test getting a single advisory returns the correct status from the enum column
- [ ] Test that the response JSON shape is unchanged (backward compatibility)

## Verification Commands
- `cargo test -p tests -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service, model, and endpoints for enum status
- Depends on: Task 5 — Update advisory ingestion pipeline for enum status
