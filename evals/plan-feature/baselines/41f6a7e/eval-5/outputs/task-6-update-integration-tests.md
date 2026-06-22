# Task 6 — Update advisory integration tests for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema where `advisory.status` is an enum column instead of a foreign key join. Tests must verify that the advisory list endpoint correctly filters by enum status values, the advisory get endpoint returns the status string directly, and the API response shape remains unchanged.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory integration tests: remove any test setup that seeds the `advisory_status` lookup table; update test advisory inserts to use the `status` enum column; update assertions on response payloads to verify the status field is returned as before; add a test for filtering by status (e.g., `GET /api/v2/advisory?status=Fixed`); verify that the response shape has not changed from the consumer's perspective

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` for test structure, database setup, and assertion style. The project uses `assert_eq!(resp.status(), StatusCode::OK)` pattern per the repository conventions.
- Tests hit a real PostgreSQL test database (per repository conventions). Update test database setup to not seed the `advisory_status` table, since it no longer exists.
- When inserting test advisory records, use the `ActiveModel` with `status: Set(AdvisoryStatusEnum::New)` instead of the old `status_id: Set(1)` pattern.
- Add at least one test case for each use case in the feature:
  - UC-1: Advisory list with status filter — verify `GET /api/v2/advisory?status=Fixed` returns only advisories with status "Fixed"
  - UC-2: Advisory ingestion flow — verify that an ingested advisory has the correct enum status in the response
- Per docs/constraints.md §5.11: add a doc comment to every test function explaining what it verifies.
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases.
- Per docs/constraints.md §5.8: compare the updated advisory tests against `tests/api/sbom.rs` for parity on setup, teardown, and assertion patterns.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, database setup helpers, and assertion patterns
- `tests/api/search.rs` — reference for search-related test patterns if advisory search is also tested

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum schema
- [ ] No test references the `advisory_status` lookup table
- [ ] A test verifies status filtering on the advisory list endpoint works with enum values
- [ ] A test verifies the advisory get endpoint returns status as a string in the response
- [ ] The API response shape in test assertions matches the pre-migration response shape (status is a string)
- [ ] `cargo test --test api` passes

## Test Requirements
- [ ] Test advisory list endpoint returns advisories with status as a string field
- [ ] Test advisory list endpoint filters by status enum value (e.g., `?status=Fixed` returns only "Fixed" advisories)
- [ ] Test advisory get endpoint returns a single advisory with status as a string
- [ ] Test that seeding advisories with different enum statuses produces correct filtered results

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum status column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly
