# Task 2 — Enhance SearchService with Relevance-Based Ranking

## Repository
trustify-backend

## Description
Update the SearchService to use PostgreSQL full-text search ranking functions (`ts_rank` or `ts_rank_cd`) so that search results are ordered by relevance score rather than by insertion order or alphabetically. This addresses the "results should be more relevant" requirement by ensuring that results matching more search terms, or matching them in more important fields, appear first. The search query should use the `tsvector` columns and GIN indexes created in Task 1.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use `to_tsquery`/`plainto_tsquery` for query parsing and `ts_rank`/`ts_rank_cd` for result ordering
- `common/src/db/query.rs` — extend shared query builder helpers with a full-text search ranking method that can be reused across modules

## API Changes
- `GET /api/v2/search` — MODIFY: results are now ordered by relevance score (descending) by default; response includes a `relevance_score` field per result

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor it to use PostgreSQL's `to_tsquery()` for parsing the search term and `ts_rank()` or `ts_rank_cd()` for computing relevance scores against the `tsvector` columns added by Task 1.
- Add a relevance score field to the search result model so consumers can see how well each result matched.
- Use `plainto_tsquery` for simple user queries (space-separated words treated as AND) and reserve `to_tsquery` for advanced query syntax if needed in the future.
- Order results by `ts_rank` descending by default. Preserve the option to sort by other fields if the caller specifies explicit sort parameters.
- Extend `common/src/db/query.rs` with a reusable helper method for applying full-text search ranking to a SeaORM `Select` query, so that individual entity modules can also benefit from ranked search in their list endpoints.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping (as documented in the repository conventions).
- Per `docs/constraints.md` section 2 (Commit Rules): commit must reference TC-9002 and follow Conventional Commits.
- Per `docs/constraints.md` section 5.4: reuse existing query helpers in `common/src/db/query.rs` rather than duplicating query logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; extend rather than duplicate for full-text search ranking
- `common/src/model/paginated.rs` — PaginatedResults wrapper; search results should continue to use this for pagination
- `common/src/error.rs` — AppError enum for error handling pattern

## Acceptance Criteria
- [ ] Search queries use PostgreSQL `ts_rank` for relevance scoring
- [ ] Search results are ordered by relevance score (descending) by default
- [ ] Each search result includes a `relevance_score` field
- [ ] Search still returns correct results for exact-match queries
- [ ] Pagination continues to work correctly with relevance-ordered results
- [ ] A reusable full-text search ranking helper is available in `common/src/db/query.rs`

## Test Requirements
- [ ] Integration test: search for a term that appears in multiple entities, verify results are ordered by relevance
- [ ] Integration test: search for an exact title match, verify it appears first in results
- [ ] Integration test: search with pagination, verify relevance ordering is preserved across pages
- [ ] Integration test: verify `relevance_score` field is present and non-negative in response

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Indexes via Database Migration
