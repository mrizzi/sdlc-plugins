# Task 4 — Add comprehensive integration tests for search improvements

**Feature:** TC-9002 — Improve search experience
**Label:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Ensure the search improvements (performance, relevance, and filtering) are thoroughly tested with end-to-end integration tests. While Tasks 1-3 each include test requirements for their specific changes, this task adds cross-cutting integration tests that verify the combined behavior: filters working together with relevance scoring, pagination working correctly with filters applied, and overall search behavior under realistic data scenarios with multiple entity types.

## Files to Modify
- `tests/api/search.rs` — Add comprehensive integration tests that cover cross-cutting search behavior: combined filters with relevance scoring, pagination with filters, multi-entity search scenarios, and edge cases (empty results, special characters in queries)

## Implementation Notes
- **Testing conventions:** Integration tests in `tests/api/` hit a real PostgreSQL test database. Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern used in existing tests. Review `tests/api/sbom.rs` and `tests/api/advisory.rs` for the established test setup and assertion patterns.
- **Test data setup:** Tests need to ingest sample SBOMs, advisories, and packages with known text content, severity levels, dates, and licenses to produce deterministic search results. Use the ingestion patterns from `modules/ingestor/src/service/mod.rs` and `modules/ingestor/src/graph/` for test data setup.
- **Cross-cutting scenarios to cover:**
  - Search with multiple filters applied simultaneously (e.g., `entity_type=advisory&severity=high&q=cve`)
  - Pagination with filters (verify `total` count reflects filtered results, not all results)
  - Relevance ordering with filters (verify score-based ordering is preserved when filters are active)
  - Empty result set (filters that match nothing return empty paginated response, not an error)
  - Special characters in search queries (parentheses, quotes, ampersands) handled gracefully
  - Large result sets paginate correctly
- **Response validation:** Verify responses use `PaginatedResults<T>` shape from `common/src/model/paginated.rs` with correct `total`, `items`, and pagination metadata.
- **Constraint §5.2:** Read existing test files before writing new tests to match established patterns.
- **Constraint §5.9:** Prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., testing each entity_type filter value). Check sibling test files first to see if parameterized tests are used in this project (Constraint §5.10).
- **Constraint §5.11:** Add a doc comment to every test function.
- **Constraint §5.12:** Add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — Integration test patterns for endpoint testing, test setup, and assertions
- `tests/api/advisory.rs` — Integration test patterns, particularly for severity-related assertions
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic for setting up test data
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion logic for setting up test data
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response shape to validate in assertions

## Acceptance Criteria
- [ ] Integration tests cover combined filter + search query scenarios
- [ ] Integration tests cover pagination with active filters
- [ ] Integration tests cover relevance ordering with active filters
- [ ] Integration tests cover edge cases (empty results, special characters)
- [ ] All tests use realistic test data with multiple entity types
- [ ] All new test functions have doc comments
- [ ] Non-trivial test functions include given-when-then inline comments

## Test Requirements
- [ ] At least one test verifies that `entity_type` + `severity` + search query filters compose correctly
- [ ] At least one test verifies that pagination `total` reflects the filtered count, not the unfiltered count
- [ ] At least one test verifies that relevance ordering is preserved when filters are active
- [ ] At least one test verifies graceful handling of special characters in search queries
- [ ] At least one test verifies empty result sets return a valid paginated response with `total: 0`

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance
- Depends on: Task 2 — Implement relevance scoring for search results
- Depends on: Task 3 — Add filter parameters to the search endpoint
