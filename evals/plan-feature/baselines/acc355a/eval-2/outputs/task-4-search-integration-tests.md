# Task 4 — Expand search integration tests for performance, ranking, and filters

## Repository
trustify-backend

## Target Branch
main

## Description
Expand the existing search integration test suite to comprehensively cover the new search capabilities: full-text search indexing, relevance ranking, entity-type filtering, severity filtering, and combined filter scenarios. This task ensures end-to-end test coverage for all search improvements introduced in Tasks 1-3.

## Files to Modify
- `tests/api/search.rs` — Add integration tests covering: ranked search result ordering, entity-type filtering, severity filtering, combined filter scenarios, empty/invalid query handling, and pagination with filters

## Implementation Notes
- The existing test file `tests/api/search.rs` contains search endpoint integration tests. Extend it with new test functions rather than modifying existing tests, to preserve backward-compatible test coverage.
- Follow the existing test pattern in `tests/api/search.rs` and sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`) which hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Test data setup should create entities across all three types (SBOMs, advisories, packages) with known text content so that search ranking and filtering can be deterministically verified.
- For ranking tests: insert entities with varying degrees of match quality (exact match, partial match, no match) and verify results are returned in descending relevance order.
- For filter tests: insert entities of each type and verify that filter parameters correctly restrict results.
- For performance-related tests: verify that search queries with indexes return results within a reasonable time bound (use a test timeout or wall-clock assertion if the test framework supports it). This serves as a regression guard, not a benchmark.

## Reuse Candidates
- `tests/api/search.rs` — Existing search integration tests to extend with new test cases
- `tests/api/sbom.rs` — SBOM endpoint integration tests demonstrating the project's test setup patterns, assertion style, and test database usage
- `tests/api/advisory.rs` — Advisory endpoint integration tests as another reference for test patterns

## Acceptance Criteria
- [ ] Integration tests verify that search results are returned in relevance-ranked order
- [ ] Integration tests verify entity_type filter for each entity type (sbom, advisory, package)
- [ ] Integration tests verify severity filter for advisory results
- [ ] Integration tests verify combined filters (entity_type + severity)
- [ ] Integration tests verify backward compatibility (no filters returns all types)
- [ ] Integration tests verify error handling for invalid filter values
- [ ] All new tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: search with a specific query returns results ranked by relevance score (most relevant first)
- [ ] Test: `entity_type=sbom` filter returns only SBOMs
- [ ] Test: `entity_type=advisory` filter returns only advisories
- [ ] Test: `entity_type=package` filter returns only packages
- [ ] Test: `severity=critical` filter returns only critical-severity advisories
- [ ] Test: combined `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Test: no filters returns results from all entity types
- [ ] Test: empty search query returns appropriate response
- [ ] Test: search results include pagination metadata (total count, offset, limit)

## Dependencies
- Depends on: Task 3 — Add search filter support
