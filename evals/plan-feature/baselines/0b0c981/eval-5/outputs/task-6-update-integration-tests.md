## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema where advisory status is an enum column on the `advisory` table instead of a joined lookup table. Tests must verify that advisory list and detail endpoints return correct status values using the enum column, and that status filtering works without the join. Remove any test setup code that inserts rows into the `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use enum status values directly; update assertions to verify status filtering and response correctness with the new schema

## Implementation Notes
- In `tests/api/advisory.rs`, update test fixture setup: instead of inserting rows into the `advisory_status` table and using `status_id` foreign keys, set the `status` field directly to `AdvisoryStatusEnum` variants when creating test advisory entities.
- Update status filter test cases to verify that `WHERE status = 'Fixed'` filtering works correctly through the API endpoint.
- Verify that the advisory list response shape is unchanged — the `status` field should still be a string in the JSON response.
- Follow the existing integration test patterns in `tests/api/sbom.rs` for test setup, HTTP request construction, and assertion patterns (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
- Per constraints §5.11: add a doc comment to every test function created. Per §5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — reference pattern for integration test structure, HTTP client setup, and assertion patterns
- `tests/api/search.rs` — reference for test patterns involving filtered queries

## Acceptance Criteria
- [ ] No test code references the `advisory_status` lookup table
- [ ] Tests create advisory entities with `AdvisoryStatusEnum` values directly
- [ ] Tests verify advisory list endpoint returns correct status strings
- [ ] Tests verify status filtering works correctly with each enum value
- [ ] All advisory integration tests pass

## Test Requirements
- [ ] Integration test verifying advisory list endpoint returns advisories with correct status values
- [ ] Integration test verifying advisory list endpoint status filter returns only matching advisories
- [ ] Integration test verifying advisory detail endpoint returns the correct status string
- [ ] All existing advisory test scenarios continue to pass with the updated setup

## Verification Commands
- `cargo test --test api -- advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:121d9ac8cb52dc05935a5da6a33a7f2cf2cb90a92ad5f6f6e9a25212d1d64d20
