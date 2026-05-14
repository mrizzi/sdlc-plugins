## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, all filter parameter combinations, performance regression detection, and backward compatibility. These tests validate that the search improvements from TC-9002 work end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/search.rs` -- Add integration tests covering full-text search relevance ranking, filter parameters (entity_type, severity, license, date_from, date_to), combined filters, backward compatibility, and edge cases (empty queries, invalid filters, no results)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Set up test data by inserting SBOMs, advisories, and packages with known searchable text, severity values, license values, and creation dates so that filter and ranking assertions can be deterministic.
- For relevance ranking tests: insert multiple entities with varying degrees of keyword overlap in their searchable fields, then verify that a search query returns them in the expected relevance order.
- For filter tests: insert entities spanning multiple types, severities, licenses, and dates, then verify that each filter correctly narrows the result set.
- For backward compatibility tests: issue search requests without any of the new filter parameters and verify the response shape matches `PaginatedResults<T>` with the expected entities.
- For edge cases:
  - Empty search query with no filters should return all entities.
  - Invalid filter values (e.g., severity="nonexistent") should return an empty result set or a 400 error, depending on the implementation in Task 3.
  - Search query with no matching results should return an empty `PaginatedResults` with `total: 0`.
- Per constraints doc section 5.11: add a doc comment to every test function.
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions (those with distinct setup, action, and assertion phases).

## Reuse Candidates
- `tests/api/search.rs` -- existing search integration tests to follow as a pattern and extend
- `tests/api/sbom.rs` -- SBOM endpoint integration tests demonstrating test setup and assertion patterns
- `tests/api/advisory.rs` -- advisory endpoint integration tests demonstrating test setup and assertion patterns

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Relevance ranking is verified by asserting result order for queries with known relevance distribution
- [ ] Each filter parameter (entity_type, severity, license, date_from, date_to) has at least one dedicated test
- [ ] Combined filter tests verify correct intersection behavior
- [ ] Backward compatibility test verifies existing API behavior is preserved
- [ ] Edge cases (empty query, no results, invalid filters) are covered
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Integration test: full-text search returns results in relevance-ranked order
- [ ] Integration test: entity_type filter isolates results to the specified type(s)
- [ ] Integration test: severity filter restricts advisory results correctly
- [ ] Integration test: license filter restricts package results correctly
- [ ] Integration test: date range filter restricts results to the specified window
- [ ] Integration test: combining multiple filters produces the correct intersection
- [ ] Integration test: omitting all new parameters returns the same results as the original search endpoint
- [ ] Integration test: empty query returns all entities
- [ ] Integration test: query with no matches returns empty PaginatedResults

## Verification Commands
- `cargo test -p tests --test search` -- all search integration tests pass

## Dependencies
- Depends on: Task 1 -- Add full-text search migration (database schema must be in place)
- Depends on: Task 3 -- Implement search filtering and relevance ranking (endpoint changes must be complete)
