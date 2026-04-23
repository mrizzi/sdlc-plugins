## Repository
trustify-backend

## Description
Rewrite the search service to use PostgreSQL full-text search with `ts_rank` scoring instead of basic LIKE/ILIKE queries. This addresses the "results should be more relevant" requirement by ranking results based on text match quality. Results across entity types (SBOMs, advisories, packages) are scored and interleaved by relevance.

**Assumption pending clarification**: The feature description does not define what "relevant" means. We assume relevance is determined by PostgreSQL `ts_rank` scoring on full-text search vectors, with advisory severity used as a secondary ranking signal. We assume all three entity types are searched in a single query and results are returned in a unified, ranked list.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace the current search implementation in `SearchService` with full-text search queries using `to_tsquery()` and `ts_rank()`. The service currently does "full-text search across entities" but presumably uses basic pattern matching. Rewrite to query the `tsvector` columns created in Task 1, compute `ts_rank` scores, and sort results by rank descending.
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint handler to pass through ranking parameters and return results with a `score` or `relevance` field in the response body.
- `common/src/db/query.rs` — Add a shared helper for building `ts_rank` ORDER BY clauses, following the existing pattern of shared query builder helpers for filtering, pagination, and sorting. This allows other modules to adopt full-text ranking in the future.

## API Changes
- `GET /api/v2/search` — MODIFY: Response now includes a `relevance_score` field per result. Results are ordered by relevance score descending by default. Existing fields are preserved for backward compatibility.

## Implementation Notes
- In `modules/search/src/service/mod.rs`, the current `SearchService` likely builds queries using SeaORM's query builder. Replace the WHERE clause with `search_vector @@ to_tsquery('english', ?)` and add `ts_rank(search_vector, to_tsquery('english', ?))` as a select expression and ORDER BY clause.
- Use `common/src/db/query.rs` as the location for shared ranking logic. The existing file already contains shared query builder helpers for filtering, pagination, and sorting — a ranking helper fits naturally here.
- For advisory results, apply a secondary sort using the severity field from `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) to boost higher-severity advisories when relevance scores are equal.
- Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs` as all list endpoints do.
- Error handling must follow the `Result<T, AppError>` pattern using `.context()` wrapping from `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs::*` — Existing query builder helpers for pagination and sorting can be extended for ranking
- `common/src/model/paginated.rs::PaginatedResults` — Standard response wrapper for list results
- `common/src/error.rs::AppError` — Standard error type for handler responses

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of LIKE/ILIKE
- [ ] Results include a `relevance_score` field
- [ ] Results are sorted by relevance score descending by default
- [ ] Advisory results use severity as a secondary ranking signal
- [ ] Existing search response fields are preserved (backward compatible)
- [ ] Empty search queries return a meaningful response (not an error)

## Test Requirements
- [ ] Unit test: searching for a known term returns results with non-zero relevance scores
- [ ] Unit test: results are ordered by relevance score descending
- [ ] Unit test: a search matching multiple entity types returns interleaved results sorted by score
- [ ] Unit test: advisory severity acts as a tiebreaker for equal relevance scores
- [ ] Unit test: empty or whitespace-only search queries are handled gracefully
- [ ] Unit test: special characters in search queries do not cause SQL injection or query errors

## Dependencies
- Depends on: Task 1 — Add database migration for full-text search indexes
