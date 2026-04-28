# Task 5 — Update and Expand Search Integration Tests

## Repository
trustify-backend

## Description
Update and expand the search integration tests in `tests/api/search.rs` to cover the new full-text search ranking, filtering, and performance characteristics introduced by Tasks 1-3. The existing search tests need to be updated to validate relevance ordering and new filter parameters, and new test cases are needed to cover edge cases, filter combinations, and backward compatibility.

## Files to Modify
- `tests/api/search.rs` — update existing search tests to validate relevance ranking; add new tests for filter parameters, filter combinations, edge cases, and backward compatibility

## Implementation Notes
- Inspect the current test structure in `tests/api/search.rs` to understand the existing test patterns: how the test database is set up, how HTTP requests are made, and what assertions are used
- Follow the existing assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` as documented in the repository conventions
- Reference test patterns from sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) for consistent setup and assertion style
- Test data setup should insert entities with known, predictable content so relevance ranking assertions are deterministic — e.g., insert an SBOM with the search term in its title and another with the term only in its description, then assert the title match ranks higher
- For filter tests, insert entities spanning multiple types, severity levels, and date ranges, then verify each filter narrows results correctly
- Per constraints doc section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., parameterize across different entity type filter values)
- Per constraints doc section 5.11: add a doc comment to every test function
- Per constraints doc section 5.12: add given-when-then inline comments to non-trivial test functions
- Per constraints doc section 2: commit must reference TC-9002 in footer

## Reuse Candidates
- `tests/api/search.rs` — existing search test infrastructure (database setup, HTTP client, assertion helpers)
- `tests/api/sbom.rs` — sibling integration test file demonstrating established test patterns
- `tests/api/advisory.rs` — sibling integration test file demonstrating established test patterns

## Acceptance Criteria
- [ ] Existing search tests pass with the new full-text search implementation
- [ ] New tests validate that relevance ranking orders title matches above description matches
- [ ] New tests validate each filter parameter independently (entity_type, date_from, date_to, severity, license)
- [ ] New tests validate filter combinations work correctly
- [ ] New tests validate backward compatibility (no filters = search across all entities)
- [ ] New tests validate error handling for invalid filter values
- [ ] All test functions have doc comments
- [ ] Non-trivial test functions have given-when-then inline comments

## Test Requirements
- [ ] Test: search returns results ranked by relevance (title match > description match)
- [ ] Test: entity_type filter restricts results to specified type
- [ ] Test: date_from and date_to filters restrict results to date range
- [ ] Test: severity filter restricts advisory results by severity
- [ ] Test: license filter restricts package results by license
- [ ] Test: combining entity_type + severity returns correct intersection
- [ ] Test: empty search query returns appropriate response
- [ ] Test: special characters in search query do not cause errors
- [ ] Test: no filters applied returns all matching results across entity types

## Verification Commands
- `cargo test --test search` — all search integration tests pass
- `cargo test --test search -- --nocapture` — run with output visible to verify test coverage

## Dependencies
- Depends on: Task 3 — Add Filtering Parameters to Search Endpoint
