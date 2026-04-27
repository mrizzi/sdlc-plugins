# Task 5 — Add comprehensive integration tests for search improvements

**Feature:** TC-9002 — Improve search experience
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Description
Add comprehensive integration tests covering the new search functionality: filters, relevance scoring, pagination, and sorting. While individual tasks include basic test requirements, this task provides end-to-end integration test coverage for the complete search improvement feature, including edge cases and combined scenarios.

## Files to Modify
- `tests/api/search.rs` — Add new integration test functions for filters, relevance scoring, pagination, sorting, and combined scenarios

## Implementation Notes
- Follow the existing test patterns in `tests/api/search.rs` — inspect this file first to understand the test setup, database seeding, and assertion patterns
- Reference the test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for examples of list/filter/pagination testing
- Tests should use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the codebase (per repo conventions)
- Tests must hit a real PostgreSQL test database (per repo conventions under Testing)
- Seed test data that includes multiple entity types (SBOMs, advisories, packages) with varying names, descriptions, severities, and dates to enable meaningful filter and relevance testing
- Per docs/constraints.md Section 5.11: every test function must have a doc comment
- Per docs/constraints.md Section 5.12: non-trivial test functions must include given-when-then inline comments
- Per docs/constraints.md Section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs (e.g., different filter combinations), applying the Meszaros heuristic

## Reuse Candidates
- `tests/api/search.rs` — Existing search tests; follow the same setup and assertion patterns
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for pagination and list testing patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for filter testing patterns

## Acceptance Criteria
- [ ] Tests cover filtering by entity type (SBOM, advisory, package)
- [ ] Tests cover filtering by severity for advisories
- [ ] Tests cover filtering by date range
- [ ] Tests cover combined filters (entity type + severity + date range)
- [ ] Tests verify relevance scoring (name match ranks higher than description match)
- [ ] Tests verify pagination (offset/limit) returns correct subsets and total counts
- [ ] Tests verify sorting options (relevance, date, name)
- [ ] Tests verify backward compatibility (no filters returns all results)
- [ ] Tests verify error handling (invalid filter values return 400)
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Entity type filter tests: one per entity type + combined types
- [ ] Severity filter test: filter advisories by specific severity level
- [ ] Date range filter test: filter by date_from, date_to, and both combined
- [ ] Combined filter test: entity_type + severity + date range
- [ ] Relevance ranking test: term in title vs term in description
- [ ] Pagination test: verify offset/limit behavior with known data set size
- [ ] Sort test: verify each sort option produces correctly ordered results
- [ ] Error test: invalid entity_type value returns 400
- [ ] Error test: invalid date format returns 400
- [ ] Backward compatibility test: no parameters returns all results as before

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo test -p tests` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add search filter parameters to the search endpoint
- Depends on: Task 4 — Ensure search endpoint uses PaginatedResults with sorting support
