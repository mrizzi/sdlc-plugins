## Repository
trustify-backend

## Description
Add comprehensive integration tests for the improved search functionality, covering relevance ranking, filter behavior, and performance characteristics.

## Files to Modify
- `tests/api/search.rs` — add test cases for relevance ranking, filter parameters, and combined filter+search behavior

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` for test setup, database fixtures, and assertion style.
- Tests must hit a real PostgreSQL test database, consistent with project convention.
- Set up test data with entities that have known characteristics: different entity types, severity levels, dates, and text in title vs description fields.

## Reuse Candidates
- `tests/api/search.rs` — existing search tests to extend
- `tests/api/sbom.rs` — test data setup patterns
- `tests/api/advisory.rs` — advisory fixture creation patterns

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover relevance ranking, each filter type, filter combinations, and edge cases
- [ ] Tests follow existing `tests/api/` patterns

## Test Requirements
- [ ] Test: title matches rank higher than description matches in search results
- [ ] Test: `entity_type=advisory` filter returns only advisory results
- [ ] Test: `severity=critical` filter returns only critical advisories
- [ ] Test: `date_from` and `date_to` filter narrows results correctly
- [ ] Test: combining entity_type and severity filters works with AND logic
- [ ] Test: search with no matching results returns empty set

## Dependencies
- Depends on: Task 3 — Search filters
