## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the enhanced search functionality, covering full-text search ranking, filter parameters, and performance characteristics. This validates that the search improvements from Tasks 1-3 work correctly end-to-end against a real PostgreSQL database.

## Files to Modify
- `tests/api/search.rs` — Add integration test cases for full-text search ranking, filtering by entity type, filtering by severity, date range filtering, filter combinations, and edge cases (empty queries, invalid filters)

## Implementation Notes
Follow the existing test patterns in `tests/api/search.rs` and the other integration test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`).

Test cases should cover:

1. **Relevance ranking**: Ingest test data with known terms, search for those terms, and verify the most relevant result appears first
2. **Entity type filter**: Search with `type=advisory` and verify only advisory results are returned
3. **Severity filter**: Search with `severity=critical` and verify only matching advisories are returned
4. **Date range filter**: Search with `from` and `to` parameters and verify results fall within the range
5. **Combined filters**: Search with multiple filters active and verify AND semantics
6. **Edge cases**: Empty query string, invalid filter values, no matching results
7. **Backward compatibility**: Search without any filters still returns results as before

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for any setup or teardown operations. Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Test Patterns: integration tests in `tests/api/` hit real PostgreSQL; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for test setup patterns, test data ingestion, and assertion style
- `tests/api/advisory.rs` — Reference for advisory-specific test data with severity values

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover full-text search ranking correctness
- [ ] Tests cover each filter parameter individually
- [ ] Tests cover filter combinations
- [ ] Tests cover error cases (invalid filters, empty queries)
- [ ] Tests verify backward compatibility (search without filters)

## Test Requirements
- [ ] Test that searching for a known term returns results ordered by relevance (highest-ranked first)
- [ ] Test that `type=sbom` filter returns only SBOM entities
- [ ] Test that `type=advisory` filter returns only advisory entities
- [ ] Test that `severity=critical` filter returns only critical-severity advisories
- [ ] Test that date range filter (`from`, `to`) restricts results to the specified window
- [ ] Test that combining `type` and `severity` filters returns only matching results
- [ ] Test that an invalid severity value returns an error response
- [ ] Test that a search with no filters returns results (backward compatibility)

## Dependencies
- Depends on: Task 3 — Add filter query parameters to search endpoint

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira
