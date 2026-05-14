# Task 5: Add Comprehensive Integration Tests for Search Improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests covering all search improvements from TC-9002: performance (full-text search), relevance scoring, and filtering. This task consolidates the end-to-end testing to verify that all pieces work together and that existing functionality has not regressed.

**Assumption (pending clarification)**: The existing test infrastructure in `tests/api/search.rs` uses a real PostgreSQL test database (as documented in the repository conventions). This task assumes that test database setup runs migrations automatically, so the new indexes from Task 1 will be available in the test environment.

**Assumption (pending clarification)**: No performance benchmarks or SLA targets were provided. Integration tests in this task verify functional correctness and basic response time assertions (e.g., search completes within 2 seconds). Formal performance benchmarks are out of scope without defined targets.

## Files to Modify
- `tests/api/search.rs` — Add new integration test functions covering full-text search accuracy, relevance ordering, filter combinations, and backward compatibility; update existing tests if the response shape has changed (new `SearchResult` wrapper from Task 3)

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`:
  - Use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
  - Parse response JSON to verify result structure and content.
  - Tests run against a real PostgreSQL test database.
- Test data setup: create test SBOMs, advisories (with varying severity levels), and packages (with different licenses) before running search queries. Follow the data setup patterns in existing test files.
- Organize tests into clearly named functions:
  - `test_search_fulltext_matches_expected_results` — verifies that full-text search finds entities by name and description keywords.
  - `test_search_relevance_exact_match_ranks_first` — verifies that an exact title match ranks above a partial match.
  - `test_search_relevance_severity_boost` — verifies that high-severity advisories rank above low-severity for the same search term.
  - `test_search_filter_entity_type` — verifies that `entity_type=sbom` returns only SBOMs.
  - `test_search_filter_severity` — verifies that `severity=critical` returns only critical advisories.
  - `test_search_filter_license` — verifies that `license=MIT` returns only MIT-licensed packages.
  - `test_search_filter_combined` — verifies that multiple filters work together.
  - `test_search_filter_invalid_returns_400` — verifies that invalid filter values return 400 Bad Request.
  - `test_search_backward_compatible_no_filters` — verifies that an unfiltered search still works and returns results from all entity types.
  - `test_search_response_includes_score_and_type` — verifies the `SearchResult` response includes `relevance_score` and `entity_type` fields.
- Each test should verify the response includes the `PaginatedResults` structure from `common/src/model/paginated.rs` (total count, items array, pagination metadata).
- Use the `StatusCode` enum from `axum::http` for status assertions, matching the existing test pattern.

## Acceptance Criteria
- [ ] All new integration tests pass against the test database
- [ ] All existing tests in `tests/api/search.rs` continue to pass (updated if response shape changed)
- [ ] Tests cover: full-text search accuracy, relevance ordering, severity boost, entity_type filtering, severity filtering, license filtering, combined filters, invalid filter handling, backward compatibility
- [ ] Each test function has a descriptive name that communicates what it validates
- [ ] Tests follow the existing integration test conventions in `tests/api/`

## Test Requirements
- [ ] `test_search_fulltext_matches_expected_results` — insert entities with known names, search by name keyword, verify matches are returned
- [ ] `test_search_relevance_exact_match_ranks_first` — insert entities with similar names, search for an exact name, verify it is the first result
- [ ] `test_search_relevance_severity_boost` — insert two advisories with same search term but different severities, verify critical ranks above low
- [ ] `test_search_filter_entity_type` — search with `entity_type=sbom`, verify all results have `entity_type: "sbom"`
- [ ] `test_search_filter_severity` — search with `severity=critical`, verify only critical-severity advisories are returned
- [ ] `test_search_filter_license` — search with `license=MIT`, verify only MIT-licensed packages are returned
- [ ] `test_search_filter_combined` — search with `entity_type=advisory&severity=high`, verify only high-severity advisories are returned
- [ ] `test_search_filter_invalid_returns_400` — search with `entity_type=invalid`, verify 400 response
- [ ] `test_search_backward_compatible_no_filters` — search with no filter parameters, verify results include all entity types
- [ ] `test_search_response_includes_score_and_type` — verify each result item has `relevance_score` (f64) and `entity_type` (string) fields

## Dependencies
- Depends on: Task 4 — Add Filter Parameters to Search Endpoint (all features must be implemented before comprehensive testing)
