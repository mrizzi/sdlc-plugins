## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the end-to-end flow: ingesting an SBOM with packages and license data, calling the license report endpoint, and verifying the response structure and compliance flags. This ensures the report correctly groups packages by license, includes transitive dependencies, and evaluates policy compliance.

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create
- `tests/api/license_report.rs` — integration tests for `GET /api/v2/sbom/{id}/license-report`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Each test should set up its own test data by inserting SBOM, package, and package_license records, then call the endpoint and verify the response.
- Register the new test file in `tests/api/` following the module convention used by `sbom.rs`, `advisory.rs`, and `search.rs`.
- Test scenarios to cover:
  1. **All compliant**: SBOM with packages under MIT and Apache-2.0 licenses, policy allows both. Expect all groups with `compliant: true`.
  2. **Non-compliant detected**: SBOM with a package under GPL-3.0, policy denies GPL-3.0. Expect that group with `compliant: false`.
  3. **Transitive dependencies included**: SBOM with a direct dependency (MIT) that has a transitive dependency (BSD-3-Clause). Both should appear in the report.
  4. **Empty SBOM**: SBOM with no packages. Expect `{ groups: [] }`.
  5. **Non-existent SBOM**: Request with an invalid SBOM ID. Expect 404 response.
  6. **Multiple packages same license**: Several packages all under MIT. Expect a single MIT group containing all packages.
- Per docs/constraints.md 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., the compliant/non-compliant scenarios could be parameterized).
- Per docs/constraints.md 5.11: add a doc comment to every test function.
- Per docs/constraints.md 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, database initialization, and assertion patterns
- `tests/api/advisory.rs` — another integration test file demonstrating the test structure convention; reference for how to organize multiple related test cases
- `entity/src/sbom_package.rs` — entity for creating SBOM-package relationships in test setup
- `entity/src/package_license.rs` — entity for creating package-license mappings in test setup

## Acceptance Criteria
- [ ] Integration tests exist for all 6 scenarios listed above
- [ ] Tests pass against a real PostgreSQL test database
- [ ] Tests verify both HTTP status codes and response body structure
- [ ] Non-compliant licenses are correctly flagged in test assertions
- [ ] Transitive dependency test verifies deep dependency tree traversal
- [ ] All test functions have doc comments
- [ ] Non-trivial tests have given-when-then inline comments

## Test Requirements
- [ ] Test: all-compliant SBOM returns all groups with `compliant: true`
- [ ] Test: SBOM with denied license returns group with `compliant: false`
- [ ] Test: transitive dependencies appear in the report groups
- [ ] Test: empty SBOM returns empty groups array
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: multiple packages with same license are grouped together

## Verification Commands
- `cargo test --test api -- license_report` — expected: all 6 license report integration tests pass

## Dependencies
- Depends on: Task 3 — License report endpoint
