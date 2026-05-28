# Task 4 — Optimize search query performance and add caching

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search endpoint for performance to address the user complaint that "search is slow." This includes adding HTTP response caching via tower-http for search results, optimizing the SearchService query construction to minimize database round-trips, and ensuring the full-text search queries use the GIN indexes efficiently. Add a search-specific query timeout to prevent slow queries from blocking the connection pool.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize query construction to execute a single query per entity type (or a single UNION query) instead of multiple sequential queries; add query timeout
- `modules/search/src/endpoints/mod.rs` — configure tower-http caching middleware for the search endpoint with appropriate cache-control headers; add request-level timeout
- `common/src/db/limiter.rs` — review and potentially adjust connection pool limiter settings for search query concurrency

## Implementation Notes
- The project already uses `tower-http` caching middleware (per Key Conventions). Configure the search endpoint's route builder with cache-control headers: use a short TTL (e.g., 30-60 seconds) for search results since the underlying data may change with new ingestion.
- Optimize the SearchService to minimize database round-trips: instead of querying each entity table sequentially, consider using a UNION ALL query or parallel futures (tokio::join!) to query sbom, advisory, and package tables concurrently.
- Add a query-level timeout using SeaORM's `ConnectionTrait` with PostgreSQL's `SET LOCAL statement_timeout` to prevent individual search queries from running too long. A 5-second timeout is reasonable for search.
- Ensure the full-text search queries include an explicit `WHERE tsvector_column @@ to_tsquery(...)` clause so PostgreSQL's query planner uses the GIN indexes from Task 1.
- Reference `common/src/db/limiter.rs` to understand the existing connection pool limiter pattern; search queries should respect the pool limiter to avoid connection exhaustion under high search load.
- All handlers return `Result<T, AppError>` per convention — timeout errors should map to a 504 Gateway Timeout or 408 Request Timeout via the AppError enum.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing caching configuration in endpoint route builders before adding new cache configuration.

## Reuse Candidates
- `common/src/db/limiter.rs` — existing connection pool limiter; reuse for search concurrency control
- `common/src/error.rs` — AppError enum for mapping timeout errors to HTTP responses
- `modules/search/src/endpoints/mod.rs` — existing endpoint route builder where tower-http caching is already configured for other endpoints

## Acceptance Criteria
- [ ] Search endpoint responds with cache-control headers
- [ ] Repeated identical search queries are served from cache within the TTL window
- [ ] Search queries execute using the GIN indexes (verified via EXPLAIN ANALYZE)
- [ ] Search queries time out gracefully after the configured timeout
- [ ] Connection pool is not exhausted under concurrent search requests

## Test Requirements
- [ ] Integration test: search response includes appropriate cache-control headers
- [ ] Integration test: search query completes within acceptable time for a dataset with 1000+ entities
- [ ] Integration test: verify that a very slow/complex query returns a timeout error rather than hanging

## Verification Commands
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search GIN indexes via database migration
