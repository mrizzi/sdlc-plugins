## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for all search improvements: relevance ranking, filtering, caching, and performance. This ensures the "don't break existing functionality" non-functional requirement is met and validates the new search capabilities end-to-end.

## Files to Modify
- `tests/api/search.rs` — Extend existing search integration tests with new test cases covering relevance ranking, filters, caching behavior, and backward compatibility

## Implementation Notes
In `tests/api/search.rs`:
- Add test fixtures that seed the test database with known SBOMs, advisories, and packages with varying attributes (different severities, dates, names with distinct text patterns)
- Follow the existing test pattern using `assert_eq!(resp.status(), StatusCode::OK)` as established in `tests/api/sbom.rs` and `tests/api/advisory.rs`

Test categories to add:

1. **Backward compatibility tests**: Verify that existing search queries (no filters, no explicit ranking) return results without errors. This validates the "don't break existing functionality" requirement.

2. **Relevance ranking tests**: 
   - Search for a term that appears as an exact match in one entity and partial match in another — verify exact match ranks first
   - Search for a term with no matches — verify empty `PaginatedResults` response (from `common/src/model/paginated.rs`)

3. **Filter tests**:
   - Filter by entity_type=sbom — verify only SBOM results returned
   - Filter by entity_type=advisory — verify only advisory results returned
   - Filter by severity — verify only matching advisories returned
   - Filter by date range — verify only results within range returned
   - Combine entity_type + severity filters — verify AND behavior
   - Invalid filter value — verify 400 error response

4. **Caching tests**:
   - Execute same search twice — verify second response is faster or served from cache
   - Execute search, wait for TTL expiry, search again — verify fresh results

Assumption (pending clarification): Performance assertions (e.g., "second query is faster") may be flaky in CI. These tests should use cache hit/miss indicators rather than timing-based assertions if possible.

Per CONVENTIONS.md §Testing: Integration tests hit a real PostgreSQL test database using the existing test infrastructure.
Applies: task modifies `tests/api/search.rs` matching the integration test convention.

## Acceptance Criteria
- [ ] All existing search tests continue to pass (backward compatibility)
- [ ] New tests cover relevance ranking ordering
- [ ] New tests cover each filter type independently
- [ ] New tests cover combined filters
- [ ] New tests cover invalid filter input error handling
- [ ] New tests cover search caching behavior
- [ ] Tests use real PostgreSQL test database per project conventions

## Test Requirements
- [ ] At least 2 backward compatibility tests (existing search behavior preserved)
- [ ] At least 3 relevance ranking tests (exact match priority, partial match, no results)
- [ ] At least 5 filter tests (each filter type, combined filters, invalid input)
- [ ] At least 2 caching tests (cache hit, cache expiry)

## Dependencies
- Depends on: Task 2 — search-relevance-ranking
- Depends on: Task 3 — search-filters
- Depends on: Task 4 — search-caching

[sdlc-workflow] Description digest: sha256-md:d35c39091f4887fbaa5f0018f59e6396dc1c388501fef127acd406da124992df
