## Repository
trustify-backend

## Description
Expand the search integration test suite to comprehensively cover the new search performance, relevance ranking, and filtering capabilities introduced in Tasks 1-3. This task ensures that all acceptance criteria from the previous tasks are verified by automated tests and that no regressions are introduced to existing search behavior.

## Files to Modify
- `tests/api/search.rs` -- Extend the existing search integration test file with new test cases covering relevance ordering, filter parameters, edge cases, and backward compatibility

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response validation.
- Tests should set up fixture data with known characteristics: e.g., advisories with different severities, SBOMs with different creation dates, entities with names that match search terms at different relevance levels.
- For relevance ordering tests, insert entities where one has the search term in its title (high relevance) and another has it only in a description field (lower relevance), then verify the response order and that `relevance_score` values are monotonically decreasing.
- For filter tests, insert a mix of entity types and verify that each filter parameter correctly narrows the result set.
- Include negative tests: invalid filter values should return `StatusCode::BAD_REQUEST`.
- Include a backward compatibility test: perform a search without any new parameters and verify the response structure matches the pre-existing format (all original fields present).
- Test configuration in `tests/Cargo.toml` should not need changes unless new test utility dependencies are required.

## Reuse Candidates
- `tests/api/search.rs` -- Existing search tests to extend. Follow the same setup, assertion, and teardown patterns.
- `tests/api/sbom.rs` -- Reference for integration test structure, fixture setup, and HTTP client usage patterns.
- `tests/api/advisory.rs` -- Reference for advisory-specific test data setup, especially for severity-based filtering tests.

## Acceptance Criteria
- [ ] All new search features (relevance ranking, filtering by entity type, filtering by severity, filtering by date range) have corresponding integration tests
- [ ] Negative test cases exist for invalid filter values (400 responses)
- [ ] Backward compatibility test verifies that searches without new parameters return the existing response format
- [ ] All existing tests in `tests/api/search.rs` continue to pass without modification
- [ ] Test coverage includes combined filter + relevance scenarios

## Test Requirements
- [ ] Test: search with a query term returns results ordered by `relevance_score` descending
- [ ] Test: `relevance_score` field is present and is a positive number for matching results
- [ ] Test: `entity_type=advisory` filter returns only advisory results
- [ ] Test: `entity_type=sbom` filter returns only SBOM results
- [ ] Test: `entity_type=package` filter returns only package results
- [ ] Test: `severity=critical&entity_type=advisory` returns only critical advisories
- [ ] Test: `severity=high` without entity_type returns 400
- [ ] Test: `created_after` filter excludes older results
- [ ] Test: `created_before` filter excludes newer results
- [ ] Test: combined filters (type + severity + date + query) work together
- [ ] Test: search without any new parameters returns backward-compatible response
- [ ] Test: invalid `entity_type` value returns 400
- [ ] Test: empty search query with filters still returns filtered results

## Dependencies
- Depends on: Task 3 -- Add filter support to the search endpoint
