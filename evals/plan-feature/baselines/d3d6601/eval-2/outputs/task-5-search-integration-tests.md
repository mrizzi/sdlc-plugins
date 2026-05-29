## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the improved search functionality, covering full-text search relevance, filter combinations, edge cases, and performance characteristics. This task ensures the search improvements from TC-9002 are well-tested and provides a regression safety net for future changes.

**Ambiguity note:** The feature description's non-functional requirement "should be fast enough" provides no measurable threshold. **Assumption pending clarification:** Tests validate that search queries complete within a reasonable time bound (e.g., assert response within 2 seconds for test data set), but this is a smoke test, not a formal performance benchmark. A formal performance target should be established with the product owner and tested in a production-representative environment.

## Files to Modify
- `tests/api/search.rs` — extend existing search integration tests with new test cases for full-text search relevance, filter functionality, filter combinations, edge cases, and basic performance assertions

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` — inspect the current test structure to understand setup, assertion patterns, and test data provisioning
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern used throughout the test suite
- Tests should hit a real PostgreSQL test database per the repository testing convention
- Test data setup should create SBOMs, advisories, and packages with known attributes to enable deterministic assertions on search and filter results
- Relevance tests should verify ordering: an exact title match should rank higher than a partial description match
- Filter tests should verify each filter independently and in combination
- Edge case tests should cover: empty search query, special characters in search query (e.g., `"openssl/1.1"`), very long search queries, filters with no matching results
- Per docs/constraints.md §5.11: add a doc comment to every test function
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions
- Per docs/constraints.md §2 (Commit Rules): use Conventional Commits format with Jira issue ID in footer

## Reuse Candidates
- `tests/api/search.rs` — existing search tests; follow the same structure and extend
- `tests/api/sbom.rs` — SBOM endpoint integration tests showing test setup and assertion patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests showing test data creation

## Acceptance Criteria
- [ ] Relevance ordering tests verify that exact matches rank higher than partial matches
- [ ] Filter tests cover severity, license, date range, and entity type filters
- [ ] Combined filter tests verify AND composition behavior
- [ ] Edge case tests cover empty queries, special characters, and no-result scenarios
- [ ] All new tests pass against the test database
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Test: full-text search returns relevant results ranked by score
- [ ] Test: severity filter returns only matching advisories
- [ ] Test: license filter returns only matching packages
- [ ] Test: date range filter returns only SBOMs within the specified range
- [ ] Test: entity type filter returns only the specified entity type
- [ ] Test: multiple filters combine with AND logic
- [ ] Test: empty search query returns a defined response (not an error)
- [ ] Test: special characters in search query do not cause errors
- [ ] Test: search with filters but no matching results returns empty paginated response

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `cargo test --test api` — full integration test suite passes

## Dependencies
- Depends on: Task 4 — Add search filters (tests cover filter functionality)

[sdlc-workflow] Description digest: sha256:a65f168d4be8a6df560814bac7fba48618ad4108c18dbefa9c377ced490190d3
