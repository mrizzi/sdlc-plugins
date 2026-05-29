# Task 6 -- Update advisory integration tests for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column. Tests must no longer set up or reference the `advisory_status` lookup table. Instead, they should create test advisories with `AdvisoryStatusEnum` values directly and assert that filtering, fetching, and listing by enum status works correctly. This ensures end-to-end validation that the migration, entity changes, service updates, and endpoint changes all work together.

## Files to Modify
- `tests/api/advisory.rs` -- update all advisory integration tests to: (1) create test data using `advisory.status = AdvisoryStatusEnum::Fixed` instead of inserting into `advisory_status` and referencing via `status_id`, (2) update assertions to check the `status` string field in responses, (3) add test cases for filtering by each enum value, (4) remove any test setup code that creates `advisory_status` lookup table rows
- `tests/Cargo.toml` -- add dependency on `entity` crate if not already present (needed for `AdvisoryStatusEnum` import)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/search.rs` for test structure: setup test data, make HTTP request, assert response status and body
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the repository conventions
- Test data setup should insert advisory rows with the enum status field directly, not through the old lookup table flow
- Include test cases for all four status values (New, Analyzing, Fixed, Rejected) to ensure complete enum coverage
- Verify that the JSON response shape has not changed -- `status` should still appear as a string field with values like `"Fixed"`, `"New"`, etc.
- Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005
- Per docs/constraints.md SS5.11: add a doc comment to every test function explaining what it verifies
- Per docs/constraints.md SS5.12: add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test structure, test data setup, and assertion patterns
- `tests/api/search.rs` -- reference for search-related integration test patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the enum-based schema
- [ ] No test code references `advisory_status` entity, table, or `status_id` column
- [ ] Tests cover filtering advisories by each of the four status values
- [ ] Tests verify that JSON response format is unchanged (backward compatibility)
- [ ] All test functions have doc comments

## Test Requirements
- [ ] Test GET /api/v2/advisory returns advisories with correct status strings
- [ ] Test GET /api/v2/advisory?status=Fixed returns only advisories with Fixed status
- [ ] Test GET /api/v2/advisory?status=New returns only advisories with New status
- [ ] Test GET /api/v2/advisory/{id} returns the correct status for a specific advisory
- [ ] Test that filtering by an invalid status value returns an appropriate error response

## Verification Commands
- `cargo test -p tests --test advisory` -- all advisory integration tests pass
- `cargo test` -- full test suite passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory_status_enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service, models, and endpoints to use enum status
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status directly

[sdlc-workflow] Description digest: sha256:5aa71f7c08d07927c09c1721b8ade9bcfc9d5fbc14c5bf507d4bae957be72a93
