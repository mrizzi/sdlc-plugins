# Task 4: Add search response caching and query optimization

## Repository

trustify-backend

## Target Branch

`main`

## Description

Improve search performance by adding HTTP-level response caching with tower-http and optimizing the search query execution path. This includes configuring cache-control headers for search responses, adding connection-level statement caching, and providing EXPLAIN ANALYZE guidance for ongoing query tuning.

## Files to Modify

- `modules/search/src/endpoints/mod.rs` -- Add caching behavior to the search endpoint:
  - Apply `tower_http::set_header::SetResponseHeaderLayer` or equivalent to set `Cache-Control` headers on search responses
  - Use `Cache-Control: public, max-age=30` for search results (short TTL since data changes frequently)
  - Add `Vary: Accept, Authorization` headers so caches differentiate by user context
  - Add an `ETag` based on a hash of the query parameters and a data-version timestamp, enabling conditional requests (304 Not Modified)

- `modules/search/src/service/mod.rs` -- Optimize query execution:
  - Use `LIMIT` push-down: apply pagination limits at the database level rather than fetching all results and truncating in Rust
  - For multi-table searches (SBOM + advisory + package), use `UNION ALL` with per-table `LIMIT` instead of separate queries followed by merge-sort, reducing round trips
  - Add `SET LOCAL statement_timeout = '5s'` guard for search queries to prevent runaway queries from holding connections
  - Precompute the `tsquery` once and reuse across all table searches within a single request

## Reuse Candidates

- `server/src/main.rs` -- Check how tower-http middleware is currently configured for other routes. The caching middleware pattern used there should be replicated for the search endpoint. Look for `tower_http::set_header`, `tower_http::compression`, or custom middleware layers.
- `common/src/db/query.rs` -- The existing pagination helpers should already push `LIMIT`/`OFFSET` to the database. Verify this is the case; if not, fix it here.

## Implementation Notes

- The tower-http caching approach should be a middleware layer applied specifically to the search route, not globally. In Axum, this is done by wrapping the search router with `.layer(SetResponseHeaderLayer::overriding(...))` before merging it into the main router.
- For the ETag implementation, hash the canonical query string (sorted parameters) combined with a data-freshness timestamp. The data-freshness timestamp can be a simple `SELECT MAX(updated_at) FROM ...` query that is itself cached in-memory with a short TTL (e.g., 5 seconds).
- The `UNION ALL` optimization is particularly important for unfiltered searches that hit all three entity tables. Profile the current approach (separate queries) vs. `UNION ALL` and choose based on actual performance. The `UNION ALL` approach may require a common projection across entity types.
- Add SQL comments (e.g., `/* search:sbom */`) to generated queries to make them identifiable in PostgreSQL's `pg_stat_statements` for monitoring.
- Document the EXPLAIN ANALYZE process in code comments so future developers can profile search queries:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT ... FROM sbom WHERE search_vector @@ plainto_tsquery('english', 'openssl')
  ORDER BY ts_rank(search_vector, plainto_tsquery('english', 'openssl')) DESC
  LIMIT 20;
  ```
- Consider adding a `X-Search-Timing` response header (debug builds only) that reports query execution time in milliseconds for performance monitoring.

## Acceptance Criteria

- [ ] Search responses include appropriate `Cache-Control` headers
- [ ] Search responses include `Vary` headers for correct cache partitioning
- [ ] Repeated identical searches within the cache TTL return faster (measurable via response timing)
- [ ] Pagination limits are pushed to the database (no over-fetching)
- [ ] Search queries have a statement timeout guard preventing runaway execution
- [ ] The tsquery is computed once per request, not once per table
- [ ] No functional regression: all existing search behavior is preserved

## Test Requirements

- Integration test: verify `Cache-Control` header is present and has expected directives
- Integration test: verify `Vary` header is present
- Integration test: verify search results are correct after caching layer is added (no stale/wrong data)
- Performance test: measure search latency before and after optimization on a dataset with at least 1000 entities. Document the baseline and improved times in the PR description.
- Integration test: verify statement timeout prevents queries exceeding 5 seconds from blocking

## Verification Commands

```bash
# Check cache headers
curl -v "http://localhost:8080/api/v2/search?q=openssl" 2>&1 | grep -i cache-control
curl -v "http://localhost:8080/api/v2/search?q=openssl" 2>&1 | grep -i vary

# Profile a search query
psql -d trustify -c "EXPLAIN (ANALYZE, BUFFERS) SELECT *, ts_rank(search_vector, plainto_tsquery('english', 'openssl')) AS rank FROM sbom WHERE search_vector @@ plainto_tsquery('english', 'openssl') ORDER BY rank DESC LIMIT 20;"

# Check pg_stat_statements for search queries
psql -d trustify -c "SELECT query, calls, mean_exec_time, rows FROM pg_stat_statements WHERE query LIKE '%search%' ORDER BY mean_exec_time DESC LIMIT 10;"
```

## Dependencies

- Task 1 (search indexes) must be completed -- GIN indexes are essential for query performance
- Tasks 2 and 3 are not strict dependencies but should ideally be completed first so the caching and optimization work covers the final query shape
