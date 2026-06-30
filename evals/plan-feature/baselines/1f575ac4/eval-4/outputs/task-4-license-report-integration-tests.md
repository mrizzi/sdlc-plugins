# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests exercise the full stack from HTTP request through the service layer and database, validating the complete license report workflow including compliance checking, grouping, and error cases. The tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test configuration if required by the project's test setup

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — it demonstrates how to set up the test database, create test data, make HTTP requests to the API, and assert on response status and body.
- Test assertions should use the `assert_eq!(resp.status(), StatusCode::OK)` pattern as established in the test codebase.
- Test data setup: create an SBOM with associated packages and license data using the existing entity/service layer. Ensure test packages have a mix of compliant and non-compliant licenses to validate the compliance checking logic.
- Include tests for the CI/CD pipeline use case (UC-2): verify that the response structure allows a consumer to programmatically check for `compliant: false` in any group.
- The tests hit a real PostgreSQL test database per the project's testing conventions.

## Reuse Candidates
- `tests/api/sbom.rs` — Demonstrates the integration test setup pattern: database initialization, test data creation, HTTP request execution, and response assertion.
- `tests/api/advisory.rs` — Another integration test example showing the established test patterns.
- `tests/api/search.rs` — Shows additional test patterns for API endpoint testing.

## Acceptance Criteria
- [ ] Integration tests exist in `tests/api/license_report.rs`
- [ ] Tests cover the happy path: valid SBOM with packages returns grouped license data
- [ ] Tests cover the compliance logic: mix of compliant and non-compliant licenses produces correct `compliant` flags
- [ ] Tests cover the error case: non-existent SBOM ID returns an error response
- [ ] Tests cover the empty case: SBOM with no packages returns an empty groups array
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: valid SBOM with MIT and Apache-2.0 licensed packages returns 200 with two groups, both `compliant: true`
- [ ] Integration test: valid SBOM with a non-compliant license returns 200 with that group having `compliant: false`
- [ ] Integration test: non-existent SBOM ID returns appropriate error status (404 or similar)
- [ ] Integration test: SBOM with no packages returns 200 with an empty `groups` array
- [ ] Integration test: response JSON structure matches the documented shape (`groups[].license`, `groups[].packages`, `groups[].compliant`)

## Verification Commands
- `cargo test --test license_report` — All license report integration tests pass
- `cargo test` — All tests (existing and new) pass with no regressions

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
