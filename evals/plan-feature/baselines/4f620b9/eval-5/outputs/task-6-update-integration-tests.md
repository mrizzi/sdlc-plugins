# Task 6 — Update advisory integration tests for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to validate the new enum-based status column. Tests must verify that advisory list filtering by status works against the enum column, that advisory details return the correct enum status value, and that the API response shape remains unchanged (status as a string in JSON). Remove any test setup code that inserts rows into the now-dropped `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use enum status values instead of lookup table inserts; update status filter assertions to use enum values; verify response shape backward compatibility

## Implementation Notes
- The existing advisory integration tests likely set up test data by inserting rows into `advisory_status` and then referencing those IDs when creating advisory rows. Replace this with direct enum value assignment on the advisory entity.
- Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern used throughout the test suite per the project's testing conventions.
- Test database setup should run the new migration (Task 2) to have the enum type available.
- Verify that JSON serialization of the status field in API responses produces the same string values as before (e.g., `"status": "Fixed"` not `"status": "fixed"` or `"status": 2`).
- Reference the SBOM integration tests in `tests/api/sbom.rs` for the established integration test pattern.
- Per docs/constraints.md §5.11: add a doc comment to every test function created.
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test file demonstrating the established test setup, assertion, and response validation patterns
- `tests/api/advisory.rs` — existing advisory tests to update (contains current test structure and setup patterns)

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Tests verify status filtering works with enum values (e.g., filter by "Fixed")
- [ ] Tests verify the API response shape is unchanged (status is still a string)
- [ ] Test functions have doc comments and given-when-then comments where applicable

## Test Requirements
- [ ] Test advisory list endpoint with status filter for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Test advisory get endpoint returns correct status enum value as string
- [ ] Test that filtering by an invalid status returns an appropriate error response
- [ ] Verify all tests pass: `cargo test --test advisory`

## Verification Commands
- `cargo test --test advisory` — all advisory integration tests pass
- `cargo test` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use enum status column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly

[sdlc-workflow] Description digest: sha256-md:b7402079a54ce521dcd4b06ff5cf412545792a2f55931d0fdb378aa9ecd14e00
