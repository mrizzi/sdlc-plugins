# Task 2: Optimize SearchService Query Execution

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to leverage the new database indexes (Task 1) and optimize query execution for faster search response times. This addresses the TC-9002 requirement that "search should be faster."

**Assumption (pending clarification)**: The current `SearchService` performs search using `LIKE` or `ILIKE` queries (a common pattern in unoptimized search implementations). This task assumes the optimization path is to switch to PostgreSQL full-text search using `to_tsvector` / `to_tsquery` functions that utilize the GIN indexes created in Task 1. If the current implementation already uses full-text search, the optimization may instead focus on query plan tuning.

**Assumption (pending clarification)**: No specific latency target was provided ("should be fast enough"). This task assumes a reasonable target of p95 < 500ms for searches against datasets up to 100,000 entities. This target should be validated with the product owner.

**Assumption (pending clarification)**: Search is assumed to query across all three entity types (SBOMs, advisories, packages) in a single request, matching the existing behavior in `modules/search/src/endpoints/mod.rs` (`GET /api/v2/search`). If search should be scoped to individual entity types, the approach would differ.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace or optimize the core search query logic to use PostgreSQL full-text search (`to_tsvector`/`to_tsquery`) instead of pattern matching; add query result caching using `tower-http` cache patterns
- `modules/search/Cargo.toml` — Add any required dependencies for full-text search query construction (if SeaORM extensions are needed)
- `common/src/db/query.rs` — Add a shared full-text search query builder helper that constructs `tsvector`/`tsquery` conditions, following the existing pattern of shared query helpers (filtering, pagination, sorting) in this file

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` handles full-text search across entities. Refactor its query construction to:
  1. Parse the user's search term into a `tsquery` (handling multi-word queries by joining with `&` for AND semantics or `|` for OR semantics).
  2. Execute the search using `to_tsvector('english', column) @@ to_tsquery('english', ?)` against the GIN-indexed columns from Task 1.
  3. Use `UNION ALL` or sequential queries across sbom, advisory, and package tables, then merge results.
- Add a reusable full-text search builder function in `common/src/db/query.rs` alongside the existing filtering and pagination helpers. This function should accept a search term and column list, and return a SeaORM `Condition`.
- Follow the error handling convention: all service methods return `Result<T, AppError>` with `.context()` wrapping, as documented in `common/src/error.rs`.
- Consider adding query-level `LIMIT` pushdown to avoid fetching unbounded rows before pagination is applied (the existing pagination pattern is in `common/src/model/paginated.rs`).
- Leverage connection pool limiter in `common/src/db/limiter.rs` to prevent search queries from starving other operations.

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`tsvector`/`tsquery`) for query execution
- [ ] A reusable full-text search query helper is added to `common/src/db/query.rs`
- [ ] Search queries hit GIN indexes (verified by `EXPLAIN ANALYZE` in development)
- [ ] Search results are returned with pagination via `PaginatedResults<T>` from `common/src/model/paginated.rs`
- [ ] Existing search endpoint `GET /api/v2/search` continues to function correctly
- [ ] Error handling follows `Result<T, AppError>` with `.context()` pattern

## Test Requirements
- [ ] Existing tests in `tests/api/search.rs` pass without modification
- [ ] Add a unit test in `modules/search/src/service/mod.rs` verifying that the full-text search query builder produces correct SQL for single-word and multi-word queries
- [ ] Verify via integration test that search returns results for known entities in the test database

## Dependencies
- Depends on: Task 1 — Add Database Indexes for Search Performance
