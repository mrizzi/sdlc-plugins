## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests verify the end-to-end behavior of the advisory severity aggregation feature, including correct severity counts, advisory deduplication, 404 handling for missing SBOMs, the optional threshold query parameter, and performance characteristics for SBOMs with many advisories. Tests follow the existing integration test patterns in `tests/api/` using a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
Follow the existing integration test patterns established in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (Advisory endpoint tests). These files demonstrate:
- Test database setup and teardown
- HTTP request construction and response assertion using `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test data ingestion (creating SBOMs and advisories in the test database)
- JSON response body parsing and field assertion

Test cases to implement:

1. **Basic severity counts**: Ingest an SBOM with advisories at different severity levels, call the endpoint, verify each severity count matches
2. **Empty SBOM (no advisories)**: Ingest an SBOM with no linked advisories, verify all counts are zero
3. **Advisory deduplication**: Link the same advisory to an SBOM multiple times, verify the count reflects unique advisories only
4. **SBOM not found**: Call the endpoint with a non-existent SBOM ID, verify 404 response
5. **Threshold filter — critical**: Call with `?threshold=critical`, verify only critical count is non-zero (others filtered)
6. **Threshold filter — high**: Call with `?threshold=high`, verify critical and high counts are returned
7. **Invalid threshold value**: Call with an invalid threshold value, verify appropriate error response

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/advisory_summary.rs` matching the convention's integration test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow test setup patterns, HTTP client configuration, and assertion style
- `tests/api/advisory.rs` — Advisory endpoint integration tests; follow advisory test data creation patterns
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion logic; use to create test advisory data linked to SBOMs

## Acceptance Criteria
- [ ] All 7 test cases are implemented and pass against a PostgreSQL test database
- [ ] Tests verify correct severity count values, not just response status codes
- [ ] Tests verify advisory deduplication produces correct unique counts
- [ ] Tests follow existing integration test patterns from `tests/api/`

## Test Requirements
- [ ] Test for basic severity counts with multiple severity levels returns correct per-level counts
- [ ] Test for empty SBOM returns all-zero counts with total of 0
- [ ] Test for advisory deduplication returns count of 1 for a duplicated advisory
- [ ] Test for non-existent SBOM returns 404 status code
- [ ] Test for threshold=critical returns only critical severity count
- [ ] Test for threshold=high returns critical and high severity counts
- [ ] Test for invalid threshold value returns an appropriate error response

## Verification Commands
- `cargo test --test api advisory_summary` — All advisory-summary integration tests pass
- `cargo test --test api` — Full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
