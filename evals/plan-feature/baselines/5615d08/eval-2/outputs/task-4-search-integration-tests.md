## Repository
trustify-backend

## Description
Add comprehensive integration tests for the search improvements implemented in Tasks 1-3: performance optimizations, relevance scoring, and filter parameters. The existing test file `tests/api/search.rs` covers the baseline search behavior. This task extends it with tests that verify the new functionality and guard against regressions. These tests also serve as executable documentation of the assumed behaviors where the feature requirements were ambiguous (see Ambiguities A1-A5 in impact-map.md).

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for relevance ordering, filter parameters, combined filters, error handling, and performance characteristics

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` and the sibling test files `tests/api/sbom.rs` and `tests/api/advisory.rs`. These use the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the repository conventions.
- Tests hit a real PostgreSQL test database (per repository conventions). Ensure test data setup includes:
  - Multiple SBOMs, advisories, and packages with distinct names and descriptions
  - Advisories with varying severity levels (critical, high, medium, low)
  - Entities with different creation dates to support date range filter tests
- For relevance tests: create two entities where one matches the search term in its name and the other matches only in its description. Assert the name-match result appears first in the response.
- For filter tests: submit requests with various query parameter combinations and assert the response contains only matching entities.
- For error handling tests: submit requests with invalid filter values (e.g., `severity=invalid`) and assert a 400 status code response.
- For backwards compatibility: re-run queries without any filter parameters and assert results match the pre-existing behavior.
- The response structure should be checked against the `PaginatedResults` shape from `common/src/model/paginated.rs`, extended with any score metadata added in Task 2.
- Use `serde_json::Value` or typed response structs to deserialize and inspect response bodies.

## Reuse Candidates
- `tests/api/search.rs` — Existing test structure and setup code; extend rather than rewrite
- `tests/api/sbom.rs` — Test patterns for SBOM-related assertions; reference for response structure validation
- `tests/api/advisory.rs` — Test patterns for advisory-related assertions; reference for severity field validation

## Acceptance Criteria
- [ ] All new tests pass against the PostgreSQL test database
- [ ] All pre-existing tests in `tests/api/search.rs` continue to pass
- [ ] Test coverage includes relevance ordering, each individual filter, combined filters, invalid inputs, and backwards compatibility
- [ ] Tests document the assumed behaviors from the ambiguous requirements (comments reference the ambiguity IDs from the impact map)

## Test Requirements
- [ ] Test: search results are ordered by relevance score (name-match before description-match)
- [ ] Test: search response includes score metadata
- [ ] Test: `entity_type` filter returns only the specified entity type
- [ ] Test: `severity` filter returns only advisories with matching severity
- [ ] Test: `date_from` and `date_to` filters restrict results to the specified date range
- [ ] Test: combining `entity_type` and `severity` filters narrows results with AND logic
- [ ] Test: omitting all filters returns unfiltered results (backwards compatibility)
- [ ] Test: invalid severity value returns 400 Bad Request
- [ ] Test: invalid date format returns 400 Bad Request

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 2 — Improve search result relevance with weighted scoring
- Depends on: Task 3 — Add filter parameters to search endpoint
