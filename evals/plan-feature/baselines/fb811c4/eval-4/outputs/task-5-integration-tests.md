## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the full request-response cycle against a test PostgreSQL database, following the existing test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration test module with the following test cases:
  1. **test_license_report_success** — Ingest an SBOM with packages having various licenses (MIT, Apache-2.0, GPL-3.0-only), call the endpoint, verify the response contains correct license groups with accurate compliance flags
  2. **test_license_report_all_compliant** — Ingest an SBOM where all packages have approved licenses, verify all groups have `compliant: true` and summary shows zero non-compliant
  3. **test_license_report_non_compliant_flagged** — Ingest an SBOM with at least one denied license, verify the group is flagged with `compliant: false`
  4. **test_license_report_transitive_deps** — Ingest an SBOM with a dependency tree, verify transitive dependencies appear in the report with `is_transitive: true`
  5. **test_license_report_not_found** — Call the endpoint with a non-existent SBOM ID, verify 404 response
  6. **test_license_report_empty_sbom** — Ingest an SBOM with no packages, verify the report returns an empty groups list and zeroed summary

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if test modules are explicitly registered (check existing test config)

## Implementation Notes
- Follow the existing test pattern in `tests/api/sbom.rs` for test setup, database initialization, and HTTP client configuration
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with other API tests
- Test data setup: ingest test SBOMs with known packages and licenses before each test case
- Deserialize the response body into `LicenseReport` to validate the structure and field values
- Use a test-specific license policy file or configure the policy via test setup to control which licenses are approved/denied
- Performance: while not a strict integration test, consider adding a test with a larger dataset (hundreds of packages) to sanity-check response time if feasible in the test environment

Per CONVENTIONS.md: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs`.

## Acceptance Criteria
- All six test cases pass against a test PostgreSQL database
- Tests validate both the HTTP status codes and the response body structure/content
- Test coverage includes success, not-found, empty, and compliance scenarios
- Tests are independent and can run in any order

## Test Requirements
- This task IS the test task — all tests listed above must be implemented and passing
- Tests should clean up test data or use isolated test transactions to avoid interference

## Dependencies
- Depends on: Task 4 — License Report Endpoint (needs the endpoint to be available for integration testing)

[sdlc-workflow] Description digest: sha256-md:72a5c4314f030872102dcaa7f4be2afc07b8fdbdf8f61db89206a9540eacad45
