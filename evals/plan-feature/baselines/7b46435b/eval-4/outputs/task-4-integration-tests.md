## Repository
trustify-backend

## Target Branch
main

## Description
Write integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Cover the main use cases: valid license report generation with grouped results, 404 for non-existent SBOMs, policy violation flagging for non-compliant licenses, transitive dependency inclusion, empty SBOM handling, and performance characteristics with larger package sets.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `tests/api/sbom_license_report.rs` -- integration tests for the license-report endpoint covering all test scenarios

## Files to Modify
- `tests/api/mod.rs` -- add `mod sbom_license_report;` to register the new test module (if a mod.rs exists; otherwise the test is auto-discovered)

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` (SBOM endpoint integration tests) for test structure, database setup, and assertion patterns. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the test suite.

Each test should:
1. Set up test data in the PostgreSQL test database (create SBOM, packages, license mappings, and optionally a policy config)
2. Make an HTTP request to `GET /api/v2/sbom/{id}/license-report`
3. Assert on the response status code and body

Test cases to implement:
- **Happy path**: SBOM with multiple packages across several licenses; verify groups are correctly formed and compliant flags match the policy
- **Non-existent SBOM**: request with a random UUID returns 404
- **Policy violation**: SBOM with packages using a denied license returns `compliant: false` for that group
- **Transitive dependencies**: SBOM with both direct and transitive dependencies; verify transitive packages are included and marked correctly
- **Empty SBOM**: SBOM with no packages returns an empty groups array
- **Multiple packages same license**: verify they are grouped together in a single `LicenseGroup`

Per CONVENTIONS.md: all handlers and service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `tests/api/sbom_license_report.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM endpoint integration tests; follow the same test setup, database fixtures, and assertion patterns
- `tests/api/advisory.rs` -- another endpoint test file demonstrating the established integration test structure

## Acceptance Criteria
- [ ] Integration test file `tests/api/sbom_license_report.rs` exists
- [ ] At least 5 test cases covering the scenarios listed above
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests use the established test patterns from the existing test suite

## Test Requirements
- [ ] Test: valid SBOM returns 200 with grouped license data and correct compliance flags
- [ ] Test: non-existent SBOM returns 404
- [ ] Test: SBOM with denied licenses returns non-compliant groups
- [ ] Test: transitive dependencies are included and marked as transitive
- [ ] Test: empty SBOM returns empty groups array
- [ ] Test: multiple packages with the same license are grouped together

## Verification Commands
- `cargo test -p trustify-tests sbom_license_report` -- all integration tests pass

## Dependencies
- Depends on: Task 3 -- Implement license-report REST endpoint
