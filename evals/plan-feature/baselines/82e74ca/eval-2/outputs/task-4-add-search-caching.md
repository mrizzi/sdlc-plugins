# Task 4 — Add Response Caching to Search Endpoint

## Repository
trustify-backend

## Description
Add HTTP-level response caching to the search endpoint to reduce database load for repeated queries and improve response times. This addresses the "search should be faster" requirement by avoiding redundant database round-trips for identical search queries within a short time window.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add `tower-http` caching middleware configuration to the search route builder, with appropriate cache duration and cache-control headers

## Implementation Notes
- The project already uses `tower-http` caching middleware as noted in the repository conventions. Inspect `server/src/main.rs` and existing endpoint route builders to find how caching is currently configured for other endpoints, then follow the same pattern for the search endpoint.
- Set a short cache TTL (e.g., 30-60 seconds) since search results may change as new SBOMs and advisories are ingested. The cache duration should balance freshness against performance.
- Use `Cache-Control` headers with `max-age` and `must-revalidate` directives.
- Ensure cache keys incorporate all query parameters (search term, filters, pagination) so different queries are cached separately.
- Consider adding `Vary` headers for any request headers that affect the response.
- Per constraints doc 5.2: inspect existing caching configuration in the codebase before implementing.
- Per constraints doc 5.4: reuse the existing `tower-http` caching setup rather than introducing a new caching mechanism.

## Reuse Candidates
- `server/src/main.rs` — Axum server setup where existing caching middleware is configured; follow its pattern
- `modules/search/src/endpoints/mod.rs` — existing route registration to extend with caching layer

## Acceptance Criteria
- [ ] Search endpoint responses include `Cache-Control` headers with appropriate `max-age`
- [ ] Identical search queries within the cache TTL return cached responses without hitting the database
- [ ] Different query parameters (search term, filters, page) produce separate cache entries
- [ ] Cache is invalidated after TTL expiry
- [ ] No regression in correctness — cached responses match non-cached responses

## Test Requirements
- [ ] Test that `Cache-Control` headers are present in search endpoint responses
- [ ] Test that repeated identical requests within TTL are served from cache (verify via response headers or timing)
- [ ] Test that different query parameters are cached independently

## Dependencies
- Depends on: Task 3 — Add Search Filter Parameters (caching must account for filter parameters in cache keys)
