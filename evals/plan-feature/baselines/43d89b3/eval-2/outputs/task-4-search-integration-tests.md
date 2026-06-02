## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering performance expectations, relevance ranking validation, and filter combinations. This task consolidates test coverage for the search improvements introduced by Tasks 1-3 and ensures end-to-end behavior is validated.

## Files to Modify
- `tests/api/search.rs` — add new integration tests for relevance ranking, filtering, and combined scenarios

## Implementation Notes
Add integration tests to `tests/api/search.rs` following the existing test pattern in that file. The project uses integration tests that hit a real PostgreSQL test database, with assertions using the `assert_eq!(resp.status(), StatusCode::OK)` pattern (per Key Conventions).

Test scenarios to cover:
1. **Relevance ranking validation:** insert test data with varying match quality, perform a search query, and verify the ordering reflects relevance scoring (exact matches first).
2. **Filter isolation:** for each filter parameter (entity_type, severity, date_from, date_to), verify that applying the filter excludes non-matching results.
3. **Filter combinations:** verify that multiple filters can be combined and results satisfy all filter criteria.
4. **Edge cases:** empty result sets when filters match nothing, large result sets with pagination, and invalid filter parameter values returning error responses.
5. **Backward compatibility:** verify that requests without any new parameters return results identical to the pre-change behavior.

Reference sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) for test setup patterns, database seeding, and assertion conventions.

Per docs/constraints.md:
- §2 (Commit Rules): commits must reference TC-9002, follow Conventional Commits, and include the Assisted-by trailer.
- §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes.
- §5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs.
- §5.11: add a doc comment to every test function created.
- §5.12: add given-when-then inline comments to non-trivial test functions.

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance
- Depends on: Task 2 — Implement weighted full-text search ranking
- Depends on: Task 3 — Add filter parameters to search endpoint

## Reuse Candidates
- `tests/api/sbom.rs` — test setup patterns and assertion conventions to follow
- `tests/api/advisory.rs` — test setup patterns for advisory-related test data
- `tests/api/search.rs` — existing search tests to extend (not duplicate)

## Acceptance Criteria
- [ ] Integration tests cover relevance ranking (exact match appears first in results)
- [ ] Integration tests cover each filter parameter in isolation
- [ ] Integration tests cover combined filter scenarios
- [ ] Integration tests cover edge cases (empty results, invalid parameters)
- [ ] Integration tests verify backward compatibility (no filters = existing behavior)
- [ ] All new test functions have doc comments
- [ ] Non-trivial tests include given-when-then inline comments
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test: search with exact match term returns exact match as first result
- [ ] Test: search with `entity_type=sbom` returns only SBOMs
- [ ] Test: search with `severity=high` returns only high-severity advisories
- [ ] Test: search with `date_from` and `date_to` returns only results within range
- [ ] Test: search with `entity_type=advisory` AND `severity=critical` returns only critical advisories
- [ ] Test: search with no parameters returns all results (backward compatible)
- [ ] Test: search with invalid `entity_type` value returns error response
- [ ] Test: search with invalid date format returns error response

## Verification Commands
- `cargo test --test search` — all search tests pass
