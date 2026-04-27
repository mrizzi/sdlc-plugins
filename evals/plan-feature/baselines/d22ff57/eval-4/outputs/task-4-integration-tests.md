# Task 4 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, following the existing integration test patterns in `tests/api/`. This task adds thorough edge-case coverage beyond the basic happy-path tests included with the endpoint task.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering multiple scenarios: compliant SBOM, non-compliant SBOM, mixed compliance, transitive dependencies, empty SBOM, large SBOM performance, and invalid SBOM ID.

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (likely no changes needed if the existing test infrastructure covers it).

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Use the same test database setup, HTTP client construction, and assertion style (`assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Test data setup: create SBOM records with known packages and licenses in the test database before calling the endpoint. Include packages with a mix of allowed, denied, and unknown licenses.
- Transitive dependency test: set up a package dependency chain (A depends on B depends on C) and verify that the report includes licenses from all levels of the dependency tree.
- Performance test: create an SBOM with 1000 packages and verify the endpoint responds within 500ms (p95 requirement). Use a simple timing assertion or benchmark.
- Each test function must have a doc comment explaining its purpose, per constraints doc section 5.11.
- Non-trivial tests must include given-when-then inline comments to delineate setup, action, and assertion phases, per constraints doc section 5.12.
- Consider using parameterized tests where multiple scenarios exercise the same behavior with different license policy configurations, per constraints doc section 5.9 — but only if existing tests in `tests/api/` use parameterized patterns (do not introduce new test patterns per section 5.10).

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow test setup and assertion patterns.
- `tests/api/advisory.rs` — additional integration test examples for the assertion style.

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover: compliant SBOM, non-compliant SBOM, mixed compliance, transitive deps, empty SBOM, non-existent SBOM (404), and performance (p95 < 500ms for 1000 packages)
- [ ] Test assertions verify both HTTP status codes and response body structure
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions include given-when-then inline comments

## Test Requirements
- [ ] Test: SBOM with all allowed licenses returns all groups with `compliant: true`
- [ ] Test: SBOM with a denied license returns the corresponding group with `compliant: false`
- [ ] Test: SBOM with a mix of allowed and denied licenses returns correct per-group compliance flags
- [ ] Test: SBOM with transitive dependencies includes all dependency licenses in the report
- [ ] Test: SBOM with zero packages returns an empty groups array
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: SBOM with 1000 packages responds within 500ms

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
