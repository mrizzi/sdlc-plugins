## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license report endpoint that cover the full request-response cycle against a real PostgreSQL test database. These tests validate the end-to-end behavior of the license compliance reporting feature including compliant SBOMs, non-compliant SBOMs, transitive dependency resolution, empty SBOMs, and automated compliance gate scenarios (CI/CD pipeline use case).

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint following the existing test patterns in `tests/api/`

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if needed for test discovery

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Set up test data by ingesting an SBOM with known packages and license data before running the license report tests. Reuse existing test utilities for database setup.
- Create a test license policy JSON file in the test fixtures with known allowed and denied licenses to ensure deterministic test outcomes.
- Test scenarios should cover:
  - A fully compliant SBOM (all packages have allowed licenses)
  - A non-compliant SBOM (at least one package has a denied license)
  - An SBOM with transitive dependencies where a transitive package has a non-compliant license
  - An SBOM with no packages (empty groups)
  - Requesting a license report for a non-existent SBOM ID (404)
  - CI/CD gate scenario: verify the response structure allows programmatic compliance checking (check that `non_compliant_count` and per-group `compliant` fields are present and correct)
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests demonstrating the test setup, database fixture, and assertion patterns to follow
- `tests/api/advisory.rs` — Additional integration test examples showing request construction and response parsing patterns

## Acceptance Criteria
- [ ] Integration tests exist for all specified scenarios (compliant, non-compliant, transitive, empty, 404, CI/CD gate)
- [ ] Tests use the existing test infrastructure and PostgreSQL test database
- [ ] Tests follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in sibling test files
- [ ] All tests pass when run with `cargo test --test api`
- [ ] Test data setup includes known license assignments for deterministic results

## Test Requirements
- [ ] Integration test: fully compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant SBOM returns at least one group with `compliant: false` and correct `non_compliant_count`
- [ ] Integration test: transitive dependency with non-compliant license is detected and flagged
- [ ] Integration test: SBOM with no packages returns empty groups and zero counts
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: response structure supports programmatic compliance checking (verify `non_compliant_count` field presence and accuracy)

## Verification Commands
- `cargo test --test api -- license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint
