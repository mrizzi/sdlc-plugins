# Task 6: Add Integration Tests for Search Improvements

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the search improvements implemented in Tasks 1-5. Tests should cover full-text search relevance ranking, filter parameters, edge cases, and regression scenarios to ensure existing functionality is not broken. This addresses the non-functional requirement "Don't break existing functionality."

**Ambiguity note:** The feature provides no definition of expected search behavior or test scenarios. The test cases below are based on assumed behavior from Tasks 1-5 (pending clarification on expected search semantics and relevance expectations).

## Files to Modify
- `tests/api/search.rs` — Add new integration test cases for FTS relevance ranking, filter parameters, combined search+filter queries, edge cases (empty queries, special characters), and pagination of filtered results

## Implementation Notes
- Follow the existing test pattern in `tests/api/search.rs` and other test files like `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test data setup: insert test records (SBOMs, advisories, packages) with known text content so search results are deterministic. Ensure the migration from Task 1 has run so `search_vector` columns and triggers are active.
- Key test scenarios:
  1. **Relevance ranking**: Insert records with varying relevance to a search term. Verify that the most relevant result appears first.
  2. **Entity type filter**: Search with `?type=advisory` and verify only advisory results are returned.
  3. **Severity filter**: Search with `?severity=high` and verify only high-severity advisories are returned.
  4. **Date range filter**: Search with `?created_after=<date>` and verify older results are excluded.
  5. **Combined filters**: Search with `?q=term&type=advisory&severity=critical` and verify all filters are applied.
  6. **Empty query**: Verify empty search returns empty results (not all records).
  7. **Special characters**: Verify search handles special characters without errors (SQL injection prevention).
  8. **No matches**: Verify searching for a non-existent term returns an empty paginated result.
  9. **Invalid filter values**: Verify `?severity=invalid` returns 400 Bad Request.
- Use `PaginatedResults<T>` deserialization to verify response structure.
- Per CONVENTIONS.md: integration tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests for test setup patterns and assertion style
- `tests/api/sbom.rs` — SBOM endpoint tests for reference on test data insertion and response deserialization
- `tests/api/advisory.rs` — Advisory endpoint tests for reference on severity-related test scenarios

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Existing tests in `tests/api/search.rs` continue to pass (no regressions)
- [ ] Tests cover relevance ranking, all filter types, combined filters, and edge cases
- [ ] Test data setup is self-contained (each test creates its own test data)
- [ ] Tests validate both response status codes and response body content

## Test Requirements
- [ ] Relevance ranking test: most relevant result appears first in results
- [ ] Entity type filter test: `?type=advisory` returns only advisories
- [ ] Severity filter test: `?severity=high` returns only high-severity advisories
- [ ] Date range filter test: `?created_after` and `?created_before` correctly bound results
- [ ] Combined filter test: multiple filters applied simultaneously
- [ ] Empty query test: returns empty result set
- [ ] Special character test: handles `%`, `'`, `"`, `\` without errors
- [ ] Invalid filter test: returns 400 status with error message
- [ ] Pagination test: filtered results respect pagination parameters

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 5 — Add filter parameters to search endpoint

---

`[sdlc-workflow] Description digest: sha256-md:f7b1c5d9e4a06f2b3c8d5e0a1b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4`
