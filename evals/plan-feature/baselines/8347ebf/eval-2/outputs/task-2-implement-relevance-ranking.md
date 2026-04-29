# Task 2 — Implement Relevance-Based Search Ranking in SearchService

## Repository
trustify-backend

## Description
Refactor the `SearchService` in the search module to use PostgreSQL full-text search with relevance ranking instead of simple pattern matching. Search results should be ordered by a relevance score computed via `ts_rank` against the `tsvector` indexes created in Task 1. The relevance score should also be included in the search response so consumers can display or use it.

This directly addresses the user complaint that "search doesn't return useful results" by ensuring results are ranked by how well they match the query, with configurable field weighting (e.g., exact title matches rank higher than description matches).

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `to_tsquery` / `plainto_tsquery` against the `tsvector` columns, order results by `ts_rank`, and return relevance scores
- `modules/search/src/endpoints/mod.rs` — update the search endpoint response to include a relevance score field alongside each result
- `common/src/model/paginated.rs` — evaluate whether `PaginatedResults<T>` needs a generic score/metadata field, or if a search-specific response wrapper is more appropriate

## API Changes
- `GET /api/v2/search` — MODIFY: response items now include a `relevance_score` field (f64); results are ordered by relevance score descending by default

## Implementation Notes
- Use PostgreSQL's `plainto_tsquery('english', <user_query>)` for user-friendly query parsing (handles spaces, no need for special syntax). Consider also supporting `to_tsquery` for advanced users via an optional `query_mode` parameter.
- Apply `ts_rank(tsvector_column, query)` for relevance scoring. Use field weights set in the migration (Task 1) to ensure title matches outrank description matches.
- The existing `SearchService` in `modules/search/src/service/mod.rs` handles full-text search across entities. Modify the existing query logic rather than creating a parallel implementation.
- Follow the error handling pattern established in the codebase: all handlers return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`).
- For the response type, prefer creating a `SearchResult<T>` wrapper that includes `item: T` and `relevance_score: f64` rather than modifying `PaginatedResults<T>`, to keep the shared pagination type clean.
- Per constraints doc section 5 (Code Change Rules): inspect existing code before modifying, follow patterns in Implementation Notes, do not duplicate existing functionality.

## Reuse Candidates
- `modules/search/src/service/mod.rs` — existing `SearchService` implementation; extend rather than replace
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; reuse pagination and sorting helpers
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; use as reference for the search result wrapper pattern
- `common/src/error.rs` — `AppError` enum and `IntoResponse` impl; follow the same error handling pattern

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsquery` against `tsvector` columns) instead of `LIKE`/`ILIKE`
- [ ] Results are ordered by relevance score (highest first) by default
- [ ] Each search result item includes a `relevance_score` field in the API response
- [ ] Multi-word queries return relevant results (e.g., searching "critical vulnerability" matches advisories with both words)
- [ ] Empty or whitespace-only queries return an appropriate error or empty result set

## Test Requirements
- [ ] Integration test: search for a known term returns matching results ordered by relevance
- [ ] Integration test: multi-word query returns results containing all terms ranked higher than partial matches
- [ ] Integration test: search response includes `relevance_score` field with non-zero values for matching results
- [ ] Integration test: empty query returns 400 or empty result set (not a server error)

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Indexes via Database Migration
