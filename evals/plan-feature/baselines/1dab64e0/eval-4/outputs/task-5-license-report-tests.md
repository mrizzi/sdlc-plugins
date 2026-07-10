## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint
(`GET /api/v2/sbom/{id}/license-report`). These tests exercise the full request path
against a real PostgreSQL test database, verifying correct license grouping, transitive
dependency inclusion, compliance flagging, and error handling.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add the test module if needed for compilation

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` for test structure,
database setup, assertion style (`assert_eq!(resp.status(), StatusCode::OK)`), and
test data preparation.

Each test should:
1. Set up test data (SBOM with packages and license mappings) in the test database
2. Make an HTTP request to the license report endpoint
3. Assert on the response status and body structure

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test
database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the integration test pattern for SBOM endpoints including test database setup, HTTP request construction, and response assertion
- `tests/api/advisory.rs` — demonstrates another integration test pattern for comparison

## Acceptance Criteria
- [ ] Integration tests cover: compliant SBOM, non-compliant SBOM, mixed compliance, empty SBOM, non-existent SBOM
- [ ] Tests verify the response JSON structure matches the `LicenseReport` schema
- [ ] Tests verify transitive dependency licenses are included in the report
- [ ] Tests verify compliance flags match the configured policy
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: SBOM with all permissive licenses returns all groups with `compliant: true`
- [ ] Test: SBOM with a denied license returns that group with `compliant: false`
- [ ] Test: SBOM with transitive dependencies includes transitive package licenses in groups
- [ ] Test: Non-existent SBOM ID returns 404 status
- [ ] Test: SBOM with no packages returns an empty `groups` array
- [ ] Test: SBOM with packages having multiple licenses groups them correctly

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report service
- Depends on: Task 4 — Add license report endpoint
