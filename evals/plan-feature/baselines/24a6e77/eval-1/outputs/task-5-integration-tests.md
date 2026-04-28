# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint in the existing test suite. These tests must cover the full request-response lifecycle against a real PostgreSQL test database, verifying correct severity aggregation, deduplication, 404 handling, threshold filtering, and response shape. The tests serve as the primary verification that all preceding tasks work together correctly end-to-end.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixtures, HTTP client usage, and assertion style
- Tests should use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns consistent with the existing test files
- Test data setup: create SBOM entries, advisory entries with different severity levels, and link them via the `sbom_advisory` join table — use the existing test helper patterns from sibling test files
- For deduplication testing: create a scenario where the same advisory (same advisory ID) is linked to an SBOM multiple times and verify it is counted only once
- For threshold testing: create an SBOM with advisories across all severity levels and verify that each threshold value filters correctly
- Per constraints (Section 5.11): add a doc comment to every test function
- Per constraints (Section 5.12): add given-when-then inline comments to non-trivial test functions with distinct setup, action, and assertion phases
- Per constraints (Section 5.9): consider using parameterized tests for threshold filtering scenarios if the project uses parameterized test patterns — check `tests/api/sbom.rs` and `tests/api/advisory.rs` for existing patterns first
- Per constraints (Section 5.10): do not introduce parameterized test patterns if sibling tests do not use them

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests, demonstrates test setup patterns, fixture creation, and assertion style
- `tests/api/advisory.rs` — advisory endpoint integration tests, shows how advisory test data is created
- `tests/api/search.rs` — additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration test: SBOM with advisories at all four severity levels returns correct counts in JSON response
- [ ] Integration test: SBOM with no linked advisories returns `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: duplicate advisory links are deduplicated — same advisory counted only once
- [ ] Integration test: `?threshold=critical` returns only critical count (other fields zero or omitted per implementation)
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium counts
- [ ] Integration test: invalid threshold value returns 400 status
- [ ] Integration test: response Content-Type is `application/json`
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests are independent — no shared mutable state between test functions
- [ ] Test data is properly set up and torn down within each test

## Verification Commands
- `cargo test -p trustify-tests --test api` — all integration tests should pass, including the new advisory summary tests

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
