## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint integration tests to work with the new enum-based status column instead of the lookup table. Tests must verify that advisory list filtering by status, advisory detail retrieval with status, and advisory ingestion all function correctly with the `advisory_status_enum` column. Remove any test setup code that inserts rows into the now-dropped `advisory_status` lookup table and replace it with direct enum value usage.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to use `AdvisoryStatusEnum` values instead of inserting into `advisory_status` lookup table; update status filter assertions; add tests for each enum value; verify response shape is unchanged

## Implementation Notes
The existing integration tests likely set up test data by inserting rows into `advisory_status` and then creating advisories with `status_id` references. Replace this with:
1. Create advisories with `status: AdvisoryStatusEnum::Fixed` (or other variants) directly on the `ActiveModel`
2. Remove any `advisory_status` table seeding from test fixtures
3. Verify the response JSON still contains a string `"status"` field (not an enum object)

Test the status filter by querying `GET /api/v2/advisory?status=Fixed` and verifying only advisories with that status are returned.

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status assertions.
Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests as a reference for test structure, setup patterns, and assertion conventions
- `tests/api/advisory.rs` — existing advisory tests to understand current test patterns and adapt them

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] Test setup no longer references the `advisory_status` lookup table
- [ ] Tests verify status filtering for each of the four enum values (`New`, `Analyzing`, `Fixed`, `Rejected`)
- [ ] Tests verify the response JSON shape is unchanged (status is a string field)
- [ ] Tests verify advisory creation with each valid status value

## Test Requirements
- [ ] Test: `GET /api/v2/advisory?status=Fixed` returns only advisories with status `Fixed`
- [ ] Test: `GET /api/v2/advisory?status=New` returns only advisories with status `New`
- [ ] Test: `GET /api/v2/advisory/{id}` returns the correct status string in the detail response
- [ ] Test: Advisory list without status filter returns advisories with mixed statuses
- [ ] Test: Advisory ingestion creates records with the correct enum status value

## Verification Commands
- `cargo test --test advisory` — advisory integration tests pass
- `cargo test -p tests` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum status writes
