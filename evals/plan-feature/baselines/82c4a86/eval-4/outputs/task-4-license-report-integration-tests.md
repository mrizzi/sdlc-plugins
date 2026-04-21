# Task 4 — Add integration tests for the license compliance report endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the license compliance report endpoint covering the full request lifecycle: setting up test data (SBOM with packages and license mappings), calling `GET /api/v2/sbom/{id}/license-report`, and verifying the response structure and compliance evaluation logic. Tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` -- it demonstrates how to set up a test PostgreSQL database, create test data (SBOMs, packages), make HTTP requests to endpoints, and assert on response status and body.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per CONVENTIONS.md Key Conventions.
- Test scenarios to cover:
  - SBOM with all compliant licenses (all groups have `compliant: true`)
  - SBOM with some non-compliant licenses (mixed compliance in report)
  - SBOM with only non-compliant licenses (all groups `compliant: false`)
  - SBOM with transitive dependencies contributing additional licenses
  - Empty SBOM (no packages) returning an empty groups array
  - Non-existent SBOM ID returning 404
- Set up test license policy data that matches the test scenarios (e.g., deny GPL-3.0, allow MIT/Apache-2.0).
- Per constraints.md section 5.9-5.10: check `tests/api/sbom.rs` for existing test patterns. If sibling tests use parameterized patterns, prefer parameterized tests for the scenario matrix; otherwise follow the existing style.
- Per constraints.md section 5.11: add a doc comment to every test function explaining what scenario it verifies.
- Per constraints.md section 5.12-5.13: add given-when-then inline comments to non-trivial test functions (those with distinct setup, action, and assertion phases). Omit for trivial single-assertion tests.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test structure, test database setup helpers, HTTP request patterns
- `tests/api/advisory.rs` — additional reference for integration test patterns and assertions

## Acceptance Criteria
- [ ] Integration tests cover compliant, non-compliant, mixed, empty, and not-found scenarios
- [ ] Tests verify both the HTTP status code and the response body structure
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests follow the existing integration test patterns in `tests/api/`
- [ ] Every test function has a doc comment
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Test: SBOM with all MIT-licensed packages returns all groups as compliant (200)
- [ ] Test: SBOM with a denied license (e.g., GPL-3.0) returns that group as non-compliant (200)
- [ ] Test: SBOM with no packages returns empty groups array (200)
- [ ] Test: Non-existent SBOM ID returns 404 status
- [ ] Test: Transitive dependencies appear in the license report groups
- [ ] Test: Mixed scenario with some compliant and some non-compliant license groups

## Verification Commands
- `cargo test --test api -- license_report` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
