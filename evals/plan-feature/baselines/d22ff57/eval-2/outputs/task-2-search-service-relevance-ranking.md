# Task 2 — Refactor SearchService to use full-text search with relevance ranking

## Repository
trustify-backend

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to leverage the
PostgreSQL full-text search indexes created in Task 1. Replace the current search
implementation with `tsquery`-based queries and `ts_rank` relevance scoring so that
searches execute against GIN indexes (making search faster) and results are ordered
by relevance score (making results more useful). This task addresses two of the three
MVP requirements: performance and relevance.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to:
  - Convert user search input into a PostgreSQL `tsquery` using `plainto_tsquery('english', $1)`
  - Query entity tables using the `@@` operator against the `search_vector` column
  - Compute relevance scores using `ts_rank(search_vector, query)`
  - Order results by descending relevance score
  - Search across `sbom`, `advisory`, and `package` tables and merge results
- `modules/search/src/lib.rs` — Update module exports if new types or re-exports are introduced

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs`
  to understand how it currently constructs queries and returns results. Preserve any
  existing patterns that are still applicable (error handling, pagination).
- Use `plainto_tsquery('english', $1)` for parsing user search input — it handles multi-word
  queries naturally by AND-ing terms. For more advanced use cases, `websearch_to_tsquery`
  supports quoted phrases and `-` exclusions, but `plainto_tsquery` is sufficient for MVP.
- Use `ts_rank(search_vector, query)` to compute relevance scores. Select this as an
  additional column and order results by it descending.
- The search must query across multiple entity tables (`sbom`, `advisory`, `package`).
  Follow whichever cross-table query pattern the existing `SearchService` uses — either
  `UNION ALL` with a type discriminator column, or parallel queries merged in Rust.
- Reuse `PaginatedResults<T>` from `common/src/model/paginated.rs` for response wrapping.
- Reuse query builder helpers from `common/src/db/query.rs` for pagination and sorting.
  Extend these helpers if needed for full-text search query construction rather than
  building separate query infrastructure.
- Handle edge cases: empty search input should return an empty result set or a 400 error
  (follow existing endpoint conventions). Queries with no matches should return an empty
  `PaginatedResults` with total count 0.
- Error handling must follow the existing `AppError` pattern from `common/src/error.rs`
  with `.context()` wrapping on all fallible operations.
- Per constraints §5.4: do not duplicate existing query helper functionality.
- Per constraints §5.1: keep changes scoped to the search module files.
- Per constraints §5.2: inspect existing code before modifying it.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination,
  and sorting. Extend these for full-text search query construction.
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper. Reuse for
  search result pagination.
- `common/src/error.rs` — `AppError` enum with `IntoResponse` impl. Use `.context()`
  wrapping per established patterns.
- `modules/search/src/service/mod.rs` — Current SearchService implementation. Preserve
  working patterns while refactoring query construction.

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL `tsquery`/`tsvector` operators for search queries
- [ ] Search results are ranked by relevance using `ts_rank`
- [ ] Multi-word search queries are handled correctly (AND semantics by default)
- [ ] Results include a relevance score
- [ ] Search queries use the GIN indexes (no sequential scans on indexed columns)
- [ ] Empty or whitespace-only search input is handled gracefully
- [ ] Error handling follows existing `AppError` patterns with `.context()` wrapping

## Test Requirements
- [ ] Test: search with a single keyword returns matching entities ranked by relevance
- [ ] Test: search with multiple keywords returns entities matching all terms
- [ ] Test: search with no results returns empty `PaginatedResults` with total 0
- [ ] Test: entity with search term in title ranks higher than entity with term only in description
- [ ] Test: empty or whitespace-only query returns appropriate response

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
