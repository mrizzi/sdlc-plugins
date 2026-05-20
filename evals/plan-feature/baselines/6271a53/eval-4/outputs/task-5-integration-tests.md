# Task 5 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover compliant and non-compliant license scenarios, transitive dependency handling, empty SBOMs, and error cases. These tests hit a real PostgreSQL test database following the existing integration test patterns.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if needed (depending on test discovery configuration)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/` — see `sbom.rs` for the established test structure:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting an SBOM with known packages and licenses before running the report endpoint
- Test scenarios to cover:
  1. **All compliant**: SBOM with packages having only allowed licenses — all groups should have `compliant: true`
  2. **Mixed compliance**: SBOM with some allowed and some denied licenses — verify correct compliance flags per group
  3. **Transitive dependencies**: SBOM with a dependency tree — verify transitive packages are included and marked `transitive: true`
  4. **Empty SBOM**: SBOM with no packages — verify empty groups array is returned
  5. **Non-existent SBOM**: Request with invalid ID — verify 404 error response
  6. **Large SBOM performance**: SBOM with many packages — verify the response completes (this validates the query efficiency)
- Per constraints (docs/constraints.md) section 5.11: every test function must have a doc comment
- Per constraints (docs/constraints.md) section 5.12: non-trivial test functions must include given-when-then inline comments
- Per constraints (docs/constraints.md) section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrate the test setup pattern, database initialization, and assertion conventions
- `tests/api/advisory.rs` — Advisory endpoint tests show another example of the integration test pattern
- `tests/api/search.rs` — Search endpoint tests show how to verify JSON response shapes

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, and mixed license scenarios
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify error handling for invalid SBOM IDs
- [ ] Test functions have doc comments
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: SBOM with only allowed licenses returns all groups as compliant
- [ ] Integration test: SBOM with denied licenses returns those groups as non-compliant
- [ ] Integration test: transitive dependencies appear in the report with `transitive: true`
- [ ] Integration test: empty SBOM returns empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON shape matches the LicenseReport contract

## Verification Commands
- `cargo test --test api -- license_report` — runs the license report integration tests specifically

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
