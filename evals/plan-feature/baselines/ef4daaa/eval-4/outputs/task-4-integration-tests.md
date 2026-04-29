# Task 4 -- Add Integration Tests for License Report Endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests
should cover the full request/response cycle against a real PostgreSQL test database,
following the existing integration test patterns in `tests/api/`. This includes tests
for compliant SBOMs, non-compliant SBOMs, transitive dependency license resolution,
edge cases (empty SBOM, missing SBOM), and performance validation for large SBOMs.

## Files to Modify
- `tests/Cargo.toml` -- add any new test dependencies if needed

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the license report endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and
  `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - Set up test data (SBOM with packages and license mappings) before each test
- Test scenarios to cover:
  1. **Compliant SBOM**: all packages have licenses in the allowed list -- verify all
     groups have `compliant: true`
  2. **Non-compliant SBOM**: some packages have denied licenses -- verify those groups
     have `compliant: false`
  3. **Mixed SBOM**: combination of compliant and non-compliant licenses
  4. **Transitive dependencies**: package A depends on B depends on C -- C's license
     must appear in the report
  5. **Empty SBOM**: SBOM with no packages returns empty groups array
  6. **Missing SBOM**: non-existent SBOM ID returns 404
  7. **No policy violations**: when policy has empty denied list and empty allowed list,
     all licenses are compliant
- For performance testing: create a test fixture with ~1000 packages and verify the
  endpoint responds within a reasonable time (this can be a separate test marked with
  `#[ignore]` for CI if it's too slow for regular runs).
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial tests.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for SBOM endpoint integration test patterns, test
  database setup, and assertion style
- `tests/api/advisory.rs` -- reference for entity-specific integration test patterns
- `entity/src/sbom.rs` -- SBOM entity for test fixture setup
- `entity/src/package.rs` -- Package entity for test fixture setup
- `entity/src/package_license.rs` -- Package-License mapping for test fixture setup
- `entity/src/sbom_package.rs` -- SBOM-Package relationship for test fixture setup

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/license_report.rs`
- [ ] Tests cover all 7 scenarios listed in Implementation Notes
- [ ] All tests pass against the test database
- [ ] Tests follow the existing assertion pattern (`assert_eq!` on status codes)
- [ ] Test functions have doc comments
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant SBOM returns flagged groups with `compliant: false`
- [ ] Integration test: mixed SBOM returns correct compliance flags per group
- [ ] Integration test: transitive dependency licenses are included in the report
- [ ] Integration test: empty SBOM returns 200 with empty groups
- [ ] Integration test: missing SBOM returns 404
- [ ] Integration test: permissive policy (no restrictions) marks all licenses compliant

## Verification Commands
- `cargo test --test api -- license_report` -- all license report integration tests pass

## Dependencies
- Depends on: Task 3 -- Add License Report Endpoint
