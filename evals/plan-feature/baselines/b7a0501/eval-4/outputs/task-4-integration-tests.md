# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint covering the full request-response cycle against a real PostgreSQL test database. Tests verify correct grouping by license, compliance flagging, transitive dependency inclusion, error handling for invalid SBOM IDs, and edge cases like empty SBOMs.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if needed (depending on how the test harness discovers tests)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data in the database, make HTTP requests to the endpoint, and assert on response status and body
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern used by existing tests
- Test data setup should create an SBOM with multiple packages having different licenses (MIT, Apache-2.0, GPL-3.0) and a policy that flags GPL-3.0 as non-compliant
- Include a test case with transitive dependencies to verify the full dependency tree is walked
- Include edge cases: SBOM with no packages (empty groups), non-existent SBOM ID (404 response)
- Per constraints doc section 5.11: every test function must have a doc comment
- Per constraints doc section 5.12: non-trivial test functions must have given-when-then inline comments
- Per constraints doc section 5.9: consider parameterized tests if multiple test cases exercise the same behavior with different inputs (e.g., testing different license combinations)

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for SBOM integration test patterns, test database setup, and assertion style
- `tests/api/advisory.rs` — Reference for similar endpoint integration test structure
- `tests/api/search.rs` — Additional reference for test patterns

## Acceptance Criteria
- [ ] Test for valid SBOM returns 200 with correctly grouped license data
- [ ] Test for SBOM with policy violations shows `compliant: false` on flagged groups
- [ ] Test for transitive dependencies verifies all transitively included packages appear in the report
- [ ] Test for non-existent SBOM ID returns 404
- [ ] Test for SBOM with no packages returns 200 with empty groups array
- [ ] All tests pass against the test database

## Test Requirements
- [ ] `test_license_report_compliant_sbom` — SBOM with only allowed licenses returns all groups as compliant
- [ ] `test_license_report_with_violations` — SBOM with denied licenses returns non-compliant groups flagged
- [ ] `test_license_report_transitive_deps` — Transitive dependencies are included in license groups
- [ ] `test_license_report_not_found` — Non-existent SBOM ID returns 404
- [ ] `test_license_report_empty_sbom` — SBOM with no packages returns empty groups

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
