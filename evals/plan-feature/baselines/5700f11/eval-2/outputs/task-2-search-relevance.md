## Repository
trustify-backend

## Description
Optimize the SearchService for performance and relevance-ranked results. Replace or augment the current full-text search implementation in the search module to use the GIN-indexed tsvector columns created in Task 1. Introduce relevance scoring so that results are ordered by match quality rather than insertion order. Add a relevance score field to the search response so API consumers can display or use the ranking.

**ASSUMPTION -- pending clarification**: Relevance is defined as PostgreSQL `ts_rank` scoring against the tsvector columns. This is a reasonable MVP default but needs validation with real user queries and expected result orderings from the product owner.

**ASSUMPTION -- pending clarification**: The target performance SLA is assumed to be p95 < 500ms for typical queries against the current production dataset size. No concrete latency target was provided in the requirements.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Refactor the `SearchService` to use tsvector-based queries with `ts_rank` scoring instead of (or in addition to) LIKE/ILIKE pattern matching. Optimize query construction to leverage GIN indexes.
- `modules/search/src/endpoints/mod.rs` -- Update the `GET /api/v2/search` handler to include relevance score in the response and support a `sort` parameter that allows sorting by relevance (default) or other fields.
- `modules/search/Cargo.toml` -- Add any additional dependencies if needed for query building

## API Changes
- `GET /api/v2/search` -- MODIFY: Response items now include a `relevance_score` field (f32). Default sort order changes from unspecified to relevance descending. Add optional `sort` query parameter accepting `relevance` (default) or `date`.

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Modify this to build queries using `to_tsquery()` against the tsvector columns and rank results with `ts_rank()`.
- Use the query builder helpers in `common/src/db/query.rs` for pagination and sorting. The existing filtering and pagination infrastructure should be reused rather than reimplemented.
- Response wrapping should continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs` to maintain backward compatibility with existing API consumers.
- Error handling must follow the existing pattern: return `Result<T, AppError>` and use `.context()` wrapping as established throughout the codebase (see `common/src/error.rs` for the `AppError` enum).
- Ensure backward compatibility: existing response fields must be preserved. The `relevance_score` field is additive.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting. Extend or reuse these for relevance-based sorting.
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper for list responses. Continue using this for search results.
- `common/src/error.rs` -- `AppError` enum and `IntoResponse` implementation for consistent error handling.

## Acceptance Criteria
- [ ] Search queries use tsvector/GIN indexes (verified via EXPLAIN ANALYZE showing index scan, not seq scan)
- [ ] Search results include a `relevance_score` field in each result item
- [ ] Results are sorted by relevance score descending by default
- [ ] Optional `sort` query parameter allows sorting by `relevance` or `date`
- [ ] Existing response fields are preserved (backward compatible)
- [ ] Search response times are measurably improved compared to baseline

## Test Requirements
- [ ] Unit/integration test verifying that search results are ordered by relevance (a query matching a title exactly ranks higher than a partial match)
- [ ] Integration test verifying the `sort` parameter switches between relevance and date ordering
- [ ] Integration test verifying that the `relevance_score` field is present in response items
- [ ] Integration test verifying backward compatibility: existing search response fields are still present

## Dependencies
- Depends on: Task 1 -- Add database migration for full-text search indexes
