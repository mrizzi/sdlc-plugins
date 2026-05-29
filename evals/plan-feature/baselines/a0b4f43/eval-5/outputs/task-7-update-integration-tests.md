## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new enum-based status schema. Tests must no longer set up or reference the `advisory_status` lookup table. Instead, they should create advisory records with `AdvisoryStatusEnum` values directly and verify that status filtering, listing, and retrieval work correctly with the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update all advisory test functions: remove setup code that inserts into `advisory_status` table; create test advisory records with `status: AdvisoryStatusEnum::*` values directly; update assertions to check enum string serialization; add test cases for status filtering with enum values

## Implementation Notes
- In `tests/api/advisory.rs`, locate test setup code that creates `advisory_status` rows and stores `status_id` foreign keys on advisory records. Replace with direct enum value assignment.
- Existing test patterns can be found in `tests/api/sbom.rs` — follow the same structure for setup, request, and assertion patterns.
- Test the following scenarios:
  - List advisories with no status filter — returns all advisories with status as string
  - List advisories with status filter `?status=Fixed` — returns only Fixed advisories
  - List advisories with invalid status filter — returns appropriate error
  - Get advisory by ID — response includes status as string
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per the project's testing conventions.
- Per `docs/constraints.md` §5.11: add a doc comment to every test function.
- Per `docs/constraints.md` §5.12: add given-when-then inline comments to non-trivial test functions.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM integration tests demonstrating the project's test patterns and assertion style
- `tests/api/search.rs` — search integration tests as another reference for test structure

## Acceptance Criteria
- [ ] No test code references `advisory_status` table or `status_id` column
- [ ] Tests create advisory records with `AdvisoryStatusEnum` values directly
- [ ] Status filtering is tested with valid enum values
- [ ] Invalid status filter handling is tested
- [ ] Advisory detail retrieval returns correct status string
- [ ] All advisory integration tests pass

## Test Requirements
- [ ] Run advisory integration tests: `cargo test -p tests --test advisory`
- [ ] Verify all tests pass against a clean test database with the new migration applied
- [ ] Verify no tests reference the dropped `advisory_status` table

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory tests pass
- `cargo test -p tests` — full integration test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main