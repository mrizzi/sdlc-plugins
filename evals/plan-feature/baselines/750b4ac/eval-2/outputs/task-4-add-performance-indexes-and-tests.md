# Task 4 — Add database indexes on filter columns and comprehensive search integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on columns used for filtering (entity type, severity, date columns) to improve search query performance when filters are applied. Additionally, add comprehensive integration tests covering the full search improvement feature: full-text search, relevance ranking, filter combinations, and edge cases. This addresses the "search should be faster" non-functional requirement from TC-9002 and ensures complete test coverage for the feature.

**Assumption pending clarification:** The "should be fast enough" non-functional requirement has no measurable target. This task adds structural optimizations (B-tree indexes on filter columns) and basic performance validation via test execution time, but does not enforce a specific latency SLA. A follow-up performance benchmarking effort with concrete targets should be defined separately.

## Files to Create
- `migration/src/m0003_filter_column_indexes/mod.rs` — migration adding B-tree indexes on severity, date, and type columns used for search filtering

## Files to Modify
- `migration/src/lib.rs` — register the new index migration module
- `tests/api/search.rs` — add comprehensive integration tests covering full-text search, relevance ranking, filters, filter combinations, edge cases, and performance characteristics

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration structure.
- Add B-tree indexes on columns used in WHERE clauses by the search filters: severity column on the advisory table, date columns on all entity tables, and any discriminator column used for entity type filtering.
- The existing integration test file `tests/api/search.rs` contains search endpoint tests — inspect it to understand the existing test patterns before adding new tests.
- Follow the integration test pattern: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
- Ensure tests cover the complete search feature lifecycle: create test data, perform searches with various query/filter combinations, verify result ordering and filter correctness.
- All handlers return `Result<T, AppError>` with `.context()` wrapping — test error cases return appropriate status codes.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits and reference TC-9002 in the footer.
- Per docs/constraints.md §5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs.
- Per docs/constraints.md §5.11: add a doc comment to every test function.
- Per docs/constraints.md §5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern for creating indexes
- `tests/api/search.rs` — existing search integration tests; follow established patterns for test setup, data creation, and assertions
- `tests/api/sbom.rs` — SBOM endpoint integration tests; demonstrates test structure and patterns used across the test suite
- `tests/api/advisory.rs` — advisory endpoint integration tests; demonstrates testing with severity-related data

## Acceptance Criteria
- [ ] B-tree indexes exist on severity, date, and type columns used for search filtering
- [ ] Migration runs successfully and is registered in `migration/src/lib.rs`
- [ ] Comprehensive integration tests cover: basic full-text search, relevance ranking order, each filter type individually, filter combinations, empty/invalid queries, backward compatibility (no filters)
- [ ] All existing tests continue to pass (no regressions)
- [ ] Test suite demonstrates that indexed queries return results within acceptable time for the test dataset

## Test Requirements
- [ ] Integration test: full-text search returns relevant results for known test data
- [ ] Integration test: results are ordered by relevance score (most relevant first)
- [ ] Integration test: entity_type filter returns only matching entity types
- [ ] Integration test: severity filter returns only matching severity levels
- [ ] Integration test: date range filter returns only results within the range
- [ ] Integration test: combining entity_type + date range filter works correctly
- [ ] Integration test: empty search query returns an appropriate response (error or empty results)
- [ ] Integration test: special characters in search query are handled without errors
- [ ] Integration test: search with no matching results returns empty PaginatedResults

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test --test search` — all search integration tests pass
- `cargo test` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 3 — Add filter parameters to the search endpoint

[sdlc-workflow] Description digest: sha256-md:11d6cd4df5fc7a86c1ee6455a21b5c28ce26e1819a79ce516b08fbf26ac2f51b
