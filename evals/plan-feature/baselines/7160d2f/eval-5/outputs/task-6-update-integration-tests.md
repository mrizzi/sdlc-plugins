## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new `advisory_status_enum` column instead of the `advisory_status` lookup table. Tests that set up advisory test data by inserting status rows into the lookup table must be updated to use enum values directly. Tests that assert on advisory query results must verify the status field comes from the enum column.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use enum status values instead of lookup table inserts; update assertions to verify status filtering works with the enum column; remove any test helpers that create `advisory_status` rows

## Implementation Notes
- In `tests/api/advisory.rs`, locate test setup code that inserts rows into the `advisory_status` table (e.g., `advisory_status::ActiveModel { name: Set("New".to_owned()), .. }.insert(db).await`). Replace with direct `AdvisoryStatusEnum` values when creating advisory test records.
- Update any test that filters advisories by status to use the enum value in the query parameter (e.g., `?status=Fixed`).
- Verify the response JSON still contains the status as a string field — the API contract is unchanged.
- Follow the existing test pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status checks (see `tests/api/sbom.rs` for the established pattern).
- Remove any test utility functions or fixtures that create or reference `advisory_status` rows.
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing test code before modifying; follow established patterns.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test patterns, test setup, and assertion style
- `tests/api/search.rs` — reference for additional integration test patterns

## Acceptance Criteria
- [ ] Advisory integration tests no longer reference the `advisory_status` table or entity
- [ ] Tests correctly create advisories with enum status values
- [ ] Tests verify status filtering works with the enum column
- [ ] All advisory integration tests pass
- [ ] Response shape assertions confirm status is still a string in JSON

## Test Requirements
- [ ] Run `cargo test -p tests` (or equivalent test runner) to verify all integration tests pass
- [ ] Verify advisory list with status filter returns correct results
- [ ] Verify advisory get returns the status field correctly

## Verification Commands
- `cargo test --test advisory` — expected: all advisory tests pass
- `cargo test -p tests` — expected: all integration tests pass (no regressions in sbom or search tests)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
