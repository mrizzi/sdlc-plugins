## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based status schema. Tests must no longer set up or reference the `advisory_status` lookup table. Instead, they should create advisory fixtures with the `status` enum column directly and verify that filtering, listing, and retrieval work correctly with the enum values.

## Files to Modify
- `tests/api/advisory.rs` — update all test fixtures to use the `status` enum column instead of `status_id` FK; remove any test setup that creates `advisory_status` lookup rows; update assertions to verify enum-based status filtering and response values

## Implementation Notes
- The existing integration tests in `tests/api/advisory.rs` likely create `advisory_status` rows as test fixtures and reference them via `status_id`. Replace this with direct enum value assignment on the advisory `ActiveModel`.
- Follow the existing test pattern: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for response validation.
- Look at `tests/api/sbom.rs` for reference on the test fixture setup pattern used in this project.
- Ensure tests cover all four status values (New, Analyzing, Fixed, Rejected) in filtering scenarios.
- Verify the response shape is unchanged — the JSON response should still include status as a string field with the same values as before the migration.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test pattern for reference on test structure and assertion style
- `tests/api/search.rs` — search endpoint test pattern for additional reference

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test references the `advisory_status` lookup table or `status_id` column
- [ ] Tests verify status filtering with the enum column works correctly
- [ ] Tests verify the API response shape is unchanged (status as string)

## Test Requirements
- [ ] Test advisory list with status filter for each of the four enum values
- [ ] Test advisory get returns the correct status string in the response
- [ ] Test advisory list without status filter returns advisories with all status values

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass
- `cargo test -p tests` — all integration tests pass (no regressions in other tests)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
