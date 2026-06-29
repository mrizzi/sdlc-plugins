## Repository
trustify-backend

## Target Branch
TC-9005

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Update the advisory integration tests to exercise the new enum-based status column. Tests must verify that advisory list and detail endpoints return correct status values using the enum column, that status filtering works without the lookup table join, and that the advisory ingestion pipeline writes enum values correctly. Remove any test fixtures or setup code that references the `advisory_status` lookup table.

## Files to Modify
- `tests/api/advisory.rs` — Update advisory endpoint integration tests to use enum status values and remove lookup table references

## Implementation Notes
- In `tests/api/advisory.rs`, update test setup code that previously inserted rows into the `advisory_status` table — this table no longer exists. Instead, set the `status` field directly on advisory inserts using the `AdvisoryStatusEnum` values
- Update assertions that check status values in API responses — the response shape is unchanged (status is a string), but the underlying data source is now the enum column
- Add test cases for status filtering to verify `WHERE status = 'Fixed'` style queries work correctly without the join
- Follow the existing test pattern: use `assert_eq!(resp.status(), StatusCode::OK)` and hit a real PostgreSQL test database
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test structure, setup patterns, and assertion style
- `tests/api/search.rs` — Search endpoint integration tests; additional reference for test patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the enum-based status column
- [ ] No test code references the `advisory_status` lookup table
- [ ] Tests cover status filtering by all four enum values
- [ ] Test setup creates advisories with enum status values directly

## Test Requirements
- [ ] Test advisory list endpoint with status filter for each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Test advisory detail endpoint returns correct status string in response
- [ ] Test that advisory list without status filter returns advisories with all status types
- [ ] Test advisory ingestion writes correct enum status value

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly

[sdlc-workflow] Description digest: sha256-md:c9a8370d3bde7c045c9217d42e44d286fa00eba2557d667322b4c60b708385ad
