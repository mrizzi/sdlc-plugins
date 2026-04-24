# Task 5 — Update search integration tests for filters, relevance, and performance

## Repository
trustify-backend

## Description
Update and expand the search integration tests in `tests/api/search.rs` to cover the new
full-text search functionality, filter parameters, relevance ranking, and response format.
The existing tests must continue to pass while new tests validate the improved search
behavior. This task also adds performance-oriented assertions to ensure that searches
using the new indexes complete within acceptable timeframes.

## Files to Modify
- `tests/api/search.rs` — Update existing search tests and add new tests for:
  - Full-text search with relevance ranking
  - Filter parameters (entity type, date range, severity)
  - Combined text search + filters
  - Response format validation (SearchResultItem fields)
  - Edge cases (empty query, no results, invalid filters)

## Implementation Notes
- Inspect the existing tests in `tests/api/search.rs` to understand the current test
  patterns: setup, HTTP request construction, assertion style. Follow the same patterns
  for new tests.
- Follow the test patterns from sibling test files `tests/api/sbom.rs` and
  `tests/api/advisory.rs` — they use the `assert_eq!(resp.status(), StatusCode::OK)`
  assertion pattern.
- Integration tests hit a real PostgreSQL test database. Ensure test data includes:
  - Multiple SBOMs, advisories, and packages with varied text content
  - Advisories with different severity levels
  - Entities with different creation dates to test date range filters
- Test relevance ranking by inserting entities with known text content and asserting
  that entities with the search term in the title rank higher than entities with the
  term only in the description.
- For performance testing, use `std::time::Instant` to measure search query duration
  and assert it completes within a reasonable bound (e.g., < 500ms for a dataset with
  at least 100 entities). Note: this is a baseline smoke test, not a rigorous benchmark.
- Per constraints §5.11: add a doc comment to every test function.
- Per constraints §5.12: add given-when-then inline comments to non-trivial test functions.
- Per constraints §5.13: do not add given-when-then comments to trivial single-assertion tests.
- Per constraints §5.9: use parameterized tests when multiple test cases exercise the
  same behavior with different inputs (e.g., testing multiple entity type filters), but
  only if sibling test files use this pattern (per §5.10).

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests. Reference for test structure,
  setup patterns, and assertion conventions.
- `tests/api/advisory.rs` — Advisory endpoint integration tests. Reference for test
  structure and severity-related test data.
- `tests/api/search.rs` — Existing search tests. Extend rather than rewrite.

## Acceptance Criteria
- [ ] Existing search tests continue to pass
- [ ] New tests cover full-text search with single and multi-word queries
- [ ] New tests cover each filter parameter individually (entity_type, date_from, date_to, severity)
- [ ] New tests cover combined text search + filter queries
- [ ] New tests validate response format (SearchResultItem fields present and correct)
- [ ] New tests validate relevance ranking order
- [ ] New tests cover edge cases (empty query, no results, invalid filter values)
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Test: `GET /api/v2/search?q=openssl` returns results ranked by relevance
- [ ] Test: `GET /api/v2/search?q=openssl&entity_type=sbom` returns only SBOMs
- [ ] Test: `GET /api/v2/search?q=cve&severity=critical` returns only critical advisories
- [ ] Test: `GET /api/v2/search?q=test&date_from=2024-01-01&date_to=2024-06-30` returns date-filtered results
- [ ] Test: `GET /api/v2/search?q=nonexistent` returns empty results with 200 OK
- [ ] Test: `GET /api/v2/search?entity_type=invalid` returns 400 Bad Request
- [ ] Test: search response time < 500ms for dataset with 100+ entities

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add filter parameters to the search endpoint
- Depends on: Task 4 — Extend search endpoint response with relevance score and metadata
