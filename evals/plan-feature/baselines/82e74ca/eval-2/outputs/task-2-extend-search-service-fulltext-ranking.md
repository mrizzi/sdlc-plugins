# Task 2 — Extend SearchService with Full-Text Ranking

## Repository
trustify-backend

## Description
Enhance the `SearchService` to use PostgreSQL full-text search with weighted ranking instead of simple pattern matching. This will make search results more relevant by scoring matches based on field importance (title/name fields weighted higher than description fields) using `ts_rank`.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace or augment the existing search logic in `SearchService` to use `ts_rank` on `tsvector` columns for weighted full-text search
- `common/src/db/query.rs` — add a full-text search query builder helper that constructs `tsquery` from user input and applies `ts_rank` ordering

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides full-text search across entities. Inspect the current implementation to understand the query structure before modifying.
- Use the shared query builder pattern from `common/src/db/query.rs` (filtering, pagination, sorting) as the foundation for the full-text search helper. The new helper should compose with the existing `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs`.
- Construct `tsquery` from user search input using `plainto_tsquery` or `websearch_to_tsquery` for robust handling of user input (spaces, special characters).
- Apply `ts_rank` with weight arrays: weight A (1.0) for title/name fields, weight B (0.4) for description fields.
- Return relevance scores alongside results so the API can expose them.
- Ensure backward compatibility: if no search query is provided, fall back to the existing list behavior.
- Per constraints doc 5.4: do not duplicate existing query builder logic — extend `common/src/db/query.rs`.
- Per constraints doc 5.2: inspect existing code before modifying.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting) to extend with full-text search support
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to reuse for search results
- `modules/search/src/service/mod.rs` — existing `SearchService` implementation to build upon

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL `ts_rank` for result ordering when a search query is provided
- [ ] Results are ordered by relevance score (highest first)
- [ ] Title/name matches are ranked higher than description matches
- [ ] Empty or absent search queries fall back to existing behavior (no regression)
- [ ] Relevance scores are available in the search results

## Test Requirements
- [ ] Test that search results are ordered by relevance (exact title match ranks above partial description match)
- [ ] Test that empty search query returns all results (backward compatibility)
- [ ] Test that special characters in search input are handled safely (no SQL injection, no query errors)
- [ ] Test that relevance scores are non-negative and properly ordered

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Migration (tsvector columns and GIN indexes must exist)
