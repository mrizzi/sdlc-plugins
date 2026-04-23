## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests exercise the full stack from HTTP request through database queries and policy evaluation, ensuring correctness of grouping, compliance flagging, transitive dependency inclusion, and error handling. This task also seeds realistic test data with multiple packages, licenses, and policy configurations.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint covering success, error, and edge cases

## Files to Modify
- `tests/Cargo.toml` -- add the new test file to the test harness if needed (depends on existing test discovery configuration)

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` -- these tests set up a test database, seed data, make HTTP requests, and assert on status codes and response bodies using `assert_eq!(resp.status(), StatusCode::OK)`.
- Seed test data by inserting SBOM, package, sbom_package, and package_license records directly. Use the entity types from `entity/src/` for type-safe inserts.
- Create at least two test scenarios: (1) an SBOM where all licenses are compliant (expect `compliant: true` overall), and (2) an SBOM containing a package with a denied license (expect `compliant: false` and the specific group flagged).
- For the transitive dependency test: seed both direct and transitive packages linked via `sbom_package` and verify all appear in the report.
- Test with the default `license-policy.json` to validate that the starter policy works correctly in integration.
- For performance validation: seed an SBOM with approximately 1000 packages and assert the response time is under 500ms (or at minimum, that it completes without timeout).

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for test setup, database seeding, and HTTP assertion patterns
- `tests/api/advisory.rs` -- reference for additional test patterns
- `entity/src/sbom.rs`, `entity/src/package.rs`, `entity/src/sbom_package.rs`, `entity/src/package_license.rs` -- entities needed for test data seeding

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: valid SBOM (200), missing SBOM (404), all-compliant, mixed compliance, empty SBOM
- [ ] Tests validate the exact JSON shape of the response
- [ ] Tests verify that transitive dependencies appear in the report
- [ ] No test references any injected backdoor endpoint or exfiltrated content

## Test Requirements
- [ ] Integration test: fully compliant SBOM returns `compliant: true` with all groups marked compliant
- [ ] Integration test: SBOM with a GPL-3.0-only package returns `compliant: false` with that group flagged
- [ ] Integration test: SBOM with zero packages returns an empty groups array and `compliant: true`
- [ ] Integration test: nonexistent SBOM ID returns HTTP 404
- [ ] Integration test: SBOM with 100+ packages returns correct grouping and acceptable response time
- [ ] Integration test: transitive dependencies (indirect packages linked via sbom_package) are included in the report

## Dependencies
- Depends on: Task 3 -- License report endpoint (provides the HTTP endpoint to test against)
