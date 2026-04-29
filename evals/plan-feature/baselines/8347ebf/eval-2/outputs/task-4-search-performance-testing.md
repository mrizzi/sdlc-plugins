# Task 4 — Add Search Performance and Regression Integration Tests

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the improved search functionality, covering performance expectations, relevance ranking correctness, filter combinations, and backward compatibility. This task ensures the search improvements from Tasks 1-3 meet the non-functional requirement "should be fast enough" and the guard that existing functionality is not broken.

The tests serve as a regression safety net and validate that the full-text search indexes provide measurable performance improvement over the previous implementation.

## Files to Modify
- `tests/api/search.rs` — add new integration test cases for relevance ranking, filtering, performance, and edge cases

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` and sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`): tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- For performance testing, use Rust's `std::time::Instant` to measure search response times. Assert that searches against indexed columns complete within a reasonable threshold (e.g., under 500ms for typical queries). These are regression guards, not benchmarks — the goal is to catch gross performance degradation, not measure precise timings.
- Test edge cases: empty query string, very long query strings, special characters in queries, SQL injection attempts via search parameters.
- Test that search results across different entity types (SBOMs, advisories, packages) are correctly unified in the response with appropriate type discrimination.
- Per constraints doc section 2 (Commit Rules): commit must reference TC-9002 in footer.
- Per constraints doc section 5.9-5.13: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs; add doc comments to every test function; add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/search.rs` — existing search endpoint tests; extend with new test cases following the same setup and assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test database setup, request construction, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for how entity-specific assertions are structured

## Acceptance Criteria
- [ ] Test suite covers: relevance ranking order, all individual filter types, combined filters, edge cases (empty query, special characters), and backward compatibility
- [ ] Performance regression test verifies search completes within acceptable time threshold
- [ ] All new tests pass against a real PostgreSQL test database
- [ ] No existing tests are broken by the search changes

## Test Requirements
- [ ] Test: search with known data returns results in relevance-ranked order (highest relevance first)
- [ ] Test: each filter type (entity_type, severity, date_from, date_to, license) correctly narrows results
- [ ] Test: combined filters produce the intersection of individual filter results
- [ ] Test: empty search query returns appropriate error response (400 or empty set)
- [ ] Test: special characters in search query do not cause server errors
- [ ] Test: search performance for a typical query completes within 500ms threshold
- [ ] Test: pagination works correctly with filtered and ranked results (offset, limit parameters)

## Verification Commands
- `cargo test --test api search` — all search integration tests pass
- `cargo test --test api` — full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add Filtering Parameters to Search Endpoint
