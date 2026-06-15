## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query execution and add response caching to reduce search latency. The feature requirement states search is "currently too slow" and should be "fast enough," but provides no quantitative targets. This task addresses performance through query optimization (ensuring the full-text search queries from Task 2 use efficient execution plans) and by adding HTTP-level caching for search responses using the existing `tower-http` caching middleware.

**Assumptions pending clarification:**
- No specific latency target (e.g., p95 < 500ms) was provided. This task assumes the goal is measurable improvement over the current baseline, validated by comparing `EXPLAIN ANALYZE` output before and after optimization.
- Cache TTL for search results is assumed to be short-lived (e.g., 30 seconds) to balance freshness with performance. No caching requirements were specified in the feature description.
- No concurrent load targets or throughput requirements were provided. This task does not address horizontal scaling or connection pool tuning beyond what already exists in `common/src/db/limiter.rs`.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize search queries: add result count limits, ensure proper use of indexed columns, avoid unnecessary joins
- `modules/search/src/endpoints/mod.rs` — Add `tower-http` cache-control headers to search responses for HTTP-level caching
- `common/src/db/query.rs` — Add or refine query helper for limiting full-text search result set size before pagination

## Implementation Notes
- The project already uses `tower-http` caching middleware as noted in the Key Conventions. Add `Cache-Control` headers to the search endpoint responses in `modules/search/src/endpoints/mod.rs`, following the existing cache configuration pattern used by other endpoint route builders.
- In `modules/search/src/service/mod.rs`, ensure search queries:
  - Use the GIN index on `tsvector` columns (verify with `EXPLAIN ANALYZE`)
  - Limit the result set early in the query (use a CTE or subquery with `LIMIT` before joining related data)
  - Avoid `SELECT *` — select only the fields needed for `SearchResult` / summary structs
- Leverage the connection pool limiter in `common/src/db/limiter.rs` to prevent search queries from exhausting the connection pool under load.
- In `common/src/db/query.rs`, consider adding a helper for "top-N by rank" queries that limits the full-text search result set before applying pagination, preventing expensive ranking of the entire table.
- All changes must return `Result<T, AppError>` per `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/limiter.rs` — Connection pool limiter already in place; ensure search queries respect it
- `common/src/db/query.rs` — Existing pagination and sorting helpers to extend with rank-limited query support
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for how other endpoints configure `tower-http` cache headers in route builders

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate `Cache-Control` headers
- [ ] Search queries use index scans on `tsvector` GIN indexes (verifiable via `EXPLAIN ANALYZE`)
- [ ] Search queries limit the ranking computation to a bounded result set (not ranking the entire table)
- [ ] No regression in search result correctness — same queries return the same results (order may change within equal-rank results)
- [ ] Existing integration tests continue to pass

## Test Requirements
- [ ] Integration test: search response headers include `Cache-Control` with expected directives
- [ ] Integration test: repeated identical search queries return consistent results (cache does not cause stale or inconsistent data within TTL)
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — search integration tests pass

[sdlc-workflow] Description digest: sha256-md:56774af638d78159b7c0b5722c859dc928d1d1658a3f82d8d79fd3796d01b869
