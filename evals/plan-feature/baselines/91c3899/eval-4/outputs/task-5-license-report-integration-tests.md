## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. The tests verify end-to-end behavior by hitting the endpoint against a real PostgreSQL test database with ingested SBOM and package-license data, covering compliant, non-compliant, and mixed license scenarios as well as edge cases.

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- Add the new test file to the test suite if needed (depends on test discovery configuration)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/` -- see `tests/api/sbom.rs` for SBOM endpoint tests as a direct reference for test setup, database seeding, HTTP request construction, and assertion style.
- Use the established pattern: `assert_eq!(resp.status(), StatusCode::OK)` for status code checks.
- Tests should seed the test database with:
  - An SBOM with packages that have only compliant licenses (expect all groups `compliant: true`)
  - An SBOM with packages that have non-compliant licenses (expect some groups `compliant: false`)
  - An SBOM with transitive dependencies to verify the full dependency tree is included
  - A nonexistent SBOM ID to verify 404 response
- Each test should set up its own license policy configuration (or use the default) to control compliance expectations.
- Tests hit a real PostgreSQL test database, consistent with the project's testing strategy.

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM endpoint integration tests; follow the same test setup, fixtures, and assertion patterns
- `tests/api/advisory.rs` -- Additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration test passes for an SBOM with only compliant licenses
- [ ] Integration test passes for an SBOM with non-compliant licenses flagged correctly
- [ ] Integration test verifies transitive dependencies appear in the report
- [ ] Integration test verifies 404 for nonexistent SBOM ID
- [ ] All tests pass in CI with the PostgreSQL test database

## Test Requirements
- [ ] Test: GET license report for SBOM with all-compliant licenses returns 200 with all groups `compliant: true`
- [ ] Test: GET license report for SBOM with denied licenses returns 200 with affected groups `compliant: false`
- [ ] Test: GET license report for SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Test: GET license report for nonexistent SBOM returns 404
- [ ] Test: GET license report for SBOM with no packages returns 200 with empty groups list

## Verification Commands
- `cargo test -p tests --test license_report` -- all license report integration tests pass

## Dependencies
- Depends on: Task 4 -- Add license report endpoint
