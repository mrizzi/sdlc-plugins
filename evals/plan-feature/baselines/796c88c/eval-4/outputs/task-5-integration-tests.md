## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint that validate the full request-response cycle against a real PostgreSQL test database. These tests ensure the endpoint correctly generates compliance reports for various SBOM configurations, including edge cases like empty SBOMs, packages with no licenses, and large SBOMs for performance validation.

## Files to Modify
- None

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for `GET /api/v2/sbom/{id}/license-report`:
  - `test_license_report_basic` -- Ingest an SBOM with known packages and licenses, call the endpoint, verify response structure and grouping
  - `test_license_report_compliance_flags` -- Ingest an SBOM with both compliant and non-compliant licenses, verify compliance flags match the policy
  - `test_license_report_transitive_dependencies` -- Ingest an SBOM with transitive dependencies, verify they appear in the report with `is_transitive: true`
  - `test_license_report_unknown_licenses` -- Ingest packages with missing license data, verify they are grouped under "UNKNOWN"
  - `test_license_report_not_found` -- Call the endpoint with a non-existent SBOM ID, verify HTTP 404
  - `test_license_report_empty_sbom` -- Ingest an SBOM with no packages, verify the endpoint returns an empty report without error
  - `test_license_report_performance` -- Ingest an SBOM with 1000 packages, measure response time is under 500ms (p95 target)

## API Changes
- None (tests only)

## Implementation Notes
- Follow the testing patterns in `tests/api/sbom.rs` for test setup, database fixtures, and assertion style
- Use the same test database configuration and setup/teardown patterns as existing integration tests
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns consistent with existing tests
- For the performance test, use `std::time::Instant` to measure elapsed time and assert it is under 500ms; this test may be marked `#[ignore]` if CI environments have variable performance
- Test fixtures should create SBOM and package data programmatically using the ingestor service or direct database inserts, following whichever pattern existing tests use
- Ensure test license policy files are created in temporary directories to avoid interfering with the default policy

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the core scenarios: basic report, compliance flags, transitive deps, unknown licenses, 404, empty SBOM
- [ ] Performance test validates the p95 < 500ms target for 1000 packages
- [ ] Tests follow existing patterns in `tests/api/` for consistency
- [ ] Tests are independent and can run in any order

## Test Requirements
- [ ] Integration test: basic license report returns expected grouping and structure
- [ ] Integration test: compliance flags correctly reflect the license policy
- [ ] Integration test: transitive dependencies are included and flagged
- [ ] Integration test: unknown licenses are handled gracefully
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: empty SBOM returns valid empty report
- [ ] Integration test (optional, may be marked `#[ignore]`): 1000-package SBOM completes within 500ms

## Dependencies
- Depends on: Task 4 -- Implement license report endpoint
