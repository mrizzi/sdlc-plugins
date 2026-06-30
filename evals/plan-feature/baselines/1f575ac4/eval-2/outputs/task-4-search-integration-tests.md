# Task 4 — Add comprehensive integration tests for improved search

**Summary:** Add integration tests covering search performance, relevance ordering, and filter combinations

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests to `tests/api/search.rs` that validate the full search improvement feature end-to-end: full-text search relevance ordering, filter parameter combinations, edge cases (empty queries, no results, special characters), and backward compatibility of the existing search contract. This ensures the search improvements from Tasks 1-3 are fully verified and protects against regressions.

## Files to Modify
- `tests/api/search.rs` — Add new test functions covering relevance ordering, filter parameters, edge cases, and combined filter scenarios

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` — examine the current test structure for the `assert_eq!(resp.status(), StatusCode::OK)` pattern and how the test database is set up.
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for additional examples of how integration tests are structured (setup, request, assertion phases).
- Tests should use a real PostgreSQL test database per the project's testing convention.
- Test data setup should insert entities with known text content so relevance ordering can be deterministically verified — e.g., insert an SBOM with name "critical security sbom" and another with name "unrelated document", then search for "critical security" and verify the first result is the expected one.
- For filter tests, insert a mix of entity types and verify that filtering narrows results correctly.
- Edge case tests should cover: empty search term, search term with no matches, special characters in search term, very long search terms.
- Ensure all new test functions follow the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests; follow the established test setup and assertion patterns.
- `tests/api/sbom.rs` — SBOM endpoint tests; reference for integration test structure and test database setup.
- `tests/api/advisory.rs` — Advisory endpoint tests; reference for how advisory test data is constructed.

## Acceptance Criteria
- [ ] Tests verify that search results are ordered by relevance (most relevant first)
- [ ] Tests verify entity type filtering (`entity_type=sbom`, `advisory`, `package`)
- [ ] Tests verify date range filtering (`created_after`, `created_before`)
- [ ] Tests verify severity filtering for advisories
- [ ] Tests verify combined filter scenarios
- [ ] Tests verify backward compatibility (search without filters returns all types)
- [ ] Tests verify edge cases (empty query, no results, special characters)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Relevance ordering test: insert documents with varying keyword density, verify result ordering
- [ ] Entity type filter tests: one test per entity type verifying correct filtering
- [ ] Date range filter test: insert documents with known timestamps, verify range filtering
- [ ] Severity filter test: insert advisories with different severities, verify filtering
- [ ] Combined filter test: apply multiple filters simultaneously, verify intersection
- [ ] Empty query test: verify appropriate response for empty or missing search term
- [ ] No results test: search for a term that matches no documents, verify empty result set
- [ ] Special characters test: search for terms with quotes, ampersands, etc.

## Verification Commands
- `cargo test --test search` — All search integration tests pass
- `cargo test --test search -- --nocapture` — Run with output for debugging

## Dependencies
- Depends on: Task 3 — Add filtering parameters to search endpoint
