## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint and document the new API endpoint and license policy configuration. The integration tests exercise the full request-response cycle against a real PostgreSQL test database, covering compliant SBOMs, non-compliant SBOMs, edge cases, and performance requirements. The documentation covers the endpoint usage and the license policy configuration format.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license-report endpoint

## Files to Modify
- `tests/api/mod.rs` — Register the license_report test module (if a mod.rs exists; otherwise the test file is auto-discovered)
- `README.md` — Add section documenting the license compliance report endpoint and license policy configuration

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These files demonstrate:
- Setting up a test database with fixture data
- Making HTTP requests to the API
- Asserting response status codes with `assert_eq!(resp.status(), StatusCode::OK)`
- Validating response body structure

Test scenarios must cover:
1. **Happy path (compliant)**: Ingest an SBOM with packages that all have allowed licenses, call the license-report endpoint, verify all groups have `compliant: true`
2. **Non-compliant detection**: Ingest an SBOM with packages that have denied licenses, verify the affected groups have `compliant: false`
3. **Mixed compliance**: SBOM with both allowed and denied licenses, verify correct per-group compliance flags
4. **Transitive dependencies**: SBOM with dependency chains, verify transitive packages appear in the report
5. **Empty SBOM**: SBOM with no packages, verify empty groups response
6. **Non-existent SBOM**: Request a report for a non-existent ID, verify 404
7. **Performance assertion**: SBOM with ~1000 packages, verify response time is under the p95 target

Per CONVENTIONS.md §Key Conventions: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/license_report.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the test setup, fixture loading, and assertion patterns used in existing SBOM tests
- `tests/api/advisory.rs` — Additional reference for integration test structure and database fixture patterns

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, mixed, transitive, empty, and non-existent SBOM scenarios
- [ ] A performance test validates that report generation for a large SBOM completes within the p95 target
- [ ] README.md documents the license-report endpoint path, HTTP method, request parameters, and response shape
- [ ] README.md documents the license policy configuration format and how to customize it

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with compliant: true
- [ ] Integration test: non-compliant SBOM returns affected groups with compliant: false
- [ ] Integration test: mixed SBOM returns correct per-group compliance flags
- [ ] Integration test: transitive dependencies are included in the report
- [ ] Integration test: empty SBOM returns 200 with empty groups
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Performance test: SBOM with 1000 packages returns within 500ms

## Documentation Updates
- `README.md` — Add section describing the license compliance report endpoint (path, method, response schema) and the license policy configuration file format (JSON structure, allowed/denied lists, default policy behavior)

## Verification Commands
- `cargo test --test api license_report` — Run only the license report integration tests
- `cargo test --test api` — Run all integration tests to verify no regressions

## Dependencies
- Depends on: Task 3 — Add license report endpoint
