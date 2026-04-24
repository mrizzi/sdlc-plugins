# Task 5 — Add Search Integration Tests

## Repository
trustify-backend

## Description
Add comprehensive integration tests for the enhanced search functionality including full-text ranking, filtering, and caching. This task consolidates test coverage for the new search features to verify end-to-end behavior against a real PostgreSQL test database, following the project's established integration test patterns.

## Files to Modify
- `tests/api/search.rs` — extend existing search integration tests with new test cases covering full-text ranking, filter combinations, caching behavior, and backward compatibility

## Implementation Notes
- Follow the existing integration test pattern established in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`. These tests use the `assert_eq!(resp.status(), StatusCode::OK)` pattern and hit a real PostgreSQL test database.
- Test data setup: create test SBOMs, advisories, and packages with known names and descriptions so full-text ranking can be verified deterministically.
- For ranking tests: insert entities with varying degrees of match quality (exact title match, partial description match, no match) and verify the order of results.
- For filter tests: insert entities of different types, severities, and dates, then verify that each filter correctly narrows the result set.
- For caching tests: verify that `Cache-Control` headers are present and correctly configured.
- For backward compatibility: verify that the existing search endpoint contract (without new parameters) continues to work identically.
- Per constraints doc 5.2: read the existing test files to understand setup patterns, fixtures, and assertion styles before writing new tests.
- Per constraints doc 5.11: add a doc comment to every test function.
- Per constraints doc 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/search.rs` — existing search endpoint integration tests to extend
- `tests/api/sbom.rs` — SBOM endpoint integration test patterns (test setup, assertions)
- `tests/api/advisory.rs` — advisory endpoint integration test patterns

## Acceptance Criteria
- [ ] Integration tests cover full-text search ranking (relevance ordering)
- [ ] Integration tests cover each filter type (entity_type, severity, date_range)
- [ ] Integration tests cover filter combinations
- [ ] Integration tests verify backward compatibility (no filters = same behavior)
- [ ] Integration tests verify error handling for invalid filter values
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: search with a query term returns results ordered by relevance score
- [ ] Test: exact title match ranks higher than partial description match
- [ ] Test: entity_type filter returns only results of the specified type
- [ ] Test: severity filter returns only advisories with matching severity
- [ ] Test: date_range filter excludes results outside the specified range
- [ ] Test: combining entity_type + severity filters works correctly
- [ ] Test: request without any new parameters returns expected results (backward compat)
- [ ] Test: invalid entity_type returns 400 error
- [ ] Test: invalid date format returns 400 error

## Verification Commands
- `cargo test --test api -- search` — all search integration tests pass

## Dependencies
- Depends on: Task 4 — Add Response Caching to Search Endpoint (all search features must be implemented before comprehensive integration testing)
