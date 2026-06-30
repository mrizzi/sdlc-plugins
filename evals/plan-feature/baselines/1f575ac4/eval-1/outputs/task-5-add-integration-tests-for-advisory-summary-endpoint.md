# Task 5 — Add integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the full range of scenarios including successful responses with various severity distributions, 404 for non-existent SBOMs, deduplication of advisories, threshold query parameter filtering, and response shape validation. Tests follow the existing integration test patterns in `tests/api/` and run against a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — if needed, ensure the new test file is included in the test build (may be auto-discovered)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test scenarios to implement:
  1. **Happy path**: Create an SBOM, link advisories at various severity levels (e.g., 2 Critical, 3 High, 1 Medium, 0 Low), call the endpoint, verify exact counts in response.
  2. **Empty advisories**: Create an SBOM with no linked advisories, verify response returns all zeros: `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`.
  3. **Non-existent SBOM**: Call endpoint with a non-existent UUID, verify 404 response.
  4. **Deduplication**: Link the same advisory to an SBOM multiple times (if possible via the join table), verify the advisory is counted only once.
  5. **Threshold filtering — critical**: Call with `?threshold=critical`, verify only `critical` count is non-zero and `high`, `medium`, `low` are 0.
  6. **Threshold filtering — high**: Call with `?threshold=high`, verify `critical` and `high` counts are present, `medium` and `low` are 0.
  7. **Response shape**: Verify the JSON response has exactly the fields `critical`, `high`, `medium`, `low`, `total`.
- Set up test data by using the existing ingestion or service APIs to create SBOMs and advisories in the test database, following the setup patterns used in `tests/api/sbom.rs` and `tests/api/advisory.rs`.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test setup patterns, HTTP client usage, assertion patterns, and test database configuration
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for how advisory entities are created in tests and how severity is set
- `tests/api/search.rs` — additional integration test reference for endpoint testing patterns

## Acceptance Criteria
- [ ] Integration tests exist in `tests/api/advisory_summary.rs`
- [ ] Tests cover: happy path, empty advisories, non-existent SBOM (404), deduplication, threshold filtering (critical and high), response shape validation
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests follow the existing patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Test Requirements
- [ ] All test scenarios listed in Implementation Notes are covered
- [ ] Tests use the standard `assert_eq!(resp.status(), StatusCode::...)` assertion pattern
- [ ] Tests create their own test data and do not depend on pre-existing database state
- [ ] Tests verify both the HTTP status code and the JSON response body content

## Verification Commands
- `cargo test --test api advisory_summary` — expected outcome: all advisory summary integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
