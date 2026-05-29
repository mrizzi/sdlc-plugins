## Repository
trustify-backend

## Target Branch
main

## Description
Add a caching layer for search results to improve response times for repeated queries. This addresses TC-9002 requirement: "Search should be faster." Uses tower-http caching middleware, which is already part of the project's stack, to cache search responses with a short TTL. Cache keys incorporate the full query string (search term + filters + pagination) to ensure cached results match the request.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add tower-http cache middleware to the search route builder with appropriate TTL and cache-control headers; configure cache key to include query parameters
- `server/src/main.rs` — verify search module route mounting is compatible with the cache middleware layer (may need no changes if the middleware is applied at the module level)

## Implementation Notes
- The project already uses `tower-http` caching middleware (noted in Key Conventions). Follow the existing cache configuration pattern used by other endpoint route builders in the codebase.
- Apply caching at the search endpoint route level in `modules/search/src/endpoints/mod.rs`, not globally. This keeps cache behavior scoped to search.
- Use a short TTL (e.g., 30-60 seconds) since search indexes may be updated by the ingestor module (`modules/ingestor/`). The TTL should balance performance with data freshness.
- Set `Cache-Control: private, max-age=<TTL>` headers so that intermediate proxies don't cache user-specific search results.
- The cache key must include all query parameters (search term, entity_type, severity, date_from, date_to, offset, limit) to prevent serving stale results for different queries.
- Reference existing endpoint route builders (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs` or `modules/fundamental/src/advisory/endpoints/mod.rs`) for the pattern of adding middleware layers to Axum routes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration with middleware; reference for how tower-http caching is configured on existing endpoints
- `modules/fundamental/src/advisory/endpoints/mod.rs` — another example of route registration with middleware layers

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate Cache-Control headers
- [ ] Repeated identical search queries within the TTL window are served from cache (faster response time)
- [ ] Different query parameters (different search terms, filters, or pagination) produce different cache entries
- [ ] Cache does not serve stale results for different users or different query parameters
- [ ] Existing search functionality (results, ranking, filters) is unaffected by the cache layer

## Test Requirements
- [ ] Integration test: verify Cache-Control header is present on search responses
- [ ] Integration test: verify that two identical requests within TTL return consistent results
- [ ] Existing search tests in `tests/api/search.rs` continue to pass with caching enabled

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 3 — Search filters (caching must account for filter parameters in cache keys)

[sdlc-workflow] Description digest: sha256:803592a4bb9e596efa4b34c1dad5a7da2e12acb0bb9643639d129cc9a467941e
