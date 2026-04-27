# Task 3 — Integration tests for SBOM comparison endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint. Tests must cover the full request-response cycle against a real PostgreSQL test database, verifying correct diff computation across all six diff categories, error handling for edge cases, and performance characteristics for large SBOMs.

## Files to Create
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` or test harness entry point — register the new test module (if a module registry pattern is used)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — this file demonstrates the test setup, database seeding, HTTP request construction, and assertion patterns used in the project.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, consistent with existing tests.
- Test data setup: seed the test database with two SBOMs that have known, controlled differences across all six diff categories. This requires inserting SBOM records, package records with SBOM-package links (`sbom_package` join table), advisory records with SBOM-advisory links (`sbom_advisory` join table), and package-license records (`package_license` mapping).
- Test categories to cover:
  1. **Happy path**: two SBOMs with differences in all six categories — verify each section of the response
  2. **Empty diff**: two identical SBOMs (or same SBOM packages replicated) — verify all diff sections are empty arrays
  3. **Missing parameters**: omit `left`, omit `right`, omit both — verify 400 responses
  4. **Non-existent SBOMs**: provide IDs that don't exist — verify 404 response
  5. **Same ID**: provide the same ID for both `left` and `right` — verify 400 response
  6. **Large SBOM performance**: seed two SBOMs with ~500 packages each and verify the response completes (regression guard for the p95 < 1s requirement)
- Entity references for test data seeding: `entity/src/sbom.rs`, `entity/src/package.rs`, `entity/src/sbom_package.rs`, `entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, `entity/src/package_license.rs`.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, client construction, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory-related test data seeding
- `entity/src/sbom.rs` — SBOM entity for test data creation
- `entity/src/sbom_package.rs` — join table entity for linking packages to SBOMs in test setup

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Happy path test verifies correct counts and content for all six diff categories
- [ ] Error cases (missing params, non-existent IDs, same ID) are tested and return correct status codes
- [ ] Empty diff case is tested (comparing identical SBOM contents)
- [ ] Large SBOM test verifies response completes without timeout

## Test Requirements
- [ ] Integration test: happy path with known diff across all six categories returns correct SbomComparisonResult
- [ ] Integration test: comparing SBOMs with identical packages returns empty arrays in all sections
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: non-existent left SBOM ID returns 404
- [ ] Integration test: non-existent right SBOM ID returns 404
- [ ] Integration test: same ID for left and right returns 400
- [ ] Integration test: large SBOM comparison (~500 packages each) completes successfully

## Verification Commands
- `cargo test -p trustify-tests -- sbom_compare` — all comparison integration tests pass

## Dependencies
- Depends on: Task 2 — SBOM comparison REST endpoint
