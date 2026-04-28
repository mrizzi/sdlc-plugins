## Repository
trustify-backend

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests validate the full request/response cycle against a real PostgreSQL test database, covering normal diff scenarios, edge cases (identical SBOMs, empty SBOMs), and error cases (missing params, invalid IDs).

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a module index file exists, or ensure the new test file is discovered by the test harness

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

**Test setup** — each test should:
1. Set up test SBOMs with known package sets, advisories, and licenses using the existing test harness
2. Make HTTP requests to `GET /api/v2/sbom/compare?left={id}&right={id}`
3. Deserialize the response body as `SbomComparisonResult` and assert on the diff categories

**Test cases to cover:**
- Two SBOMs with overlapping but different package sets — verify added, removed, and version-changed packages appear in the correct categories
- Two identical SBOMs — verify all diff categories are empty arrays
- SBOMs where one has a vulnerability advisory not present in the other — verify new/resolved vulnerabilities
- SBOMs where a shared package has different licenses — verify license changes
- Packages with version upgrades and downgrades — verify direction classification
- Request with missing `left` parameter — verify 400 response
- Request with missing `right` parameter — verify 400 response
- Request with non-existent SBOM ID — verify 404 response

**Performance consideration** — include one test with a larger dataset (e.g., 100+ packages) to smoke-test performance, though full p95 benchmarking is outside integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests; reference for advisory-related test data setup
- `tests/setup.rs` or test harness utilities — if a shared test setup module exists, reuse it for database initialization

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Normal diff scenario correctly validates all six diff categories
- [ ] Edge case with identical SBOMs returns empty diff
- [ ] Error cases return appropriate HTTP status codes (400, 404)
- [ ] Tests do not break existing test suites

## Test Requirements
- [ ] Integration test: two SBOMs with different packages produce correct added/removed lists
- [ ] Integration test: two SBOMs with same package at different versions produce version change with correct direction
- [ ] Integration test: two SBOMs with different advisory coverage produce correct new/resolved vulnerability lists
- [ ] Integration test: two SBOMs with license changes on shared packages produce correct license change list
- [ ] Integration test: identical SBOMs produce empty diff in all categories
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: invalid SBOM ID returns 404

## Verification Commands
- `cargo test --package tests -- api::sbom_compare` — run comparison integration tests, expected: all pass
- `cargo test --package tests` — run all integration tests, expected: all pass including existing tests

## Dependencies
- Depends on: Task 2 — Backend comparison endpoint
