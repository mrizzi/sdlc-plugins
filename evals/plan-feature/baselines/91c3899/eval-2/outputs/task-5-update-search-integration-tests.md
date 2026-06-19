## Repository
trustify-backend

## Target Branch
main

## Description
Update and expand the search integration test suite to cover the new full-text search ranking, filtering, and combined search+filter scenarios. This ensures the search improvements are verified end-to-end against a real PostgreSQL test database and guards against regressions.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for full-text search relevance ranking, filter parameters (entity_type, severity, date_range), combined search+filter queries, edge cases (empty queries, no results, invalid filters), and performance baseline assertions

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` and sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) which use real PostgreSQL test databases
- Per Key Conventions §Testing: use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status assertions. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Test data setup should insert entities with known text content to verify ranking (e.g., insert an SBOM with "vulnerability" in the name and another with "vulnerability" only in the description; verify the name-match ranks first)
- Test filter combinations: entity_type alone, severity alone, date range alone, entity_type + search query, all filters combined
- Verify backward compatibility: existing search behavior without new parameters should produce the same results
- Consider adding a test for search performance by asserting query completion within a reasonable time (e.g., under 1 second for small test datasets), though exact thresholds are environment-dependent

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests; extend with new test cases rather than replacing
- `tests/api/sbom.rs` — Reference for test setup patterns (database seeding, HTTP client usage, assertion patterns)
- `tests/api/advisory.rs` — Reference for advisory-specific test data setup

## Acceptance Criteria
- [ ] Tests verify that full-text search returns results ranked by relevance (name matches before description matches)
- [ ] Tests verify each filter parameter works independently
- [ ] Tests verify filters compose correctly with search queries
- [ ] Tests verify backward compatibility (no filters = all results)
- [ ] Tests verify error responses for invalid filter values
- [ ] All new tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Integration test: relevance ranking — name match ranks higher than description match
- [ ] Integration test: entity_type filter — only matching entity type returned
- [ ] Integration test: severity filter — only matching severity advisories returned
- [ ] Integration test: date range filter — only entities within range returned
- [ ] Integration test: combined search query + entity_type filter
- [ ] Integration test: combined search query + severity + date range filters
- [ ] Integration test: no results found returns empty paginated response (not error)
- [ ] Integration test: invalid entity_type returns 400
- [ ] Integration test: no parameters returns all results (backward compatibility)

## Dependencies
- Depends on: Task 1 — Add full-text search migration (database schema must include tsvector columns)
- Depends on: Task 3 — Upgrade search service to full-text (search service must use new ranking)
- Depends on: Task 4 — Add search filters endpoint (filter parameters must be available)
