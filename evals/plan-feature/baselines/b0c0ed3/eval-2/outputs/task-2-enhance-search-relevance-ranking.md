## Repository
trustify-backend

## Description
Enhance the `SearchService` to use PostgreSQL's `ts_rank` function for relevance-based ordering of search results. Currently, search results are returned without meaningful ranking. This task modifies the search service and its underlying query logic to leverage the `tsvector` columns (created in Task 1) and `ts_rank` scoring so that the most relevant results appear first.

**Ambiguity note:** The feature requirement "Results should be more relevant" does not define relevance criteria. This task assumes relevance is determined by PostgreSQL full-text search ranking (`ts_rank`) using the weighted `tsvector` columns established in Task 1. No external search engine is being introduced (assumption pending clarification).

## Files to Modify
- `modules/search/src/service/mod.rs` — modify `SearchService` to use `to_tsquery` and `ts_rank` for full-text search queries with relevance-based ordering
- `common/src/db/query.rs` — add a reusable full-text search query builder helper that constructs `to_tsquery` expressions and `ts_rank` ordering, usable across modules

## API Changes
- `GET /api/v2/search` — MODIFY: search queries now use full-text matching with relevance ranking; results are ordered by relevance score descending by default. The `q` query parameter is now parsed into a `tsquery` expression. Response remains `PaginatedResults<T>` (backward-compatible).

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Modify the query construction to:
  1. Convert the user's search query string into a PostgreSQL `tsquery` using `plainto_tsquery('english', $query)` for natural language queries or `to_tsquery` for advanced syntax
  2. Use `WHERE search_vector @@ tsquery` for matching instead of any existing `LIKE`/`ILIKE` patterns
  3. Add `ORDER BY ts_rank(search_vector, tsquery) DESC` for relevance-based ordering
- Add a reusable helper in `common/src/db/query.rs` (alongside the existing filtering, pagination, and sorting helpers) that:
  - Accepts a search query string and a `tsvector` column name
  - Returns query fragments for the `WHERE` clause (tsquery match) and `ORDER BY` clause (ts_rank)
  - Handles edge cases: empty query strings (return all results), special characters in queries (sanitize input)
- Per Key Conventions: the module follows the `model/ + service/ + endpoints/` structure. The service layer handles query logic; endpoints handle HTTP concerns.
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Ensure any new error paths (e.g., malformed query syntax) use the `AppError` enum from `common/src/error.rs`.
- Per Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. The search endpoint must continue using this wrapper.
- Preserve backward compatibility: if no `q` parameter is provided, fall back to returning all results (existing behavior).

## Reuse Candidates
- `common/src/db/query.rs` — existing shared query builder helpers for filtering, pagination, and sorting. The new full-text search helper should follow the same patterns and integrate with the existing pagination/sorting mechanisms.
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper already used by search endpoint; continue using it.
- `common/src/error.rs::AppError` — error handling enum; add a variant or use an existing variant for malformed search queries.

## Acceptance Criteria
- [ ] Search results for a given query are ordered by relevance (most relevant first)
- [ ] The `GET /api/v2/search` endpoint uses PostgreSQL full-text search matching (`@@` operator) instead of pattern matching
- [ ] A reusable full-text search helper exists in `common/src/db/query.rs`
- [ ] Empty search queries return all results (backward-compatible behavior)
- [ ] Malformed query input returns a clear error response via `AppError`, not a 500
- [ ] Existing search API contract is preserved (response format, pagination)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: search with a known term returns results containing that term, ordered by relevance
- [ ] Integration test: search with a term matching an SBOM name (weight A) ranks it above a match in a description (weight B)
- [ ] Integration test: empty search query returns paginated results (backward compatibility)
- [ ] Integration test: special characters in search query do not cause 500 errors
- [ ] Unit test for the full-text search helper in `common/src/db/query.rs`: correct tsquery generation for normal and edge-case inputs

## Dependencies
- Depends on: Task 1 — Add full-text search index migration (tsvector columns and GIN indexes must exist)
