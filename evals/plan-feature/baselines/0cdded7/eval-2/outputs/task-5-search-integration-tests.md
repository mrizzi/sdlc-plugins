## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search experience, covering the new relevance ranking, filtering, caching, and combined scenarios. This ensures that all search improvements from TC-9002 work correctly end-to-end against a real PostgreSQL test database. While Tasks 2-4 each include tests for their specific changes, this task adds cross-cutting integration tests that exercise the features in combination and verify overall search behavior.

## Files to Modify
- `tests/api/search.rs` — add new integration test functions covering: combined filter + ranking scenarios, edge cases (empty results, special characters in queries, boundary date ranges), and performance baseline assertions

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` which uses `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database.
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for how test data is set up and torn down.
- Test data setup should create a mix of SBOMs, advisories, and packages with known attributes (specific titles, descriptions, severities, dates) so that test assertions can verify ranking order, filter correctness, and result counts deterministically.
- Include edge case tests:
  - Search with special characters (e.g., hyphens, dots, version numbers like "1.2.3")
  - Search with very long query strings
  - Filter with date_from equal to date_to (single day range)
  - Filter with entity_type that has no matching results
  - Combined filters that narrow results to zero
- Include a basic performance assertion: search with indexes should complete within a reasonable time threshold (e.g., under 500ms for a test dataset). This is a smoke test, not a load test.

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests; extend with new test functions following the same patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test data setup patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for test data setup and assertion patterns

## Acceptance Criteria
- [ ] Integration tests cover combined filter + ranking scenarios (e.g., filter by entity_type=advisory + severity=high, verify results are ranked by relevance)
- [ ] Edge case tests pass for special characters, empty results, and boundary date ranges
- [ ] All new tests pass against a PostgreSQL test database
- [ ] Existing tests in `tests/api/search.rs` remain unmodified and pass

## Test Requirements
- [ ] Test: search with entity_type filter + relevance ranking returns correctly filtered and ranked results
- [ ] Test: search with severity filter + date range filter returns only matching advisories within the date range
- [ ] Test: search with all filters combined (entity_type + severity + date range + search term) returns correct results
- [ ] Test: search with special characters in query string does not cause errors
- [ ] Test: search with filters that match no results returns empty paginated response (not an error)
- [ ] Test: search response times are within acceptable bounds for test dataset

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 2 — Search relevance ranking
- Depends on: Task 3 — Search filters
- Depends on: Task 4 — Search caching

[sdlc-workflow] Description digest: sha256:11f085bd9cfd32d28d0a8c7f1f2e50e6041978811709c1a688a5b90bd3ea1603
