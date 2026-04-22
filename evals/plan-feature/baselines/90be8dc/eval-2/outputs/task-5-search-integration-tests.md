## Repository
trustify-backend

## Description
Write comprehensive integration tests for the improved search functionality, covering relevance ranking, filtering, the new result model, and performance characteristics. These tests validate all acceptance criteria from Tasks 2-4 end-to-end against a real PostgreSQL test database, following the project's existing integration test patterns.

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for relevance ranking, filter parameters, search result model with scores, backward compatibility, edge cases, and performance (query plan verification)

## Implementation Notes
Follow the existing test patterns in `tests/api/search.rs` and other test files like `tests/api/sbom.rs` and `tests/api/advisory.rs`:

1. Use the existing test infrastructure in `tests/` that runs against a real PostgreSQL test database.
2. Follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern from the project conventions.
3. Test categories to cover:
   - **Relevance ranking**: Insert test data with varying relevance, search, and verify ordering by score.
   - **Filters**: Test each filter individually (`type`, `severity`, `created_after`, `created_before`) and in combination.
   - **Result model**: Verify JSON response includes `score` and `type` fields with correct values.
   - **Backward compatibility**: Verify that requests without new parameters still work as before.
   - **Edge cases**: Empty query, special characters in query, no results found, invalid filter values (expect 400).
   - **Performance**: Use `EXPLAIN ANALYZE` or equivalent to verify index scans are used (optional, can be a separate test).
4. Seed test data covering all three entity types (SBOMs, advisories, packages) with known text content to enable deterministic relevance assertions.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests; extend with new test cases following the same patterns
- `tests/api/sbom.rs` — Reference for integration test patterns, test data seeding, and assertion style
- `tests/api/advisory.rs` — Reference for integration test patterns

## Acceptance Criteria
- [ ] Tests cover relevance-ranked search results (ordering by score)
- [ ] Tests cover each filter parameter individually
- [ ] Tests cover combined filters (AND logic)
- [ ] Tests verify backward compatibility (no filters = existing behavior)
- [ ] Tests cover edge cases (empty query, invalid filters, no results)
- [ ] Tests verify the `SearchResult` JSON shape includes `score` and `type`
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: search returns results ordered by relevance score descending
- [ ] Test: `type=advisory` filter returns only advisory results
- [ ] Test: `severity=critical` filter returns only critical-severity advisories
- [ ] Test: `created_after` and `created_before` filter results by date
- [ ] Test: combining `type` and `severity` filters works correctly
- [ ] Test: search with no filters returns results from all entity types
- [ ] Test: empty search query returns 400 or empty results (per chosen behavior)
- [ ] Test: invalid filter value returns 400 Bad Request
- [ ] Test: response JSON contains `score` (float) and `type` (string) fields

## Verification Commands
- `cargo test -p tests --test search` — All search integration tests pass
- `cargo test -p tests` — Full integration test suite passes (no regressions)

## Dependencies
- Depends on: Task 2 — Implement relevance-ranked search in SearchService
- Depends on: Task 3 — Add filter parameter support to search endpoint
- Depends on: Task 4 — Add search result model with relevance score
