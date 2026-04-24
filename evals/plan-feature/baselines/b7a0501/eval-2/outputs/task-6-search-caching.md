# Task 6 — Add Caching for Search Results

## Repository
trustify-backend

## Description
Configure response caching for the search endpoint using the existing `tower-http` caching middleware to reduce database load for repeated or popular search queries. This addresses the performance requirement ("search should be faster") by avoiding redundant query execution for identical requests within a short time window.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add cache-control headers or caching middleware layer to the search route builder, following the existing caching configuration pattern used by other endpoints
- `server/src/main.rs` — Ensure the search module routes include the caching middleware layer (if caching is applied at the route-mounting level)

## Implementation Notes
- The project already uses `tower-http` caching middleware — inspect `server/src/main.rs` and existing endpoint route builders (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`) to see how caching is currently configured for other endpoints
- Apply a short TTL cache (e.g., 30-60 seconds) appropriate for search results that may change as new data is ingested
- Use `Cache-Control` headers to control caching behavior — set `max-age` and consider `stale-while-revalidate` for improved perceived performance
- Ensure that different filter combinations produce different cache keys (the query string should be part of the cache key by default with HTTP caching)
- Consider adding `Vary` header if needed to ensure filter parameters are included in cache discrimination
- Per constraints doc section 5.2: inspect the existing caching configuration before adding new caching logic

## Reuse Candidates
- `server/src/main.rs` — Existing `tower-http` caching middleware setup
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for how caching is applied to existing endpoint route builders

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate `Cache-Control` headers
- [ ] Repeated identical search requests within the cache TTL are served from cache
- [ ] Different search queries and filter combinations are cached independently
- [ ] Cache TTL is reasonable for search results (30-60 seconds)
- [ ] Caching does not interfere with pagination (different pages are cached separately)

## Test Requirements
- [ ] Integration test: verify `Cache-Control` header is present on search responses
- [ ] Integration test: verify that search responses are consistent when served from cache

## Dependencies
- Depends on: Task 5 — Add Filter Parameters to Search Endpoint
