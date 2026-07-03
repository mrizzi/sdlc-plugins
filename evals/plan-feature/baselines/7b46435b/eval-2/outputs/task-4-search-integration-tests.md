## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search integration tests to cover the new performance indexes, relevance scoring, and filter parameters introduced in Tasks 1-3. This task adds comprehensive test coverage for all search improvements in TC-9002, ensuring that the enhanced search behavior is verified against a real PostgreSQL test database and that existing search functionality is not broken.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": "RHTPA 1.6.0" }

## Files to Modify
- `tests/api/search.rs` -- add new integration test cases for: relevance ordering, entity type filtering, severity filtering, combined filters, empty results with filters, search performance with indexes, backwards compatibility of existing search behavior

## Implementation Notes
Follow the existing integration test pattern in `tests/api/search.rs` which uses a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.

The new test cases should:

1. **Relevance ordering tests**: seed the database with multiple entities where one has an exact title match and others have partial matches. Assert that the exact match appears first in the results and that `relevance_score` is present and decreasing.

2. **Entity type filter tests**: seed SBOMs, advisories, and packages. Search with `entity_type=sbom` and assert only SBOM results are returned. Repeat for advisory and package types.

3. **Severity filter tests**: seed advisories with different severity levels. Search with `severity=critical` and assert only critical advisories are returned.

4. **Combined filter tests**: search with both `entity_type=advisory&severity=high` and assert correct filtering.

5. **Error handling tests**: send invalid filter values and assert 400 Bad Request responses.

6. **Backwards compatibility tests**: ensure existing test cases pass unchanged and that searching without filters returns results from all entity types.

Reference the existing test setup patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for database seeding and HTTP client usage.

Per CONVENTIONS.md: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/search.rs` -- existing search integration tests; extend with new test cases following the same patterns
- `tests/api/sbom.rs` -- SBOM endpoint integration tests; reference for database seeding patterns and HTTP client usage
- `tests/api/advisory.rs` -- Advisory endpoint integration tests; reference for advisory-specific test data setup

## Acceptance Criteria
- [ ] Integration tests verify relevance ordering (exact match ranks higher than partial match)
- [ ] Integration tests verify entity type filtering (each type returns only matching entities)
- [ ] Integration tests verify severity filtering (returns only advisories with matching severity)
- [ ] Integration tests verify combined filters work with AND semantics
- [ ] Integration tests verify invalid filter values return 400 Bad Request
- [ ] All existing search integration tests continue to pass without modification
- [ ] Test coverage includes edge cases: empty results, no filters (backwards compatibility)

## Test Requirements
- [ ] Minimum 8 new test cases covering: relevance ordering (2), entity type filter (3), severity filter (1), combined filters (1), error handling (1)
- [ ] All tests use the real PostgreSQL test database pattern established in the project
- [ ] No test relies on specific ordering when relevance scores are equal

## Verification Commands
- `cargo test --test search` -- all search integration tests pass (existing and new)
- `cargo test --test search -- --nocapture` -- view test output for debugging

## Dependencies
- Depends on: Task 3 -- Add filter parameters to search endpoint
