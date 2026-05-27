## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint, covering compliant SBOMs, non-compliant SBOMs, transitive dependency handling, empty SBOMs, and performance validation for large SBOMs. These tests hit the real PostgreSQL test database following the established integration test patterns.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test configuration if required by the project structure

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data in the PostgreSQL test database before each test
  - Clean up test data after each test
- Test scenarios to cover:
  1. **Compliant SBOM**: Ingest an SBOM with packages that all have allowed licenses, verify all groups have `compliant: true`
  2. **Non-compliant SBOM**: Ingest an SBOM with packages that include denied licenses, verify the correct groups have `compliant: false`
  3. **Mixed licenses**: SBOM with both compliant and non-compliant license groups
  4. **Transitive dependencies**: SBOM with a dependency tree, verify that transitive dependency licenses appear in the report
  5. **Empty SBOM**: SBOM with no packages, verify empty groups array is returned
  6. **Non-existent SBOM**: Request report for an ID that does not exist, verify 404
  7. **Large SBOM performance**: SBOM with 1000 packages, verify response time is within acceptable bounds (p95 < 500ms)
- Per docs/constraints.md §5.11: add a doc comment to every test function
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions
- Per docs/constraints.md §5.9: consider parameterized tests for the compliant/non-compliant/mixed scenarios if the test setup is similar

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the integration test setup pattern, database fixtures, and assertion conventions for SBOM endpoints
- `tests/api/advisory.rs` — another example of the integration test pattern for reference
- `tests/api/search.rs` — shows the test structure used in this project

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, mixed, transitive, empty, and non-existent SBOM scenarios
- [ ] Performance test verifies acceptable response time for 1000-package SBOMs
- [ ] Tests follow the established patterns from existing integration tests

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant SBOM returns correct groups with `compliant: false`
- [ ] Integration test: mixed license SBOM returns correct compliance flags per group
- [ ] Integration test: transitive dependencies are included in license groups
- [ ] Integration test: empty SBOM returns empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: 1000-package SBOM report completes within 500ms

## Verification Commands
- `cargo test --test api license_report` — run the license report integration tests

## Dependencies
- Depends on: Task 4 — License report endpoint

[sdlc-workflow] Description digest: sha256:5851ab34f1c65ce397fa71e8e38a23ab969b3e34c8fa1f56554e10b4436b036a
