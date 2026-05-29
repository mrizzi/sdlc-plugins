## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria from the feature specification. These tests exercise the full request lifecycle against a real PostgreSQL test database, verifying correct severity aggregation, deduplication, error handling, caching behavior, and threshold filtering. The tests follow the established integration test patterns in the `tests/api/` directory.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add test module reference if needed for the new test file

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These files demonstrate the test setup (database initialization, test data seeding), HTTP request construction, response assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`), and JSON response body parsing used throughout the test suite.
- Tests should use a real PostgreSQL test database as specified in the repository's Key Conventions: "Integration tests in `tests/api/` hit a real PostgreSQL test database."
- Test data setup should create SBOMs, advisories at various severity levels, and link them via the `sbom_advisory` join table to create realistic test scenarios.
- Include edge cases: SBOM with zero advisories, SBOM with duplicate advisory links (to verify deduplication), SBOM with advisories at every severity level.
- Verify JSON response shape explicitly: check that all expected fields (`critical`, `high`, `medium`, `low`, `total`) are present with correct integer types.
- Per docs/constraints.md section 5 (Code Change Rules): follow patterns in Implementation Notes (constraint 5.3). Each test function must include a doc comment (constraint 5.11). Non-trivial tests must include given-when-then inline comments (constraint 5.12).

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests showing test setup patterns, database seeding, and response assertions
- `tests/api/advisory.rs` — Advisory endpoint integration tests demonstrating advisory test data creation
- `tests/api/search.rs` — Another integration test file showing the test module conventions

## Acceptance Criteria
- [ ] Integration test file `tests/api/advisory_summary.rs` exists with comprehensive test coverage
- [ ] Tests cover: correct severity counts, deduplication, empty advisories, non-existent SBOM (404), JSON response shape
- [ ] Tests cover threshold filtering behavior (with and without threshold parameter)
- [ ] All tests pass against the PostgreSQL test database
- [ ] Test functions include doc comments and given-when-then inline comments for non-trivial tests

## Test Requirements
- [ ] Test: GET advisory-summary for SBOM with multiple advisories at different severity levels returns correct counts
- [ ] Test: GET advisory-summary deduplicates advisories linked multiple times to the same SBOM
- [ ] Test: GET advisory-summary for SBOM with zero advisories returns all zeros
- [ ] Test: GET advisory-summary for non-existent SBOM returns 404
- [ ] Test: GET advisory-summary response contains all expected JSON fields with correct types
- [ ] Test: GET advisory-summary with threshold parameter filters counts correctly
- [ ] Test: GET advisory-summary with invalid threshold returns 400

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 5 — Add threshold query parameter support
