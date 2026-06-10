## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, validating correct license grouping, policy compliance evaluation, transitive dependency handling, and error cases.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the existing integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
  - Set up test data (SBOM with packages and licenses) before each test
- Test data setup:
  1. Ingest a test SBOM with known packages and license data
  2. Configure a license policy with specific allowed/denied licenses
  3. Call the endpoint and verify the response
- Test scenarios should cover:
  - Happy path: SBOM with multiple license types, all compliant
  - Policy violation: SBOM containing a package with a denied license
  - Transitive dependencies: verify indirect packages appear in the report
  - Empty SBOM: no packages returns an empty groups array
  - Invalid SBOM ID: returns 404
  - Performance: optional benchmark test for 1000-package SBOM if the test framework supports it
- Per CONVENTIONS.md: follow the existing integration test patterns in `tests/api/`.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests for additional pattern reference
- `tests/api/search.rs` — existing search integration tests

## Acceptance Criteria
- [ ] Integration tests cover happy path with correct license grouping
- [ ] Integration tests verify policy compliance flags
- [ ] Integration tests verify transitive dependency inclusion
- [ ] Integration tests cover 404 for invalid SBOM ID
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: valid SBOM with MIT and Apache-2.0 packages returns two groups with correct package lists
- [ ] Test: SBOM with a GPL-3.0 package and a policy denying GPL-3.0 returns `compliant: false` for that group
- [ ] Test: SBOM with transitive dependencies includes indirect package licenses in the report
- [ ] Test: non-existent SBOM ID returns 404 status
- [ ] Test: SBOM with no packages returns empty groups array

## Verification Commands
- `cargo test -p trustify-tests -- license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint
