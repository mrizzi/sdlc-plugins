## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the schema migration from the `advisory_status` lookup table to the `status` enum column. Test fixtures and assertions must use the new enum-based status field. Add test coverage for status filtering with the enum column to verify the new query path works correctly.

## Files to Modify
- `tests/api/advisory.rs` — update existing advisory endpoint integration tests to use the enum-based status field; remove any test setup that inserts into the `advisory_status` lookup table; update test fixtures to set the `status` enum column directly; add test cases for filtering by each enum value (New, Analyzing, Fixed, Rejected)

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` for test structure, database setup, and assertion style. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the test conventions.

Test fixtures should insert advisory records with the `status` enum column set directly, without referencing the `advisory_status` table.

Ensure test coverage for:
- Listing advisories without a status filter returns all statuses
- Filtering by a single status value returns only matching advisories
- The response JSON shape for advisory endpoints remains unchanged (status is a string)

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating the test setup pattern, database fixture creation, and assertion style
- `tests/api/advisory.rs` — the existing advisory tests being modified, containing the current test structure and fixture patterns

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum-based schema
- [ ] No test code references the `advisory_status` lookup table
- [ ] Test fixtures create advisories with the `status` enum column directly
- [ ] Status filter tests cover all four enum values

## Test Requirements
- [ ] `GET /api/v2/advisory` returns advisories with correct status strings
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed
- [ ] `GET /api/v2/advisory/{id}` returns the correct status for a specific advisory
- [ ] All four status enum values (New, Analyzing, Fixed, Rejected) can be filtered correctly

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:827c7ed38955c498f31af48aade5d49ab17efa82aace4e5d593050985942ccdf
