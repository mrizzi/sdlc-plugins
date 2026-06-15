## Repository
trustify-backend

## Target Branch
main

## Description
Expand the search integration test suite to comprehensively cover the new full-text search, filtering, and performance characteristics introduced by Tasks 1-4. The existing test file `tests/api/search.rs` covers basic search behavior but needs to be extended to validate relevance ranking, filter composition, edge cases, and backward compatibility of the search API.

**Assumptions pending clarification:**
- Test data setup assumes the test PostgreSQL database supports the `english` text search configuration. No specific database configuration requirements were mentioned in the feature.
- Backward compatibility tests assume the current `GET /api/v2/search` response shape (using `PaginatedResults<T>`) is the contract to preserve. No API versioning strategy was specified.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for full-text search relevance, filtering by entity type and date range, filter composition, edge cases (empty queries, special characters, very long queries), and backward compatibility

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` which uses `assert_eq!(resp.status(), StatusCode::OK)` and hits a real PostgreSQL test database.
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for examples of setting up test data, making HTTP requests, and asserting on response bodies.
- Test relevance ranking by inserting documents with search terms in different positions (title only, description only, both) and verifying the result order.
- Test filter combinations systematically: each filter alone, all filters together, no filters (backward compatibility).
- Include edge case tests: empty search string, search string with only whitespace, search string with special characters (e.g., SQL injection attempts, PostgreSQL tsquery operators), very long search strings.
- All test functions must return `Result<T, AppError>` consistent with the project's test error handling pattern.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests to extend, following their setup and assertion patterns
- `tests/api/sbom.rs` — Test data setup patterns for SBOM entities that can be reused for search test fixtures
- `tests/api/advisory.rs` — Test data setup patterns for advisory entities

## Acceptance Criteria
- [ ] Test suite covers full-text search relevance ordering (documents with search term in title rank above those with term only in description)
- [ ] Test suite covers entity type filtering (`type=sbom`, `type=advisory`, `type=package`)
- [ ] Test suite covers date range filtering (`created_after`, `created_before`)
- [ ] Test suite covers combined filter scenarios (type + date range + search query)
- [ ] Test suite covers edge cases: empty query, whitespace-only query, special characters in query
- [ ] Test suite covers backward compatibility: requests without new filter parameters return results in the expected format
- [ ] All tests pass against the test PostgreSQL database

## Test Requirements
- [ ] Relevance ranking test: insert 3+ entities with varying term positions, assert correct ordering
- [ ] Entity type filter test: insert entities of different types, filter by one type, assert only matching type returned
- [ ] Date range filter test: insert entities with different creation dates, filter by range, assert only matching dates returned
- [ ] Combined filter test: apply type + date range + search query simultaneously, assert correct intersection
- [ ] Edge case test: empty search query returns appropriate response (empty results or 400)
- [ ] Edge case test: special characters in search query do not cause server errors
- [ ] Backward compatibility test: `GET /api/v2/search?q=term` without new filter params returns `PaginatedResults` with expected shape

## Dependencies
- Depends on: Task 2 — Implement full-text search (tests validate the full-text search behavior)
- Depends on: Task 3 — Add search filters (tests validate the filtering behavior)

[sdlc-workflow] Description digest: sha256-md:fa2d7af1e7fba7a63cc3aa86ad33f076fc6700f0f90b67fda12d440ff302d8fa
