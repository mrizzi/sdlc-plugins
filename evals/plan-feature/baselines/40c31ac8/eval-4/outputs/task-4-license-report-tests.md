## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the main scenarios: a successful report with mixed compliant and non-compliant licenses, an SBOM with all licenses compliant, an SBOM with no packages, and a request for a non-existent SBOM ID.

## Files to Create
- `tests/api/sbom_license_report.rs` — integration tests for the license report endpoint

## Implementation Notes
Follow the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

Each test should:
1. Set up test data by ingesting an SBOM with packages and license associations
2. Call `GET /api/v2/sbom/{id}/license-report`
3. Assert on the response status code and body content

Test cases:
- **Happy path with mixed compliance**: Ingest an SBOM with packages under MIT (compliant) and GPL-3.0 (non-compliant per a test policy). Assert the report contains two groups, correct package counts, and the GPL-3.0 group has `compliant: false`.
- **All compliant**: Ingest an SBOM where all packages use compliant licenses. Assert `non_compliant_count` is 0 and all groups have `compliant: true`.
- **Empty SBOM**: Ingest an SBOM with no packages. Assert the report returns an empty `groups` array with `total_packages: 0`.
- **Non-existent SBOM**: Request a license report for a random UUID. Assert HTTP 404 response.
- **Transitive dependencies**: Ingest an SBOM with a dependency tree. Assert that transitive dependency licenses appear in the report groups.

Per CONVENTIONS.md §Error Handling: verify that error responses use the `AppError` format with appropriate status codes and context messages. Applies: task creates `tests/api/sbom_license_report.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Test Patterns: use the integration test patterns from `tests/api/` with real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)` assertions. Applies: task creates `tests/api/sbom_license_report.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint test setup, test database initialization, and assertion patterns
- `tests/api/advisory.rs` — reference for integration test structure and HTTP client usage

## Acceptance Criteria
- [ ] At least 5 test cases covering the scenarios listed above
- [ ] Tests use real PostgreSQL test database (not mocks)
- [ ] Tests assert on both HTTP status codes and response body content
- [ ] All tests pass (`cargo test -p trustify-tests`)

## Test Requirements
- [ ] Happy path test with mixed compliant and non-compliant licenses
- [ ] All-compliant licenses test
- [ ] Empty SBOM test (no packages)
- [ ] Non-existent SBOM ID returns 404
- [ ] Transitive dependency licenses are included in the report

## Verification Commands
- `cargo test -p trustify-tests` — all tests pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
