## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the enhanced search functionality and
filtering capabilities introduced in Tasks 2-4. This validates the "search should
be faster", "results should be more relevant", and "Add filters" requirements from
TC-9002, and satisfies the NFR "Don't break existing functionality" by verifying
backward compatibility.

## Files to Modify
- `tests/api/search.rs` — Add integration tests for relevance-scored search, filter parameters, edge cases (empty queries, invalid filters), and backward compatibility with existing search behavior

## Implementation Notes
Follow the existing integration test patterns in `tests/api/search.rs` (search
endpoint integration tests). The test file already exists and contains tests for
the search endpoint.

Tests should use the established pattern from `tests/api/`:
- Set up test data in a real PostgreSQL test database
- Make HTTP requests to the search endpoint
- Assert response status with `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Parse response bodies and validate result ordering, filtering, and content

Key test scenarios to cover:

**Relevance scoring tests:**
- Insert multiple entities with varying text content
- Search for a specific term and verify the most relevant result appears first
- Verify exact matches rank above partial matches

**Filter tests:**
- Test each filter parameter individually (entity_type, severity, date_from, date_to, license)
- Test filter combinations (AND semantics)
- Test invalid filter values return 400 status

**Backward compatibility tests:**
- Verify existing search queries (without filters) return the same structure
- Verify pagination works with filtered results

Reference the test patterns in sibling test files:
- `tests/api/sbom.rs` — SBOM endpoint integration tests (for test setup patterns)
- `tests/api/advisory.rs` — Advisory endpoint integration tests (for assertion patterns)

Per CONVENTIONS.md §Testing: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Reuse test setup patterns (database seeding, HTTP client configuration) from existing SBOM integration tests
- `tests/api/advisory.rs` — Reuse assertion patterns from existing advisory integration tests

## Acceptance Criteria
- [ ] Integration tests validate that search results are ordered by relevance score
- [ ] Integration tests validate each filter parameter works correctly in isolation
- [ ] Integration tests validate filter combinations use AND semantics
- [ ] Integration tests validate invalid filters return 400 Bad Request
- [ ] Integration tests validate backward compatibility (no filters = original behavior)
- [ ] All new tests pass against a real PostgreSQL test database
- [ ] All existing tests in `tests/api/` continue to pass

## Test Requirements
- [ ] Relevance scoring: exact match appears before partial match in results
- [ ] Relevance scoring: search with no results returns empty paginated response
- [ ] Filter: entity_type filter restricts results to specified type
- [ ] Filter: severity filter returns only matching advisories
- [ ] Filter: date range filter returns only SBOMs within range
- [ ] Filter: license filter returns only matching packages
- [ ] Filter: combining entity_type + severity narrows results correctly
- [ ] Filter: invalid severity value returns 400
- [ ] Filter: date_from after date_to returns 400 or empty results
- [ ] Backward compatibility: search without filters matches original response shape

## Verification Commands
- `cargo test --test api -- search` — Run search integration tests; all should pass

## Dependencies
- Depends on: Task 3 — Add filter query parameters to search endpoint
- Depends on: Task 4 — Add filter support to entity list endpoints
