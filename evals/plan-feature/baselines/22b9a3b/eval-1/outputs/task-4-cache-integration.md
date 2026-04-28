## Repository
trustify-backend

## Description
Add 5-minute response caching to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint using the existing `tower-http` caching middleware infrastructure. This ensures that repeated requests for the same SBOM's advisory summary within a 5-minute window are served from cache, meeting the p95 < 200ms latency requirement for SBOMs with up to 500 advisories.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add cache layer configuration to the advisory-summary route
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add appropriate cache-control headers to the response if needed

## Implementation Notes
- Per the key conventions: the project uses `tower-http` caching middleware with cache configuration in endpoint route builders. Follow the existing cache configuration pattern used by other endpoints in the SBOM module.
- Examine how caching is applied to other routes in `modules/fundamental/src/sbom/endpoints/mod.rs` — the cache middleware is likely applied as a layer on the route builder with a TTL configuration.
- Set the cache TTL to 5 minutes (300 seconds) as specified in the feature requirements.
- The cache key should incorporate both the SBOM ID path parameter and the optional `?threshold` query parameter so that different threshold values produce separate cache entries.
- Consider setting `Cache-Control: max-age=300` headers on the response to support HTTP-level caching if downstream proxies or CDNs are in use.
- Do not introduce any new caching dependencies — use only the existing `tower-http` cache infrastructure.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder with cache layer configuration for other SBOM endpoints; replicate the same caching pattern

## Acceptance Criteria
- [ ] The advisory-summary endpoint response is cached for 5 minutes
- [ ] Different SBOM IDs produce separate cache entries
- [ ] Different threshold query parameter values produce separate cache entries
- [ ] The cache uses the existing tower-http caching middleware — no new caching dependencies are introduced
- [ ] Subsequent requests within the 5-minute TTL return responses faster than the initial request

## Test Requirements
- [ ] Integration test: send two identical requests within 5 minutes, verify the second request returns the same response and is served faster (or verify via cache-hit headers if available)
- [ ] Integration test: send requests with different threshold values, verify they produce separate cached responses

## Dependencies
- Depends on: Task 3 — Advisory summary REST endpoint
