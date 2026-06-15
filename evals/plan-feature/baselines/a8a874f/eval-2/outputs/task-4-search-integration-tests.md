# Task 4: Add integration tests for search improvements

## Repository

trustify-backend

## Target Branch

main

## Description

Expand the existing search integration test suite to cover the new relevance ranking and filtering capabilities added in Tasks 2 and 3. The existing test file at `tests/api/search.rs` covers the basic search endpoint; this task adds comprehensive tests for relevance ordering, filter parameters, filter validation, and combined search-with-filters scenarios.

## Files to Modify

- `tests/api/search.rs` — Add new integration test functions covering relevance ranking, filter parameters, filter validation errors, and combined query+filter scenarios.

## Implementation Notes

- Follow the existing integration test pattern in `tests/api/search.rs` and sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Each test function should set up specific test data (e.g., advisories with known severities, entities with known names/descriptions) to produce deterministic and verifiable results.
- For relevance ranking tests: insert entities where the search term appears in the name for one and only in the description for another, then assert the name-match entity appears first in results.
- For filter tests: insert a mix of entity types and severities, then assert that filtered queries return only the expected subset.
- For date range tests: insert entities with known creation dates spanning a range, then assert the date filter boundaries work correctly.
- For error handling tests: send requests with invalid filter values and assert `400 Bad Request` responses.
- Use `PaginatedResults<T>` response deserialization to inspect result ordering and content, consistent with how `common/src/model/paginated.rs` structures responses.

## Reuse Candidates

- `tests/api/sbom.rs` — Reference for test setup patterns, HTTP client configuration, and assertion style.
- `tests/api/advisory.rs` — Reference for test data insertion patterns for advisories with severity fields.

## Acceptance Criteria

- [ ] Tests cover relevance ranking: name matches rank above description-only matches
- [ ] Tests cover entity type filtering: single type and multi-type selection
- [ ] Tests cover severity filtering for advisories
- [ ] Tests cover date range filtering with various boundary combinations
- [ ] Tests cover combined text query with filters
- [ ] Tests cover invalid filter input (400 responses)
- [ ] Tests cover backward compatibility (no filters = unfiltered results)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements

- [ ] Relevance ordering test: insert 2+ entities, search by term that appears in name of entity A and description of entity B, assert A appears before B
- [ ] Type filter test: insert mixed entities, filter by `type=advisory`, assert only advisories returned
- [ ] Multi-type filter test: filter by `type=sbom&type=package`, assert both types returned, advisories excluded
- [ ] Severity filter test: insert advisories with different severities, filter by `severity=high`, assert only high-severity advisories returned
- [ ] Date range test: insert entities with dates in and outside range, assert only in-range entities returned
- [ ] Combined test: apply text query and type filter together, assert both constraints are respected
- [ ] Invalid filter test: send `type=invalid`, assert 400 response
- [ ] Empty filter test: send search with no filters, assert all results returned

## Dependencies

- **Task 2** — Relevance ranking must be implemented before relevance tests can pass
- **Task 3** — Filter parameters must be implemented before filter tests can pass

---

[Description digest: sha256-md:d9f4a1b25c7e0938f1b4d2e6c5f7a9c1e3f5b7d9a1c3e5f7b9d1a3c5e7f9b1d3 would be posted as a comment]
