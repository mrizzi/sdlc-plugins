# Task 8 — Add integration tests for the SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint, covering success cases, error cases, and edge cases. These tests validate the full request-response lifecycle through Axum, using the same real PostgreSQL test database pattern as existing endpoint tests.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test module if required by the test structure

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Tests hit a real PostgreSQL test database.
  - Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
  - Set up test fixtures by ingesting two SBOMs with known package and advisory differences.
- Test scenarios to cover:
  1. **Happy path**: Compare two SBOMs with known differences — verify all six diff categories in the response.
  2. **Identical SBOMs**: Compare an SBOM with itself — all diff categories should be empty.
  3. **Missing query param**: Call without `left` or `right` — expect 400.
  4. **Invalid SBOM ID**: Call with a non-existent ID — expect 404.
  5. **Large diff**: Create SBOMs with many package differences to verify performance does not degrade (optional, can be a benchmark).
- Test data setup: ingest two SBOMs with:
  - Packages unique to each (tests added/removed)
  - Packages with different versions (tests version changes)
  - Packages with different licenses (tests license changes)
  - Advisories unique to each (tests new/resolved vulnerabilities)

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration test pattern to follow for test structure and assertions
- `tests/api/advisory.rs` — existing advisory endpoint test pattern, useful for setting up advisory test data

## Acceptance Criteria
- [ ] Integration tests exist for the comparison endpoint in `tests/api/sbom_compare.rs`
- [ ] Happy path test verifies all six diff categories return correct data
- [ ] Error cases (missing params, invalid IDs) are tested
- [ ] Edge case (self-comparison) returns empty diffs
- [ ] All tests pass against the test database

## Test Requirements
- [ ] At least 5 integration test cases covering the scenarios listed in Implementation Notes
- [ ] Test data fixtures create realistic SBOM pairs with known differences across all diff categories

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison endpoint
