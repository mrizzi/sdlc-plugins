## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` to use PostgreSQL full-text search with `tsvector`/`tsquery` for relevance-ranked results instead of basic pattern matching. This replaces the current search implementation (which users report as returning irrelevant results) with a proper full-text search approach that ranks results by relevance using `ts_rank`.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace existing search query logic with tsvector/tsquery full-text search using ts_rank for relevance ordering
- `modules/search/src/lib.rs` — update module exports if new types are introduced

## Files to Create
- `modules/search/src/model/mod.rs` — define SearchResult model with relevance score field and SearchQuery input struct

## API Changes
- `GET /api/v2/search` — MODIFY: response now includes a `relevance_score` field (f64) on each result item, and results are ordered by relevance score descending by default

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` handles full-text search across entities — refactor it to use `to_tsquery` or `plainto_tsquery` for the user's search term and `ts_rank` against the `search_vector` column added by Task 1's migration
- Use `plainto_tsquery` for simpler user input (space-separated words become AND terms) and `websearch_to_tsquery` if advanced operators are desired
- Order results by `ts_rank(search_vector, query)` descending so the most relevant results appear first
- Follow the existing service pattern from `modules/fundamental/src/sbom/service/sbom.rs` — methods return `Result<T, AppError>` using `.context()` for error wrapping
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response wrapper
- Reference `common/src/db/query.rs` for existing query builder patterns (pagination, sorting) — extend rather than duplicate the pagination logic
- Consider adding a minimum relevance threshold to filter out very low-scoring matches

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend these for relevance-based ordering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; use this for search results
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of the service pattern (fetch, list operations)

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsvector/tsquery) instead of basic pattern matching
- [ ] Results are ranked by relevance score using ts_rank
- [ ] Results include a `relevance_score` field in the response
- [ ] Empty or whitespace-only search terms return an appropriate error or empty result set
- [ ] Search across all entity types (sbom, advisory, package) returns unified, ranked results

## Test Requirements
- [ ] Test that searching for an exact name match returns it as the top result
- [ ] Test that partial word matches return relevant results
- [ ] Test that results are ordered by relevance (more relevant matches first)
- [ ] Test that searching for a term present in multiple entity types returns results from all types
- [ ] Test edge cases: empty query, special characters, very long queries

## Dependencies
- Depends on: Task 1 — Add full-text search migration (requires tsvector columns and GIN indexes)
