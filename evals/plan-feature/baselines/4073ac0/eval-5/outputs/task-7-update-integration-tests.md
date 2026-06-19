## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to work with the new enum-based status column instead of the `advisory_status` lookup table. Test setup must create advisories with enum status values directly, assertions must verify status as a string in API responses, and new tests must validate status filtering with the enum column.

## Files to Modify
- `tests/api/advisory.rs` — Update test setup to insert advisories with `AdvisoryStatusEnum` values instead of creating `advisory_status` rows and foreign keys; update status filter test cases to use enum values; add tests for invalid status filter handling; verify response format is unchanged

## Implementation Notes
Follow the existing test patterns in `tests/api/advisory.rs`. The tests use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation.

Update test fixtures that create advisory rows to set `status: AdvisoryStatusEnum::New` (or other variants) directly on the active model instead of creating `advisory_status` rows and setting `status_id`.

Use the sibling test file `tests/api/sbom.rs` as a pattern reference for integration test structure and database setup.

For status filtering tests, verify:
- Filtering by a valid enum value returns only matching advisories
- Filtering by an invalid value returns a 400 error
- No filter returns all advisories with correct status strings

Ensure the test assertions check that the response JSON `status` field contains the expected string value (e.g., `"Fixed"`, `"New"`), confirming backward compatibility.

## Reuse Candidates
- `tests/api/advisory.rs` — Existing advisory test cases to update in-place
- `tests/api/sbom.rs` — Sibling test module for pattern reference on test setup and assertions
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper used in list endpoint test assertions

## Acceptance Criteria
- [ ] All existing advisory tests pass with the enum-based status schema
- [ ] Test setup creates advisories with `AdvisoryStatusEnum` values directly
- [ ] No test references to `advisory_status` entity or `status_id` column
- [ ] Status filtering tests validate enum-based filtering
- [ ] Invalid status filter test confirms 400 error response
- [ ] Response body assertions confirm status is returned as a string (backward compatible)

## Test Requirements
- [ ] Integration test: list advisories returns status as string in response
- [ ] Integration test: filter by status "Fixed" returns correct subset
- [ ] Integration test: filter by invalid status returns 400 Bad Request
- [ ] Integration test: get advisory by ID returns correct status string
- [ ] All advisory integration tests pass (`cargo test -p tests --test advisory`)

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
