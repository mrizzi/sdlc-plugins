# Task 2 — Optimize SearchService with PostgreSQL full-text search

**Summary:** Refactor SearchService to use tsvector/tsquery full-text search for faster, more relevant results

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL's native full-text search capabilities (tsvector/tsquery) instead of any naive pattern-matching approach (e.g., LIKE or ILIKE queries). This addresses both the "search is slow" and "results should be more relevant" requirements by leveraging PostgreSQL's built-in text search engine, which provides tokenization, stemming, stop-word removal, and relevance ranking out of the box.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor the `SearchService` full-text search method to use `to_tsquery()` against the `search_vector` columns added by Task 1's migration, with `ts_rank()` or `ts_rank_cd()` for relevance-based ordering
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` handler to pass relevance-ordered results to the response

## API Changes
- `GET /api/v2/search` — MODIFY: Results are now ordered by relevance score (descending) by default instead of arbitrary order. No breaking changes to the request or response schema.

## Implementation Notes
- Examine the current implementation in `modules/search/src/service/mod.rs` to understand the existing query pattern before making changes. The `SearchService` likely has a method that performs full-text search across entities.
- Use SeaORM's `raw_query` or `QuerySelect::column` with custom expressions to construct `to_tsquery` and `ts_rank` SQL expressions, since SeaORM does not have built-in tsvector support.
- The query should use `plainto_tsquery('english', $search_term)` for user-friendly query parsing (handles spaces and common words without requiring the user to know tsquery syntax).
- Apply `ts_rank(search_vector, query)` as the ORDER BY expression so the most relevant results appear first.
- Reference the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting patterns — ensure relevance-based ordering integrates with the existing sorting mechanism rather than replacing it.
- Reference the `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` to ensure the response format remains compatible.
- All handlers must return `Result<T, AppError>` per the error handling convention in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate the sorting mechanism.
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; search results must conform to this type.
- `common/src/error.rs` — `AppError` enum for error handling; use `.context()` wrapping pattern.
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for how other services structure their query methods.

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL `to_tsquery()` and `ts_rank()` for full-text search
- [ ] Search results are ordered by relevance score (most relevant first)
- [ ] User search terms are parsed with `plainto_tsquery` (no tsquery syntax required from users)
- [ ] Search queries hit the GIN indexes created in Task 1 (no sequential scans on large tables)
- [ ] Existing search endpoint contract (`GET /api/v2/search`) remains backward compatible
- [ ] Response uses `PaginatedResults<T>` wrapper

## Test Requirements
- [ ] Add integration test verifying that a search query returns results ordered by relevance (insert documents with varying keyword density, verify ordering)
- [ ] Add integration test verifying that search returns results matching partial terms (stemming works)
- [ ] Verify that existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — Search integration tests pass
- `EXPLAIN ANALYZE SELECT ... FROM sbom WHERE search_vector @@ to_tsquery(...)` — Confirm index scan is used (manual verification)

## Dependencies
- Depends on: Task 1 — Add database indexes for search-critical columns
