# Task 5 — Add integration tests for the license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, verifying correct grouping, compliance evaluation, transitive dependency inclusion, and error handling. This ensures the endpoint behaves correctly across all expected scenarios including edge cases.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (Advisory endpoint tests).
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per the codebase convention.
- Tests hit a real PostgreSQL test database per the project convention.
- **Test scenarios to cover:**
  1. SBOM with packages under multiple license types — verify correct grouping
  2. SBOM with a denied license — verify `compliant: false` on the relevant group
  3. SBOM with only allowed licenses — verify all groups have `compliant: true`
  4. SBOM with transitive dependencies — verify transitive packages appear in the report
  5. Non-existent SBOM ID — verify 404 response
  6. SBOM with no packages — verify empty groups in response
  7. SBOM with packages that have no license data — verify graceful handling
- Per docs/constraints.md §5.11: Add a doc comment to every test function.
- Per docs/constraints.md §5.12: Add given-when-then inline comments to non-trivial test functions.
- Per docs/constraints.md §5.9: Consider parameterized tests for scenarios that exercise the same behavior with different license inputs (e.g., multiple allowed licenses, multiple denied licenses).

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; use as the direct template for test setup, database seeding, HTTP client usage, and assertion patterns.
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for additional test structure patterns.

## Acceptance Criteria
- [ ] All test scenarios pass against a real PostgreSQL test database
- [ ] Tests cover both success and error paths
- [ ] Tests verify the response JSON structure matches the expected schema
- [ ] Transitive dependency inclusion is explicitly tested

## Test Requirements
- [ ] Integration test: SBOM with multiple license types returns correctly grouped report
- [ ] Integration test: Denied license produces `compliant: false` flag
- [ ] Integration test: All-allowed licenses produce `compliant: true` for all groups
- [ ] Integration test: Transitive dependencies appear in the report
- [ ] Integration test: Non-existent SBOM returns 404
- [ ] Integration test: Empty SBOM returns empty groups
- [ ] Integration test: Packages without license data are handled gracefully

## Verification Commands
- `cargo test --test api license_report` — All license report integration tests pass

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
