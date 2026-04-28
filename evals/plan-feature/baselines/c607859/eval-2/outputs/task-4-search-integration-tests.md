# Task 4 — Add Integration Tests for Search Improvements

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the search improvements introduced by
TC-9002: full-text search ranking, filter parameters, and performance
characteristics. This task ensures that the search improvements are verified
end-to-end against a real PostgreSQL database, following the project's
established integration test pattern.

## Files to Modify
- `tests/api/search.rs` — add new integration test cases for ranked search,
  filtering, combined queries, edge cases, and performance

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/search.rs` and
  sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`).
- Tests hit a real PostgreSQL test database, as specified in the project's
  key conventions. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern
  established in the codebase.
- Test data setup: insert a known set of SBOMs, advisories, and packages with
  distinct names, severities, and dates so that ranking and filtering assertions
  are deterministic.
- Per constraints.md §5.11: add a doc comment to every test function.
- Per constraints.md §5.12: add given-when-then inline comments to non-trivial
  test functions that have distinct setup, action, and assertion phases.
- Per constraints.md §5.9: prefer parameterized tests when multiple test cases
  exercise the same behavior with different inputs (e.g., different filter
  combinations), but per §5.10 only if the project already uses parameterized
  test patterns — check sibling tests first.

### Test categories to cover:

**Relevance ranking tests:**
- Search for a term that appears in one entity's title and another entity's
  description — verify the title match ranks higher
- Multi-word query — verify entities matching more terms rank higher
- Exact phrase match — verify higher ranking than partial match

**Filter tests:**
- Entity type filter — verify each type returns only matching results
- Severity filter — verify advisory results are filtered correctly
- Date range filter — verify only entities within range are returned
- Combined filters — verify filters compose correctly with each other and
  with text search queries

**Edge case tests:**
- Empty query with filters — verify filters work without text search
- Special characters in query — verify no errors
- Invalid filter values — verify 400 response
- No results — verify empty result set with correct pagination metadata

**Backward compatibility tests:**
- Existing search behavior without new parameters — verify no regression

## Reuse Candidates
- `tests/api/search.rs` — existing search integration tests; follow the
  same setup/teardown patterns and assertion style
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for
  test data setup and HTTP client usage patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference
  for test data with severity field

## Acceptance Criteria
- [ ] All new tests pass against a PostgreSQL test database
- [ ] Relevance ranking is verified with deterministic test data
- [ ] All filter types are tested individually and in combination
- [ ] Edge cases (empty query, special characters, invalid filters) are covered
- [ ] Backward compatibility is verified (existing behavior unchanged)
- [ ] No existing tests are broken by the changes

## Test Requirements
- [ ] Relevance ranking: title match ranks above description-only match
- [ ] Relevance ranking: multi-term match ranks above single-term match
- [ ] Filter: entity_type=sbom returns only SBOMs
- [ ] Filter: entity_type=advisory returns only advisories
- [ ] Filter: severity=critical returns only critical advisories
- [ ] Filter: date range returns only entities within range
- [ ] Combined: text query + entity_type + severity returns correct results
- [ ] Edge: empty query with filters returns filtered results
- [ ] Edge: special characters do not cause errors
- [ ] Edge: invalid entity_type returns 400
- [ ] Backward: search without new params returns same results as before

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 3 — Add Filter Parameters to Search Endpoint
