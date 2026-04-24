# Task 2 — Refactor SearchService to use full-text search with relevance ranking

## Repository
trustify-backend

## Description
Refactor the `SearchService` in `modules/search/` to leverage the PostgreSQL full-text search
indexes created in Task 1. Replace the current search implementation with `tsquery`-based
queries and `ts_rank` relevance scoring. This addresses both MVP requirements: making search
faster (indexed queries instead of sequential scans) and making results more relevant
(ranked by relevance score).

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to:
  - Parse user search input into a PostgreSQL `tsquery` (handling multi-word queries with `&` and `|` operators)
  - Query the `search_vector` columns using `@@` operator against the `tsquery`
  - Rank results using `ts_rank(search_vector, query)` and order by descending rank
  - Search across `sbom`, `advisory`, and `package` tables and merge results
  - Return results with a relevance score field
- `modules/search/src/lib.rs` — Update module exports if new types are introduced

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text
  search across entities. Inspect the existing implementation to understand the current
  query approach before refactoring.
- Use `plainto_tsquery('english', $1)` for simple user input parsing (handles multi-word
  queries naturally). For advanced users, consider also supporting `websearch_to_tsquery`
  which handles quoted phrases and `-` exclusions.
- Use `ts_rank(search_vector, query)` to compute relevance scores. Order results by
  descending rank.
- The search must query across multiple entity tables (`sbom`, `advisory`, `package`).
  Use `UNION ALL` with a discriminator column for entity type, or execute parallel queries
  and merge in Rust — follow whichever pattern the existing `SearchService` uses.
- Reuse `PaginatedResults<T>` from `common/src/model/paginated.rs` for response wrapping.
- Reuse query builder helpers from `common/src/db/query.rs` for pagination and sorting.
- Per constraints §5.4: do not duplicate existing query helper functionality — extend
  `common/src/db/query.rs` if needed.
- Per constraints §5.1: keep changes scoped to the search module files.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination,
  and sorting. Extend these for full-text search query construction rather than building
  a separate query system.
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper. Reuse for
  search results pagination.
- `common/src/error.rs` — `AppError` enum for error handling. Use `.context()` wrapping
  per existing patterns.

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL `tsquery`/`tsvector` operators for search queries
- [ ] Search results are ranked by relevance using `ts_rank`
- [ ] Multi-word search queries are handled correctly (AND semantics by default)
- [ ] Results include a relevance score in the response
- [ ] Search queries use the GIN indexes (no sequential scans for indexed columns)
- [ ] Empty search queries return an appropriate response (empty results or error)
- [ ] Error handling follows existing `AppError` patterns with `.context()` wrapping

## Test Requirements
- [ ] Unit test: search with single keyword returns matching entities ranked by relevance
- [ ] Unit test: search with multiple keywords returns entities matching all terms
- [ ] Unit test: search with no results returns empty `PaginatedResults`
- [ ] Unit test: search relevance ordering — entity with term in title ranks higher than entity with term only in description
- [ ] Unit test: empty/whitespace-only query returns appropriate response

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
