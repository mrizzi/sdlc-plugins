## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the search improvements introduced by the preceding tasks (full-text search with relevance ranking and filter support). These tests validate that the search endpoint behaves correctly with the new functionality and that existing search behavior is preserved as a regression baseline.

**Ambiguity note:** The feature description (TC-9002) states "Don't break existing functionality" as a non-functional requirement but does not define the existing test coverage baseline or specify acceptance thresholds for regression testing. This task assumes the existing tests in `tests/api/search.rs` represent the current baseline and adds new tests alongside them.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for full-text search relevance ranking, filter parameters, combined filter+search queries, edge cases, and regression tests for existing search behavior

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs`, which hits a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in the test suite.
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for how test data is set up and how endpoints are called in integration tests.
- Test data setup should create entities (SBOMs, Advisories, Packages) with known text content so that relevance ranking can be deterministically verified (e.g., an entity with the search term in its title should rank higher than one with the term only in its description).
- For filter tests, create entities with different types, severities, and dates to verify each filter dimension independently and in combination.
- Include negative tests: searches that should return no results, invalid filter values, empty queries.
- Include regression tests that verify the search endpoint still returns correct results for queries that worked before the search improvements.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests; follow the same test setup, assertion patterns, and test database usage
- `tests/api/advisory.rs` — Existing Advisory endpoint integration tests; reference for test data creation with severity fields
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper; tests should deserialize and validate paginated response structure

## Acceptance Criteria
- [ ] Integration tests for relevance ranking verify that title matches rank higher than description matches
- [ ] Integration tests for each filter type (entity_type, severity, date_range) verify correct filtering
- [ ] Integration tests for combined filters verify AND-combination behavior
- [ ] Integration tests for edge cases (empty query, special characters, no results) verify graceful handling
- [ ] Regression tests verify that previously working search queries continue to return correct results
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Relevance ranking test: insert entities with search term in title vs description, verify title match ranks first
- [ ] Entity type filter test: insert mixed entity types, filter by one type, verify only that type is returned
- [ ] Severity filter test: insert advisories with different severities, filter by severity, verify correct filtering
- [ ] Date range filter test: insert entities with different dates, filter by range, verify correct results
- [ ] Combined filter test: apply multiple filters simultaneously, verify all constraints are enforced
- [ ] Empty query test: send search request with no query term, verify appropriate response
- [ ] Special characters test: send search query with SQL-unsafe characters, verify no error or injection
- [ ] Pagination test: insert enough results to span multiple pages, verify pagination metadata is correct
- [ ] Regression test: replicate a search that works with the current implementation and verify it still works

## Dependencies
- Depends on: Task 3 — Add search filter support to query helpers and search endpoint

[sdlc-workflow] Description digest: sha256:242532b55f16ef780f789535cdbb6691ee320c2cb76722633f3095cd80f87bd5
