# Task 5 — Add integration tests for license compliance report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. The tests verify end-to-end behavior including correct license grouping, compliance flagging, transitive dependency inclusion, error handling, and edge cases. These tests exercise the full stack from HTTP request through service to database against a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint covering happy path, compliance scenarios, edge cases, and error handling

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (check if tests are auto-discovered or explicitly listed)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data by ingesting an SBOM with known package-license data before each test
- Test scenarios should cover:
  1. **Happy path**: SBOM with packages having known licenses, verify correct grouping and compliance flags
  2. **Non-compliant licenses**: SBOM with packages that have denied licenses, verify `compliant: false` on matching groups
  3. **Mixed compliance**: SBOM with both compliant and non-compliant licenses in different groups
  4. **Transitive dependencies**: SBOM with a dependency tree, verify transitive packages are included with `transitive: true`
  5. **Empty SBOM**: SBOM with no packages returns `{ "groups": [] }`
  6. **Non-existent SBOM**: request for non-existent SBOM ID returns 404 status
- Test data setup: create test SBOMs using the ingestion infrastructure in `modules/ingestor/src/graph/sbom/mod.rs` or by directly inserting into the test database using SeaORM entities from `entity/src/`.
- Use a test-specific license policy configuration (not the default one) to control test conditions precisely.
- Verify response JSON structure matches the `LicenseReportResponse` schema: `{ "groups": [{ "license": "...", "packages": [...], "compliant": true/false }] }`.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns (test setup, HTTP client usage, assertions, DB fixtures)
- `tests/api/advisory.rs` — Advisory endpoint integration test patterns for additional reference
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion for setting up test data with known package-license data
- `entity/src/package_license.rs` — Direct entity insertion for test fixtures

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, mixed, transitive, empty, and 404 scenarios
- [ ] Tests use the established integration test patterns from the `tests/api/` directory
- [ ] No flaky tests — each test is deterministic with controlled test data

## Test Requirements
- [ ] Integration test: valid SBOM with approved licenses returns 200 with all groups as `compliant: true`
- [ ] Integration test: SBOM with denied licenses returns the relevant groups with `compliant: false`
- [ ] Integration test: transitive dependencies appear in the report with `transitive: true`
- [ ] Integration test: SBOM with no packages returns 200 with `{ "groups": [] }`
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response includes all packages from the SBOM (no packages missing)

## Verification Commands
- `cargo test --test api -- license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

[sdlc-workflow] Description digest: sha256-md:d81f63c4871e9caa920e2e5612d22d529720eae62ac51c236a660080a9628ed1