## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance ranking, filter combinations, edge cases, and backward compatibility. These tests exercise the `GET /api/v2/search` endpoint end-to-end against a real PostgreSQL test database, validating that the search improvements from Tasks 1-3 work correctly together.

## Files to Modify
- `tests/api/search.rs` — add integration tests for relevance ranking, filter parameters, filter combinations, edge cases, and backward compatibility

## Implementation Notes
Add tests to the existing `tests/api/search.rs` file, following the established integration test patterns visible in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.

Tests to add:

1. **Relevance ranking tests:**
   - Insert test entities with varying match quality (exact match, partial match, no match).
   - Query and verify results are ordered by relevance (exact match first).
   - Verify `ts_rank` ordering by checking that a document containing the search term in its title ranks above one with the term only in a description.

2. **Entity type filter tests:**
   - Insert SBOMs, advisories, and packages.
   - Query with `type=advisory` and verify only advisories are returned.
   - Query with `type=sbom` and verify only SBOMs are returned.
   - Query with `type=package` and verify only packages are returned.

3. **Severity filter tests:**
   - Insert advisories with different severities (critical, high, medium, low).
   - Query with `severity=critical` and verify only critical advisories are returned.

4. **License filter tests:**
   - Insert packages with different licenses.
   - Query with `license=MIT` and verify only MIT-licensed packages are returned.

5. **Combined filter tests:**
   - Query with `q=openssl&type=advisory&severity=high` and verify results match all criteria.

6. **Edge case tests:**
   - Empty query string returns all results (backward compatibility).
   - Query with no matches returns empty `PaginatedResults` with total=0.
   - Special characters in query do not cause errors.
   - Invalid filter value returns 400 status.

7. **Pagination with filters:**
   - Apply a filter that returns multiple results, use offset/limit, verify pagination is correct.

Follow the test structure conventions in `tests/api/sbom.rs` — use similar setup/teardown patterns, HTTP client configuration, and assertion styles. Add doc comments to each test function explaining what behavior it validates.

Per constraints (docs/constraints.md):
- Commit messages must follow Conventional Commits and reference TC-9002 (§2.1, §2.2).
- Include `--trailer="Assisted-by: Claude Code"` on all commits (§2.3).
- Keep changes scoped to the files listed (§5.1).
- Add a doc comment to every test function (§5.11).
- Add given-when-then inline comments to non-trivial test functions (§5.12).
- Prefer parameterized tests when multiple cases exercise the same behavior with different inputs, applying the Meszaros heuristic (§5.9), but only if sibling tests use parameterized patterns (§5.10).

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; follow the same test setup, HTTP client, and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reuse test data setup patterns for advisories with severity values
- `tests/api/search.rs` — existing search tests; extend rather than duplicate existing test infrastructure

## Acceptance Criteria
- [ ] All new integration tests pass against a PostgreSQL test database
- [ ] Tests cover relevance ranking (ordered by `ts_rank`)
- [ ] Tests cover each filter type individually (type, severity, license)
- [ ] Tests cover filter combinations (multiple filters AND-combined with search query)
- [ ] Tests cover edge cases (empty query, no matches, special characters, invalid filter)
- [ ] Tests cover pagination with filters
- [ ] Tests verify backward compatibility (no filters = existing behavior)
- [ ] All test functions have doc comments

## Test Requirements
- [ ] Relevance ranking: exact title match ranks above description-only match
- [ ] Entity type filter: `type=advisory` excludes non-advisory entities
- [ ] Severity filter: `severity=critical` returns only critical-severity advisories
- [ ] License filter: `license=MIT` returns only MIT-licensed packages
- [ ] Combined filters: `q=openssl&type=advisory&severity=high` narrows correctly
- [ ] Empty query: returns all entities (backward compatible)
- [ ] No matches: returns empty PaginatedResults with total=0 and status 200
- [ ] Special characters: search query with `%`, `'`, `"` does not error
- [ ] Invalid filter: `type=invalid` returns 400 status
- [ ] Pagination: offset/limit work correctly with active filters

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add search filters (tests exercise the complete search feature including filters)

[sdlc-workflow] Description digest: sha256:e0e947de0ae016c48ccf060d0255f962b548b4116b45e70c4a8170c61cd17612
