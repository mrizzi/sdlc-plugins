## Repository
trustify-backend

## Target Branch
main

## Description
Add response caching for the search endpoint to reduce database load for repeated
queries. This further addresses the "search should be faster" requirement from TC-9002
by avoiding redundant database round-trips for identical search queries within a
short time window.

ASSUMPTION (pending clarification): A short TTL cache (e.g., 60 seconds) is
appropriate for search results. Cache invalidation on data ingestion is not required
for MVP — stale results within the TTL window are acceptable.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `tower-http` caching middleware configuration to the search route builder, setting appropriate Cache-Control headers for search responses

## Implementation Notes
The repository already uses `tower-http` caching middleware (noted in Key Conventions:
"Uses tower-http caching middleware; cache configuration in endpoint route builders").

In `modules/search/src/endpoints/mod.rs` (route registration: `/api/v2/search`),
add cache layer configuration to the search route. Follow the existing caching
patterns used by other endpoint route builders in the codebase.

The cache configuration should:
- Set `Cache-Control: private, max-age=60` for search responses (short TTL)
- Vary on query parameters so different searches are cached independently
- Not cache error responses (4xx, 5xx status codes)

Reference `server/src/main.rs` (Axum server setup, route mounting) for how middleware
layers are applied to route groups.

Per CONVENTIONS.md §Caching: Uses `tower-http` caching middleware; cache configuration in endpoint route builders.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint registration: Each module's `endpoints/mod.rs` registers routes.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `server/src/main.rs` — Reference existing middleware layer application patterns for route groups
- Existing endpoint `mod.rs` files (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`) — Reference how other routes configure middleware layers

## Acceptance Criteria
- [ ] Search endpoint responses include appropriate Cache-Control headers
- [ ] Repeated identical search queries within the TTL window are served from cache (reduced database load)
- [ ] Different search queries (different query parameters) are cached independently
- [ ] Error responses (4xx, 5xx) are not cached
- [ ] Cache does not interfere with filter parameters (each unique filter combination is a separate cache entry)

## Test Requirements
- [ ] Search response headers include Cache-Control with expected max-age value
- [ ] Two identical requests within TTL return consistent results
- [ ] Requests with different query parameters are not incorrectly served from cache
- [ ] Error responses do not include cache headers (or include no-cache directive)

## Dependencies
- Depends on: Task 2 — Enhance SearchService with relevance-scored full-text search
