## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests cover the complete request-response cycle against a real PostgreSQL test database, verifying correct license grouping, compliance flag evaluation, transitive dependency inclusion, and error handling for edge cases.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data in the PostgreSQL test database, make HTTP requests to the endpoint, and assert on response status codes and body content.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests.
- Test data setup should create an SBOM with multiple packages having different licenses (some approved, some denied per the default policy) to verify grouping and compliance flag logic.
- Include a test case with transitive dependencies to verify the full dependency tree is walked.
- Include edge cases: SBOM with no packages, SBOM with all packages having the same license, SBOM with packages that have no license mapping.

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns, HTTP client configuration, and assertion patterns for SBOM-related endpoints
- `tests/api/advisory.rs` — Additional test pattern reference for entity-specific endpoint testing

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests verify correct license grouping in the response
- [ ] Tests verify compliance flags match the configured policy
- [ ] Tests verify transitive dependencies are included
- [ ] Tests verify error responses for invalid/missing SBOM IDs
- [ ] Tests cover edge cases (empty SBOM, single license, missing license data)

## Test Requirements
- [ ] Integration test: SBOM with mixed licenses returns correct grouping with appropriate compliance flags
- [ ] Integration test: SBOM with only approved licenses returns all groups as compliant
- [ ] Integration test: SBOM with denied licenses returns those groups as non-compliant
- [ ] Integration test: SBOM with transitive dependencies includes all packages in the report
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with no packages returns an empty groups array

## Dependencies
- Depends on: Task 3 — Add license report endpoint and register route
