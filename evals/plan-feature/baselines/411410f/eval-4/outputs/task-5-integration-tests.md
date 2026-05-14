# Task 5: Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, validating correct license grouping, compliance flagging, transitive dependency inclusion, and error handling.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add test file to the test suite if needed (depends on test discovery configuration)

## Implementation Notes
- Follow the existing integration test patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
  - Set up test data by ingesting an SBOM with known packages and licenses before each test
- Test scenarios to implement:
  1. **Basic report generation**: Ingest an SBOM with packages having MIT and Apache-2.0 licenses. Call `GET /api/v2/sbom/{id}/license-report`. Assert response contains two groups, both with `compliant: true`.
  2. **Non-compliant license detection**: Ingest an SBOM with a package using GPL-3.0-only (denied by default policy). Assert the report contains a group with `compliant: false` and `totalViolations >= 1`.
  3. **Transitive dependency inclusion**: Ingest an SBOM where package A depends on package B (transitive). Assert both packages appear in the license report groups.
  4. **Empty SBOM**: Ingest an SBOM with no packages. Assert the report returns empty `groups` array with `totalPackages: 0`.
  5. **Nonexistent SBOM**: Call the endpoint with a random UUID. Assert 404 response.
  6. **Multiple packages same license**: Ingest multiple packages with the same license. Assert they are grouped together in a single `LicenseGroup`.
- Use the SBOM ingestion flow from `modules/ingestor/src/graph/sbom/mod.rs` to set up test fixtures, following the pattern used in existing tests.
- Validate the JSON response structure matches the `LicenseReport` model from Task 1.

## Acceptance Criteria
- [ ] All 6 test scenarios are implemented and pass
- [ ] Tests use real PostgreSQL test database (not mocks)
- [ ] Tests follow existing patterns from `tests/api/sbom.rs`
- [ ] Test fixtures include SBOMs with diverse license combinations
- [ ] No test depends on external services or network access

## Test Requirements
- [ ] Test: basic report with compliant licenses returns correct groups
- [ ] Test: non-compliant license is flagged in report
- [ ] Test: transitive dependencies are included in report
- [ ] Test: empty SBOM returns empty report
- [ ] Test: nonexistent SBOM returns 404
- [ ] Test: multiple packages with same license are grouped together

## Dependencies
- Depends on: Task 4 — Add license report endpoint handler
