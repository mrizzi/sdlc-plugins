# Task 5 -- License Report Integration Tests

## Repository
trustify-backend

## Description
Create comprehensive integration tests for the license report endpoint that validate the full request-response cycle against a real PostgreSQL test database. Tests should cover compliant and non-compliant scenarios, transitive dependency handling, error cases, and performance characteristics, following the existing integration test patterns in the repository.

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- Add any needed test dependencies (if not already present)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
  - Set up test data (SBOM with packages and license mappings) before each test
- Test scenarios to implement:
  1. **All-compliant SBOM**: Create an SBOM with packages that all have allowed licenses, verify all groups have `compliant: true` and overall `compliant: true`
  2. **Non-compliant SBOM**: Create an SBOM with at least one package under a denied license, verify the offending group has `compliant: false` and overall `compliant: false`
  3. **Mixed compliance**: SBOM with both compliant and non-compliant licenses, verify correct per-group flags
  4. **Transitive dependencies**: Create an SBOM with a dependency chain (A depends on B depends on C), verify all packages in the chain appear in the report
  5. **Missing SBOM (404)**: Request a report for a non-existent SBOM ID, verify HTTP 404
  6. **Empty SBOM**: SBOM with no packages, verify the report returns with an empty groups list and `compliant: true`
  7. **Performance**: Generate an SBOM with 1000 packages and verify the report completes within 500ms
- Per constraints doc section 5.9: prefer parameterized tests when multiple cases exercise the same behavior with different inputs (e.g., the compliant vs non-compliant scenarios could be parameterized if the project uses that pattern)
- Per constraints doc section 5.10: check sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) for whether parameterized tests are used before introducing them
- Per constraints doc section 5.11: add a doc comment to every test function
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow the same setup, request, and assertion patterns
- `tests/api/advisory.rs` -- additional reference for integration test structure
- `tests/api/search.rs` -- additional reference for how test data is seeded and queries are validated

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover both compliant and non-compliant license scenarios
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify correct HTTP error codes for missing SBOMs
- [ ] Tests follow existing patterns in `tests/api/`
- [ ] Each test function has a doc comment

## Test Requirements
- [ ] Integration test: all-compliant SBOM returns fully compliant report
- [ ] Integration test: non-compliant SBOM correctly flags denied licenses
- [ ] Integration test: mixed compliance SBOM has correct per-group flags
- [ ] Integration test: transitive dependencies appear in the report
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: empty SBOM returns empty compliant report
- [ ] Performance test: 1000-package SBOM report completes within 500ms

## Dependencies
- Depends on: Task 4 -- License Report Endpoint (endpoint must be registered for integration tests to call)
