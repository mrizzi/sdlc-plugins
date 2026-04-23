## Repository
trustify-backend

## Description
Add HTTP response caching for search queries to reduce database load and improve perceived performance for repeated searches. The repository already uses `tower-http` caching middleware, so this task extends that existing pattern to the search endpoint.

**Assumption pending clarification**: The feature description says search should be "fast enough" but provides no cache TTL or staleness requirements. We assume a short cache TTL (e.g., 60 seconds) is appropriate for search results, since the underlying data (SBOMs, advisories) changes infrequently. This should be validated with the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `tower-http` cache control headers to search responses. Configure the cache layer on the search route builder, following the same pattern used by other endpoint modules. Set `Cache-Control: public, max-age=60` for search results.
- `server/src/main.rs` — If cache middleware is configured globally here, verify that the search routes are included in the caching layer. If search routes were previously excluded, update the route mounting to include them.

## Implementation Notes
- The repository uses `tower-http` caching middleware as noted in the conventions. Check `server/src/main.rs` for how cache middleware is applied to routes — it may be a global layer or per-route configuration.
- In `modules/search/src/endpoints/mod.rs`, add cache headers to the response. This can be done either via a `tower-http` `SetResponseHeader` layer on the route, or by setting headers directly in the handler response.
- Cache keys should include all query parameters (search term + filters) so that different searches are cached independently. This is typically handled automatically by HTTP caching based on the full URL.
- Consider adding `Vary: Accept` header if the endpoint supports multiple response formats.
- For cache invalidation: since search results depend on ingested data, the cache TTL should be short enough that new SBOMs/advisories appear in search results within a reasonable time. 60 seconds is a conservative default.

## Acceptance Criteria
- [ ] Search responses include appropriate `Cache-Control` headers
- [ ] Repeated identical search queries within the cache TTL do not hit the database
- [ ] Different search queries (different terms or filters) are cached independently
- [ ] Cache does not serve stale results beyond the configured TTL
- [ ] Caching follows the existing `tower-http` middleware pattern used elsewhere in the codebase

## Test Requirements
- [ ] Integration test: search response includes `Cache-Control` header with expected max-age value
- [ ] Integration test: verify response headers are present for both filtered and unfiltered queries
- [ ] Manual verification: two identical requests within TTL return the same response without additional DB query (observable via query logging)

## Dependencies
- Depends on: Task 3 — Add filter parameters to search endpoint
