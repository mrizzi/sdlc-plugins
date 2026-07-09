## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint (TC-9004). These tests verify the full request-response cycle of `GET /api/v2/sbom/{id}/license-report` against a real PostgreSQL test database, covering the happy path (SBOM with mixed license compliance), edge cases (empty SBOM, missing SBOM), and transitive dependency inclusion.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license compliance report endpoint

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` for test setup (database fixtures, HTTP client creation, server initialization) and assertion style (`assert_eq!(resp.status(), StatusCode::OK)`).
- Set up test fixtures that create an SBOM with packages having various licenses (some compliant, some non-compliant per a test policy), including transitive dependencies.
- Verify the response JSON structure matches `{ groups: [{ license, packages, compliant }] }`.
- Test both compliant and non-compliant license scenarios to confirm the policy enforcement works end-to-end.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Place tests in `tests/api/`.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup, fixture creation, and assertion patterns
- `tests/api/advisory.rs` — additional reference for integration test patterns in the same test suite

## Acceptance Criteria
- [ ] Integration test passes for generating a license report on an SBOM with mixed compliant and non-compliant licenses
- [ ] Integration test verifies that transitive dependency licenses are included in the report
- [ ] Integration test verifies 404 response for a non-existent SBOM ID
- [ ] Integration test verifies that packages are correctly grouped by license type
- [ ] Integration test verifies that the `compliant` flag is set correctly per the test policy

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns 200 with correct grouping for an SBOM with packages under MIT, Apache-2.0, and GPL-3.0 licenses
- [ ] Test: GET /api/v2/sbom/{id}/license-report includes transitive dependency licenses in the report
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns 404 for a non-existent SBOM ID
- [ ] Test: GET /api/v2/sbom/{id}/license-report returns empty groups for an SBOM with no packages
- [ ] Test: compliance flags match the configured policy (e.g., MIT=compliant, GPL-3.0=non-compliant given a restrictive policy)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
