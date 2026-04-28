# Task 2 — Implement Ranked Full-Text Search in SearchService

## Repository
trustify-backend

## Description
Replace the existing naive text search implementation in `SearchService` with
PostgreSQL full-text search using `ts_query` and `ts_rank`. This addresses the
TC-9002 requirements for both faster search ("Search should be faster") and
more relevant results ("Results should be more relevant").

The updated service should parse user query strings into `tsquery` format,
execute full-text searches against the GIN-indexed `tsvector` columns added
in Task 1, and rank results by relevance score.

## Files to Modify
- `modules/search/src/service/mod.rs` — rewrite search logic to use PostgreSQL
  full-text search with `ts_vector`/`ts_rank` instead of naive text matching
- `modules/search/src/lib.rs` — update module exports if new types are added

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` currently
  performs full-text search across entities. Replace the query mechanism with
  PostgreSQL `to_tsquery()` and `ts_rank()` functions.
- Use `plainto_tsquery('english', user_input)` for basic query parsing (handles
  natural language input). Consider `websearch_to_tsquery` for more advanced
  query syntax support (AND, OR, NOT, phrases).
- Order results by `ts_rank(search_vector, query)` descending to surface the
  most relevant results first.
- Include the relevance score in the response so clients can use it for display
  or further filtering.
- Follow the existing service pattern established in
  `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for error
  handling with `Result<T, AppError>` and `.context()` wrapping.
- Use the shared query helpers in `common/src/db/query.rs` for pagination
  and sorting. The search results should continue to be wrapped in
  `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Per constraints.md §5.2: inspect the current SearchService implementation
  before modifying it.
- Per constraints.md §5.4: reuse existing query builder helpers in
  `common/src/db/query.rs` rather than duplicating pagination/sorting logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering,
  pagination, and sorting; reuse for paginating search results
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper;
  use for search result responses
- `common/src/error.rs` — `AppError` enum; use for error handling in the
  updated search service
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a
  reference pattern for service structure, error handling, and database queries
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService`
  for the `search` method pattern (already has a search operation)

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`to_tsquery` / `ts_rank`)
- [ ] Results are ranked by relevance score (most relevant first)
- [ ] Relevance score is included in search response metadata
- [ ] Search across SBOMs, advisories, and packages works correctly
- [ ] Empty query returns results (graceful fallback)
- [ ] Special characters in query input are handled safely (no SQL injection)
- [ ] Response time is measurably improved compared to naive text matching

## Test Requirements
- [ ] Test that search returns results ranked by relevance (exact match ranks higher than partial)
- [ ] Test that multi-word queries return results matching more terms first
- [ ] Test that empty query input returns results without error
- [ ] Test that special characters in query do not cause errors
- [ ] Test search across multiple entity types returns mixed results ranked by relevance

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Migration
