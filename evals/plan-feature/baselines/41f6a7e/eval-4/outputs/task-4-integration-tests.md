# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. These tests cover the end-to-end flow from HTTP request through service logic to database queries, validating correct grouping, compliance flagging, transitive dependency handling, and error cases. The tests exercise the endpoint against a real PostgreSQL test database following the established testing patterns.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add test module reference if needed (inspect existing structure to confirm)

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these show:
  - How to set up the test server and database
  - How to make HTTP requests and assert on status codes and response bodies
  - The `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test scenarios should include:
  - **Happy path**: SBOM with packages having various licenses (MIT, Apache-2.0, GPL-3.0), verify correct grouping and compliance flags per the test policy
  - **All compliant**: SBOM where all packages have allowed licenses, verify all groups have `compliant: true`
  - **Non-compliant present**: SBOM with at least one denied license, verify the group has `compliant: false`
  - **Transitive dependencies**: SBOM with a dependency tree (A depends on B depends on C), verify all packages including transitives appear in the report
  - **Unknown licenses**: packages with no license data, verify they appear in an "Unknown" group
  - **Non-existent SBOM**: request a report for an invalid SBOM ID, verify 404 response
  - **Empty SBOM**: SBOM with no packages, verify empty groups array
- Set up test data by ingesting test SBOMs with known package-license relationships before running assertions
- Per docs/constraints.md section 5.11: add a doc comment to every test function
- Per docs/constraints.md section 5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests showing test setup, request patterns, and assertion conventions
- `tests/api/advisory.rs` — additional reference for integration test patterns and test data setup
- `tests/api/search.rs` — reference for how search-related tests set up data and query endpoints

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, transitive dependency, unknown license, non-existent SBOM, and empty SBOM scenarios
- [ ] Tests follow the established testing patterns in the codebase
- [ ] Each test function has a doc comment explaining its purpose

## Test Requirements
- [ ] Integration test: SBOM with mixed licenses returns correctly grouped and flagged report
- [ ] Integration test: SBOM with only allowed licenses returns all-compliant report
- [ ] Integration test: SBOM with denied license returns non-compliant group
- [ ] Integration test: transitive dependencies are included in the report
- [ ] Integration test: packages without licenses appear as "Unknown" group
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: empty SBOM returns report with empty groups

## Verification Commands
- `cargo test --test api license_report` — all license report tests pass
- `cargo test` — full test suite passes with no regressions

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
