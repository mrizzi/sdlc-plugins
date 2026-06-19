# Task 6 — Add integration tests for advisory status enum migration

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update and extend the existing advisory integration tests to verify that the advisory endpoints work correctly with the new `advisory_status_enum` column. Tests must cover status filtering, advisory retrieval with status, and ingestion with enum values. Ensure all existing advisory tests are updated to reflect the new schema (no joins to `advisory_status`).

## Files to Modify
- `tests/api/advisory.rs` — Update existing advisory endpoint integration tests to work with the new enum-based status column; add new test cases for status filtering by enum value

## Implementation Notes
- Follow the existing test pattern in `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Review `tests/api/sbom.rs` for a sibling test file demonstrating the project's integration test setup, database seeding, and assertion patterns
- Add test cases that:
  - Verify filtering advisories by each status value (New, Analyzing, Fixed, Rejected) returns correct results
  - Verify advisory detail response includes the status as a string (not an integer ID)
  - Verify the API response shape is unchanged (backward compatibility)
- Update any existing test fixtures or seed data that reference `advisory_status` table inserts — these must now set the `status` enum column directly
- Per docs/constraints.md §5.11: add a doc comment to every test function
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions
- Per docs/constraints.md §5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., filtering by different status values)
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format

## Reuse Candidates
- `tests/api/advisory.rs` — Existing advisory integration tests to extend
- `tests/api/sbom.rs` — Sibling integration test file demonstrating test setup, database seeding, and response assertion patterns
- `tests/api/search.rs` — Another sibling test file for additional pattern reference

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum schema
- [ ] New tests verify status filtering by each of the four enum values
- [ ] New tests verify the API response shape is unchanged (status is a string)
- [ ] Test seed data uses enum values instead of `advisory_status` table inserts

## Test Requirements
- [ ] `cargo test -p tests --test advisory` — all advisory tests pass
- [ ] Test coverage includes filtering by New, Analyzing, Fixed, and Rejected statuses
- [ ] Tests verify backward-compatible response format

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass
- `cargo test -p tests` — full integration test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for status enum
