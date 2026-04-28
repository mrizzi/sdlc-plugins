# Task 4 — Add License Report Integration Tests

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint, covering the primary use cases: compliant SBOMs, non-compliant SBOMs, transitive dependency resolution, edge cases (empty SBOMs, missing licenses), and the CI/CD compliance gate scenario where the report is used to block builds with non-compliant licenses.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if tests are registered explicitly (verify against existing test module structure)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - Set up test data (SBOM with packages and license mappings) before calling the endpoint
- Test data setup should create:
  - An SBOM with packages having known licenses (both compliant and non-compliant per a test policy)
  - An SBOM with transitive dependencies to verify the full dependency tree is walked
  - An SBOM with no packages (edge case)
  - A package with no license data (edge case)
- Provide a test license policy configuration that explicitly allows some licenses and denies others, so compliance flags can be deterministically verified.
- Per constraints doc section 5.9/5.10: prefer parameterized tests if the project uses them (check sibling test files for patterns). If sibling tests do not use parameterized patterns, use individual test functions.
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same setup, assertion, and teardown patterns
- `tests/api/advisory.rs` — additional reference for integration test structure and database setup
- `entity/src/sbom_package.rs` — entity for creating test SBOM-package relationships
- `entity/src/package_license.rs` — entity for creating test package-license mappings

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover: compliant SBOM, non-compliant SBOM, mixed compliance, transitive dependencies, empty SBOM, missing license data
- [ ] Tests verify the response JSON shape matches the specification
- [ ] Tests verify compliance flags are correct based on the configured policy

## Test Requirements
- [ ] Integration test: SBOM with all compliant licenses returns all groups with `compliant: true`
- [ ] Integration test: SBOM with a denied license returns the corresponding group with `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes transitively-linked packages in the report
- [ ] Integration test: SBOM with no packages returns an empty `groups` array
- [ ] Integration test: Package with no license data is handled gracefully
- [ ] Integration test: Non-existent SBOM ID returns HTTP 404
- [ ] Integration test: CI/CD gate scenario — verify that the presence of any `compliant: false` group can be programmatically detected from the response

## Dependencies
- Depends on: Task 3 — Add License Report Endpoint
