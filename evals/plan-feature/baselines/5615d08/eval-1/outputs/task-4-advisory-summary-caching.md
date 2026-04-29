## Repository
trustify-backend

## Description
Add a 5-minute cache layer to the advisory summary endpoint so repeated requests for the same SBOM's severity counts are served from cache without hitting the database. This meets the non-functional requirement of p95 < 200ms response time and reduces database load for frequently accessed SBOMs.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Wrap the handler or route with `tower-http` caching middleware configured for a 5-minute TTL
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Apply the cache layer to the advisory-summary route if caching is configured at the route level

## Implementation Notes
- The repository uses `tower-http` caching middleware as noted in the conventions. Apply caching at the route builder level in `modules/fundamental/src/sbom/endpoints/mod.rs`, following the existing caching patterns used for other endpoints.
- Set `Cache-Control: max-age=300` (5 minutes) on the response, either via middleware or by setting the header explicitly in the handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`.
- The cache key should incorporate the SBOM ID from the path to ensure per-SBOM caching.
- If the project uses an in-memory cache (e.g., `moka` or a custom cache in the app state), store the `AdvisorySeveritySummary` keyed by SBOM UUID with a 5-minute expiry. Otherwise, rely on HTTP-level caching via `Cache-Control` headers and any reverse proxy in front of the service.
- Ensure the cache respects the `Cache-Control` header so downstream reverse proxies and CDNs can also cache the response.

## Acceptance Criteria
- [ ] Advisory summary response includes `Cache-Control: max-age=300` header
- [ ] Repeated requests within 5 minutes for the same SBOM ID do not execute a new database query (if using application-level cache) or are served by HTTP cache layer
- [ ] Different SBOM IDs are cached independently
- [ ] Cache entry expires after 5 minutes, and subsequent requests hit the database

## Test Requirements
- [ ] Integration test: verify the response includes `Cache-Control: max-age=300` header
- [ ] Integration test: if application-level caching, verify that two rapid sequential requests result in only one database query

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (provides the handler and route to add caching to)
