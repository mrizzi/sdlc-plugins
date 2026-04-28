## Repository
trustify-backend

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search accuracy, relevance ranking correctness, filter combinations, performance characteristics, and backward compatibility. This task ensures the search improvements from Tasks 1-3 are thoroughly validated end-to-end against a real PostgreSQL test database, following the project's established integration test patterns.

## Files to Modify
- `tests/api/search.rs` — Extend the existing search integration tests with new test cases covering full-text search, relevance ranking, filtering, and backward compatibility

## Implementation Notes
- The existing integration tests are in `tests/api/search.rs` and follow the pattern of hitting a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` assertions (per repository conventions).
- Review existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for setup, fixtures, and assertion conventions — follow the same patterns for consistency.
- Test data setup should insert entities with known, distinct text content so that relevance ranking can be verified deterministically. For example:
  - Insert an SBOM with name "critical vulnerability scanner" and an advisory with title "critical security advisory" — a search for "critical" should return both, ranked by relevance.
  - Insert entities with non-overlapping text to verify that search correctly excludes non-matching entities.
- For filter tests, insert entities with varied attributes (different entity types, severity levels, creation dates) and verify that each filter correctly narrows results.
- For backward compatibility tests, replicate queries that work with the current search endpoint and verify they continue to return results in the same response format (`PaginatedResults<T>` from `common/src/model/paginated.rs`).
- Verify that the search endpoint continues to return results at `GET /api/v2/search` without requiring any new parameters (all filters are optional).
- All test functions must include a doc comment explaining what the test verifies, per project conventions.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test setup patterns, fixture creation, and assertion style
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for test data with severity fields
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; verify search responses conform to this shape
- `modules/search/src/endpoints/mod.rs` — Search endpoint route definition; reference for the exact URL path and parameter names

## Acceptance Criteria
- [ ] Integration tests cover full-text search returning ranked results
- [ ] Integration tests cover each individual filter parameter (entity_type, severity, created_after, created_before)
- [ ] Integration tests cover combined filters (multiple filters applied simultaneously)
- [ ] Integration tests verify backward compatibility (no-filter search returns results in existing format)
- [ ] Integration tests verify that empty search results return a valid empty `PaginatedResults` response (not an error)
- [ ] Integration tests verify that invalid filter values return 400 Bad Request
- [ ] All new test functions include doc comments
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: full-text search with a known term returns matching entities ranked by relevance
- [ ] Test: full-text search with a term matching multiple entity types returns cross-entity results
- [ ] Test: full-text search with a non-matching term returns empty results with 200 OK
- [ ] Test: filter by `entity_type=sbom` excludes advisories and packages from results
- [ ] Test: filter by `severity=critical` returns only critical-severity advisories
- [ ] Test: filter by date range (`created_after`, `created_before`) returns only entities within the range
- [ ] Test: combined filters (entity_type + severity + date range) narrow results correctly
- [ ] Test: search with no query and no filters returns all entities (backward compatibility)
- [ ] Test: invalid `entity_type` parameter returns 400 Bad Request
- [ ] Test: search response conforms to `PaginatedResults<T>` shape with `items` array and `total` count

## Verification Commands
- `cargo test -p tests -- search` — search integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 3 — Add filter parameters to search endpoint
