# Task 5 — Update and expand search integration tests

## Repository
trustify-backend

## Description
Update and expand the search integration tests in `tests/api/search.rs` to comprehensively
cover the new full-text search functionality, filter parameters, relevance ranking, response
format, and edge cases. Existing tests must continue to pass while new tests validate the
improved search behavior. This task also adds performance-oriented assertions to verify
that indexed searches complete within acceptable response times, addressing the non-functional
requirement "should be fast enough."

## Files to Modify
- `tests/api/search.rs` — Update existing search tests and add new tests covering:
  - Full-text search with relevance ranking (single keyword, multi-word queries)
  - Filter parameters (entity_type, date_from, date_to, severity)
  - Combined text search with filters
  - Response format validation (SearchResultItem fields)
  - Relevance ordering correctness
  - Edge cases (empty query, no results, invalid filter values)
  - Performance baseline (search latency with indexed data)

## Implementation Notes
- Inspect the existing tests in `tests/api/search.rs` to understand current test patterns:
  test setup, HTTP client configuration, request construction, and assertion style. Follow
  these patterns for all new tests.
- Reference sibling test files `tests/api/sbom.rs` and `tests/api/advisory.rs` for
  additional pattern guidance — they use the `assert_eq!(resp.status(), StatusCode::OK)`
  assertion pattern documented in the repository conventions.
- Integration tests hit a real PostgreSQL test database. Test data setup must include:
  - Multiple SBOMs with varied names, versions, and descriptions
  - Multiple advisories with different severity levels (critical, high, medium, low)
  - Multiple packages with different names and licenses
  - Entities with different creation dates to test date range filtering
- Test relevance ranking by inserting entities with known text content:
  - Entity A: search term appears in the title
  - Entity B: search term appears only in the description
  - Assert that Entity A ranks higher than Entity B in results
- For performance testing, use `std::time::Instant` to measure search query duration and
  assert completion within a reasonable bound (e.g., < 500ms). This is a baseline smoke
  test, not a rigorous benchmark — it ensures indexed queries are being used.
- Per constraints §5.11: add a doc comment to every test function explaining what it verifies.
- Per constraints §5.12: add given-when-then inline comments to non-trivial test functions
  (tests with distinct setup, action, and assertion phases).
- Per constraints §5.13: do not add given-when-then comments to trivial single-assertion tests.
- Per constraints §5.9-5.10: consider parameterized tests when multiple test cases exercise
  the same behavior with different inputs (e.g., testing each entity_type filter value),
  but only if sibling test files in `tests/api/` use parameterized test patterns. If they
  do not, use individual test functions instead.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests. Reference for test structure,
  test database setup, HTTP client usage, and assertion conventions.
- `tests/api/advisory.rs` — Advisory endpoint integration tests. Reference for
  severity-related test data setup and assertion patterns.
- `tests/api/search.rs` — Existing search tests. Extend rather than rewrite — preserve
  existing test coverage while adding new tests.

## Acceptance Criteria
- [ ] All existing search tests continue to pass without modification
- [ ] New tests cover full-text search with single-keyword and multi-word queries
- [ ] New tests cover each filter parameter individually (entity_type, date_from, date_to, severity)
- [ ] New tests cover combined text search plus filter queries
- [ ] New tests validate `SearchResultItem` response format (all fields present and correctly typed)
- [ ] New tests validate relevance ranking order (title match ranks above description-only match)
- [ ] New tests cover edge cases (empty query, no matching results, invalid filter values)
- [ ] Performance smoke test verifies search completes within 500ms for a dataset with 100+ entities
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Test: `GET /api/v2/search?q=openssl` returns results ranked by relevance score descending
- [ ] Test: `GET /api/v2/search?q=openssl&entity_type=sbom` returns only SBOM results
- [ ] Test: `GET /api/v2/search?q=cve&entity_type=advisory&severity=critical` returns only critical advisories
- [ ] Test: `GET /api/v2/search?q=test&date_from=2024-01-01&date_to=2024-06-30` returns only entities within the date range
- [ ] Test: `GET /api/v2/search?q=nonexistent-term-xyz` returns empty results with 200 OK
- [ ] Test: `GET /api/v2/search?entity_type=invalid` returns 400 Bad Request
- [ ] Test: search response includes `relevance_score`, `entity_type`, `snippet`, `entity_id`, `title`, and `created_at` fields
- [ ] Test: search performance completes within 500ms for 100+ entity dataset

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes with no regressions

## Dependencies
- Depends on: Task 3 — Add filter parameters to the search endpoint
- Depends on: Task 4 — Define SearchResultItem response model with enriched metadata
