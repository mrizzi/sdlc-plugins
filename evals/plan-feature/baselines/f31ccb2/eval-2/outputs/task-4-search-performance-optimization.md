## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance to address user complaints about slow search. This task adds query-level optimizations including result limiting before ranking, connection pool tuning for search queries, and HTTP-level caching for search responses. These changes target the "search should be faster" MVP requirement.

## Files to Modify
- `modules/search/src/service/mod.rs` — add query execution optimizations: LIMIT pushdown before ranking, configurable result window, and query timeout
- `modules/search/src/endpoints/mod.rs` — add tower-http cache-control headers for search responses and configure response caching
- `common/src/db/limiter.rs` — review and tune connection pool limits for search query workloads if needed

## Implementation Notes
- **Query optimization:** In the SearchService, apply a two-phase approach: first filter candidates using the GIN index (fast index scan), then rank only the filtered candidates with `ts_rank`. Avoid ranking the entire table by using a subquery or CTE with LIMIT to cap the candidate set before ranking
- **Result window:** Add a configurable maximum result window (e.g., 1000 results) to prevent unbounded queries. This works with the existing pagination from `common/src/db/query.rs` — the window caps the total searchable set, while pagination slices within that window
- **Query timeout:** Add a PostgreSQL `statement_timeout` setting on search queries to prevent long-running queries from blocking connections. Use `SET LOCAL statement_timeout = '5s'` within the transaction
- **HTTP caching:** Configure `tower-http` `CacheControl` on the search endpoint route builder. Use short TTLs (e.g., 30 seconds) with `must-revalidate` to balance freshness with performance. Follow the caching pattern documented in the project's Key Conventions
- **Connection pool:** Review `common/src/db/limiter.rs` to ensure search queries don't monopolize the pool. Consider a separate pool or priority queue for search vs. other operations if the limiter supports it
- Follow the error handling pattern from `common/src/error.rs` — timeouts should map to a 504 Gateway Timeout or 408 Request Timeout via `AppError`

## Reuse Candidates
- `common/src/db/query.rs` — pagination helpers that already implement LIMIT/OFFSET; extend with result window capping
- `common/src/db/limiter.rs` — existing connection pool limiter; review for search-specific tuning
- `common/src/error.rs` — `AppError` enum for mapping timeout errors to HTTP status codes

## Acceptance Criteria
- [ ] Search queries use index-only filtering before applying expensive ranking
- [ ] A configurable maximum result window caps the number of candidates ranked
- [ ] Search queries have a statement timeout to prevent runaway queries
- [ ] Search responses include appropriate Cache-Control headers
- [ ] Query timeouts are handled gracefully and return an appropriate HTTP error

## Test Requirements
- [ ] Test that search queries complete within acceptable time bounds (e.g., < 500ms for typical queries against test dataset)
- [ ] Test that result window capping works correctly (total results never exceed the configured maximum)
- [ ] Test that query timeout triggers an appropriate error response rather than hanging
- [ ] Test that Cache-Control headers are present on search responses

## Verification Commands
- `curl -w "%{time_total}" -s "http://localhost:8080/api/v2/search?q=test" -o /dev/null` — response time should be under 500ms
- `curl -sI "http://localhost:8080/api/v2/search?q=test" | grep -i cache-control` — should show cache-control header

## Dependencies
- Depends on: Task 2 — Refactor SearchService for relevance ranking (performance optimizations build on the refactored search pipeline)
