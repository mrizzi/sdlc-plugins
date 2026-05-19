# Task 6 — Update advisory integration tests for status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to reflect the new schema where advisory status is stored as an enum column (`advisory.status`) instead of via a join to the `advisory_status` lookup table. Test fixtures and assertions must be updated to work with the new enum-based status column, and new test cases should be added to verify status filtering works correctly with enum values.

## Files to Modify
- `tests/api/advisory.rs` — Update existing advisory integration tests: remove any test setup that inserts rows into the `advisory_status` table; update advisory insertion in test fixtures to use `AdvisoryStatusEnum` values directly; update status filter test cases to use enum string values; add test cases for each status value (New, Analyzing, Fixed, Rejected)
- `tests/Cargo.toml` — Add dependency on the entity crate if not already present (needed for `AdvisoryStatusEnum` import)

## Implementation Notes
- Follow the existing test patterns in `tests/api/advisory.rs` for structure — tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern per repository conventions
- Follow the test patterns in `tests/api/sbom.rs` for reference on integration test structure and database setup
- Test setup should insert advisory rows with the `status` enum column value directly, without any lookup table interaction
- Verify that the API response shape has not changed — the status field should still be a string in the JSON response
- Integration tests hit a real PostgreSQL test database per repository conventions
- Prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., filtering by each of the four status values)
- Per docs/constraints.md: commits must reference Jira issue ID, follow Conventional Commits, and include AI attribution trailer
- Per docs/constraints.md: PR must specify `--base TC-9005`

## Reuse Candidates
- `tests/api/advisory.rs` — Existing advisory integration tests to be updated in place
- `tests/api/sbom.rs` — SBOM integration tests for reference on test structure and database setup patterns
- `tests/api/search.rs` — Search integration tests for additional reference on query parameter testing patterns

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] Tests no longer reference `advisory_status` table or `status_id` column
- [ ] Test coverage exists for filtering by each status enum value (New, Analyzing, Fixed, Rejected)
- [ ] API response format assertions confirm status is still returned as a string
- [ ] All test functions have doc comments

## Test Requirements
- [ ] Verify advisory list endpoint integration test passes with status filter for each enum value
- [ ] Verify advisory get endpoint integration test returns correct status as string
- [ ] Verify all tests pass: `cargo test --test advisory`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
