## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality introduced in TC-9002. These tests validate the full-text search with relevance ranking, filter parameters, performance with indexes, and backward compatibility with existing search behavior. This task ensures all search improvements work end-to-end against a real PostgreSQL test database.

## Files to Modify
- `tests/api/search.rs` — Extend the existing search integration tests with new test cases covering relevance ranking, filtering, sorting, combined parameters, error handling, and backward compatibility.

## Implementation Notes
The existing test file `tests/api/search.rs` already contains search endpoint integration tests. Extend it with new test functions following the established pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.

New test functions to add:

1. **Relevance ranking tests**:
   - `test_search_returns_results_ranked_by_relevance` — Insert entities with varying match quality, verify ordering
   - `test_search_relevance_score_present` — Verify response includes `relevance_score` field
   - `test_search_sort_override` — Verify `?sort=date` overrides relevance ordering

2. **Filter tests**:
   - `test_search_filter_by_entity_type` — `?entity_type=sbom` returns only SBOMs
   - `test_search_filter_by_severity` — `?severity=critical` returns only critical advisories
   - `test_search_filter_by_date_range` — `?date_from=...&date_to=...` bounds results
   - `test_search_combined_filters` — Multiple filters applied simultaneously
   - `test_search_invalid_filter_returns_400` — Bad filter values produce 400

3. **Backward compatibility tests**:
   - `test_search_without_filters_returns_results` — Existing query behavior unchanged
   - `test_search_empty_query_returns_default` — Empty `?q=` returns results

4. **Performance validation**:
   - `test_search_with_index_completes_quickly` — Basic timing assertion that indexed search completes within a reasonable threshold

Per Key Conventions (Testing): Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Acceptance Criteria
- [ ] All new test cases pass against a PostgreSQL test database
- [ ] Relevance ranking is validated with controlled test data
- [ ] Each filter type has at least one positive and one negative test case
- [ ] Backward compatibility is explicitly tested (existing queries still work)
- [ ] Invalid input produces appropriate error responses (400 status)
- [ ] Tests are deterministic and do not depend on external state

## Test Requirements
- [ ] Test relevance ranking orders results correctly given controlled input data
- [ ] Test entity_type filter returns only matching entity types
- [ ] Test severity filter correctly narrows advisory results
- [ ] Test date range filter bounds results by date
- [ ] Test combined filters apply AND semantics
- [ ] Test invalid filter values return 400 Bad Request
- [ ] Test backward compatibility — existing search queries still work
- [ ] Test pagination works with filtered and ranked results

## Verification Commands
- `cargo test --test search` — Run search integration tests
- `cargo test --test search -- --nocapture` — Run with output for debugging

## Dependencies
- Depends on: Task 3 — Search filters (tests validate the complete search feature including filters)

[sdlc-workflow] Description digest: sha256-md:65424122df210d5b8a854559e5421b52179829c596c2ffbcbfc9ca3fe515b038
