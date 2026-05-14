## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. The tests verify end-to-end behavior: ingesting an SBOM with package-license data, calling the license report endpoint, and validating the response structure, grouping, compliance flags, and error handling. Tests hit a real PostgreSQL test database following the project's existing integration test conventions.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering compliant packages, non-compliant packages, mixed compliance, transitive dependencies, missing SBOM, and edge cases (empty SBOM, packages with no license)

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (unlikely since the test infrastructure already exists)

## Implementation Notes
- **Test pattern:** Follow the existing integration test pattern in `tests/api/sbom.rs`. Tests should use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code verification and deserialize the response body into the `LicenseReport` struct for structural assertions.
- **Test setup:** Each test should: (1) set up a test database with appropriate SBOM and package-license data, (2) configure a test license policy, (3) call the endpoint via the test HTTP client, (4) assert on the response.
- **Test cases to implement:**
  1. **All compliant:** Ingest an SBOM with packages all under MIT license (allowed by policy). Verify all groups have `compliant: true`.
  2. **Mixed compliance:** Ingest an SBOM with packages under MIT (allowed) and GPL-3.0 (denied). Verify the MIT group is compliant and the GPL-3.0 group is not.
  3. **Transitive dependencies:** Ingest an SBOM with a dependency tree (package A depends on B, B depends on C). Verify all three packages appear in the report, including transitive dependency C.
  4. **Unknown license:** Ingest an SBOM with a package under a license not in the policy. Verify it defaults to non-compliant.
  5. **Missing SBOM:** Call the endpoint with a nonexistent UUID. Verify HTTP 404 response.
  6. **Empty SBOM:** Ingest an SBOM with no packages. Verify the report returns an empty `groups` array.
- **Reuse existing test utilities:** Check `tests/api/sbom.rs` for helper functions that set up test SBOMs and packages. Reuse those helpers rather than duplicating setup code.
- **Error response assertions:** For error cases (404, 500), assert on both the HTTP status code and that the response body contains a meaningful error message.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests; reuse test setup patterns, HTTP client configuration, and assertion helpers
- `tests/api/advisory.rs` — Additional integration test example demonstrating the test database setup and teardown pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Struct used in the response; import for deserialization in test assertions

## Acceptance Criteria
- [ ] All six test scenarios pass against a real PostgreSQL test database
- [ ] Tests verify the response JSON structure matches `{ "groups": [{ "license": string, "packages": [...], "compliant": bool }] }`
- [ ] Tests verify correct compliance flag values based on the license policy
- [ ] Tests verify transitive dependencies are included in the report
- [ ] Tests cover error cases (missing SBOM returns 404)
- [ ] No N+1 query issues observable in test execution (tests complete within reasonable time for 1000-package scenarios)

## Test Requirements
- [ ] Integration test: all-compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: mixed-compliance SBOM correctly flags denied licenses as non-compliant
- [ ] Integration test: transitive dependencies appear in the report alongside direct dependencies
- [ ] Integration test: unlisted license defaults to non-compliant per policy
- [ ] Integration test: nonexistent SBOM ID returns HTTP 404
- [ ] Integration test: SBOM with no packages returns empty groups array

## Dependencies
- Depends on: Task 1 — License policy configuration and report models
- Depends on: Task 2 — License compliance report service
- Depends on: Task 3 — License report endpoint and route registration
