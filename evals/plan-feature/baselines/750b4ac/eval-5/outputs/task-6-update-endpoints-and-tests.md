# Task 6 — Update advisory endpoints and integration tests

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to work with the new enum-based status field and update all integration tests to verify the new behavior. The advisory list and get endpoints must filter and return status values from the `advisory.status` enum column instead of joining the `advisory_status` table. Integration tests must be updated to create test data using the enum column and verify correct status filtering and response shapes.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use `AdvisoryStatusEnum` values instead of string-based lookup table joins; ensure the `GET /api/v2/advisory` endpoint returns status as a string in the response (no API shape change)
- `modules/fundamental/src/advisory/endpoints/get.rs` — update `GET /api/v2/advisory/{id}` to include status from enum field in response
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if filter parameter types change
- `tests/api/advisory.rs` — update integration tests: modify test data setup to use enum status values instead of inserting into `advisory_status` table; add test for status filtering via `WHERE status = 'Fixed'` (UC-1); verify response shape is unchanged

## Implementation Notes
- The advisory endpoints in `modules/fundamental/src/advisory/endpoints/` use query parameters for filtering. Update the status filter to accept string values that map to `AdvisoryStatusEnum` variants. The filter parsing should convert the query string to the enum variant and pass it to the service layer.
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for consistent handler structure.
- Response types use `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` — the wrapper is unchanged, only the status field source changes.
- Integration tests in `tests/api/advisory.rs` follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions. Update test setup to insert advisories with `status: AdvisoryStatusEnum::Fixed` etc. instead of creating `advisory_status` rows.
- Ensure the API response body still returns status as a plain string (e.g., `"status": "Fixed"`) — no user-facing API contract change.
- Per docs/constraints.md section 5.1: changes must be scoped to the files listed above.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint implementation for consistent handler and filter patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference get endpoint pattern
- `tests/api/sbom.rs` — reference integration test pattern for endpoint testing with test data setup
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used in list response

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` returns advisories with status field sourced from enum column
- [ ] `GET /api/v2/advisory?status=Fixed` correctly filters by enum value
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with correct status from enum
- [ ] API response shape is unchanged — status is still a string field in the JSON response
- [ ] All existing integration tests pass with updated test data setup
- [ ] New integration test verifies status filtering without join (UC-1)

## Test Requirements
- [ ] Integration test: list advisories returns correct status values from enum column
- [ ] Integration test: filter advisories by status "Fixed" returns only matching advisories
- [ ] Integration test: get advisory by ID returns correct status from enum
- [ ] Integration test: verify response JSON shape is identical to pre-migration shape

## Verification Commands
- `cargo test -p tests -- advisory` — advisory integration tests pass
- `cargo check -p fundamental` — endpoint code compiles

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service layer and models to use status enum

[sdlc-workflow] Description digest: sha256-md:90421bba50291d38700402a9bf3f3fe14df831b52246136c3ca3b86f5e939e26
