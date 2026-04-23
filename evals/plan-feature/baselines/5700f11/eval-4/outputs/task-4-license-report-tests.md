## Repository
trustify-backend

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint, verifying correct behavior for normal SBOMs, edge cases (empty SBOM, unknown licenses), and error cases (non-existent SBOM). These tests ensure the entire license compliance report feature works end-to-end against a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` -- Integration test file for the license report endpoint

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, HTTP client usage, and assertion style.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the existing test files.
- Test setup should:
  1. Ingest a test SBOM with known packages and licenses (reuse or mirror the ingestion patterns from existing test fixtures)
  2. Ensure the test SBOM has packages with a mix of compliant and non-compliant licenses
- The integration test module should be added to the test harness (ensure `tests/Cargo.toml` includes the new test file if needed).

## Reuse Candidates
- `tests/api/sbom.rs` -- Reference for test setup, SBOM ingestion in tests, and HTTP assertion patterns
- `tests/api/advisory.rs` -- Additional reference for integration test structure and database fixture setup

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover the happy path, edge cases, and error cases listed in Test Requirements

## Test Requirements
- [ ] Integration test: GET license report for an SBOM with mixed licenses returns correct groupings and compliance flags
- [ ] Integration test: GET license report for an SBOM with only compliant licenses returns all groups with `compliant: true`
- [ ] Integration test: GET license report for an SBOM with packages having no license data includes an "Unknown" group marked non-compliant
- [ ] Integration test: GET license report for a non-existent SBOM ID returns 404
- [ ] Integration test: GET license report for an SBOM with zero packages returns an empty groups array
- [ ] Integration test: verify response structure matches expected JSON schema (`groups` array with `license`, `packages`, `compliant` fields)

## Verification Commands
- `cargo test -p trustify-tests --test license_report` -- All license report integration tests pass

## Dependencies
- Depends on: Task 3 -- License report endpoint (provides the endpoint under test)
