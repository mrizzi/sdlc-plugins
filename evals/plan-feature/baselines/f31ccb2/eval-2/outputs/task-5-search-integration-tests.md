## Repository
trustify-backend

## Target Branch
main

## Description
Expand the search integration test suite to comprehensively cover the new full-text search, filtering, and performance features introduced in Tasks 1-4. The existing `tests/api/search.rs` needs new test cases for relevance ranking, filter combinations, edge cases, and performance characteristics.

## Files to Modify
- `tests/api/search.rs` — add integration tests for full-text search relevance ranking, filter parameters, filter combinations, edge cases, and performance/timeout behavior

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` and sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test data setup: create test SBOMs, advisories, and packages with known names and descriptions so relevance ranking can be verified deterministically
- **Relevance tests:** Insert entities with varying degrees of match to a search term and verify that results are returned in relevance order (highest score first)
- **Filter tests:** Test each filter parameter individually and in combination:
  - `entity_type=sbom` returns only SBOMs
  - `entity_type=advisory` returns only advisories
  - `date_from` and `date_to` correctly bound results
  - `severity` filter applies only to advisories
  - Combined filters narrow results correctly
- **Edge case tests:** Empty query string, special characters in search terms, queries with no matches, very long query strings
- **Error tests:** Invalid filter values return 400, query timeout returns appropriate error
- **Performance tests:** Verify search responses include Cache-Control headers
- Use the `PaginatedResults` shape from `common/src/model/paginated.rs` for response deserialization in assertions

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test setup, test database initialization, and assertion patterns
- `tests/api/advisory.rs` — reference for testing advisory-specific fields (severity) in integration tests
- `common/src/model/paginated.rs` — `PaginatedResults<T>` struct for deserializing search responses in test assertions

## Acceptance Criteria
- [ ] Integration tests cover relevance-ranked search results
- [ ] Integration tests cover each filter parameter individually
- [ ] Integration tests cover filter combinations
- [ ] Integration tests cover edge cases (empty query, special characters, no matches)
- [ ] Integration tests cover error responses (invalid filters, timeouts)
- [ ] All new tests pass against the test database

## Test Requirements
- [ ] All new integration tests pass with `cargo test --test api`
- [ ] Tests are deterministic and do not depend on external state beyond the test database
- [ ] Test names clearly describe the scenario being tested

## Verification Commands
- `cargo test --test api search` — all search tests should pass

## Dependencies
- Depends on: Task 3 — Add search filters (tests cover filtering functionality)
- Depends on: Task 4 — Search performance optimization (tests cover caching and timeout behavior)
