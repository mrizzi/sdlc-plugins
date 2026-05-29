## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the core scenarios: successful aggregation with correct counts, 404 for non-existent SBOM, advisory deduplication, threshold query parameter filtering, and cache behavior. These tests follow the existing integration test patterns in `tests/api/` and hit a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests set up test data, make HTTP requests to the running test server, and assert on response status codes and JSON bodies.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, as documented in the repository conventions.
- Test scenarios to implement:
  1. **Happy path**: create an SBOM, link advisories at various severity levels, call the endpoint, verify the response JSON matches expected counts.
  2. **SBOM not found**: call the endpoint with a non-existent UUID, verify 404 response.
  3. **Deduplication**: create an SBOM with duplicate advisory links in the join table, verify each advisory is counted only once.
  4. **Threshold filtering**: call with `?threshold=critical`, verify only critical count is non-zero; call with `?threshold=high`, verify critical and high counts; call with invalid threshold, verify 400.
  5. **Empty SBOM**: create an SBOM with no linked advisories, verify all counts are 0 and total is 0.
- Set up test data by inserting SBOM, advisory, and sbom_advisory records directly into the test database, following the fixtures and setup patterns in sibling test files.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests demonstrating test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests demonstrating how to create advisory test data
- `common/src/model/paginated.rs::PaginatedResults` — not directly used but demonstrates the response type pattern used in sibling tests

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/advisory_summary.rs`
- [ ] Tests cover: happy path, 404, deduplication, threshold filtering (valid and invalid), empty SBOM
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow the established patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Test Requirements
- [ ] Test: SBOM with advisories at all four severity levels returns correct counts and correct total
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: duplicate advisory links do not inflate counts
- [ ] Test: `?threshold=critical` returns only critical count, total equals critical
- [ ] Test: `?threshold=high` returns critical and high, total equals their sum
- [ ] Test: invalid threshold value returns 400
- [ ] Test: SBOM with zero advisories returns all counts as 0

## Verification Commands
- `cargo test -p tests --test advisory_summary` — expected: all tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint
- Depends on: Task 4 — Add threshold query parameter

[sdlc-workflow] Description digest: sha256:9c0e9a67756435d924522fc6aabf5f237e0203d033d1d520a6239c45f585545b
