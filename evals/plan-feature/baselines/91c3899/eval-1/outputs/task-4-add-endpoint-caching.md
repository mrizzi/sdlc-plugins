## Repository
trustify-backend

## Target Branch
main

## Description
Configure 5-minute caching on the advisory-summary endpoint using the existing tower-http caching middleware. The cache must be keyed by SBOM ID and threshold parameter so that different queries return correct cached results. This fulfills the non-functional requirement of p95 < 200ms response time for repeat requests.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add cache configuration to the advisory-summary handler or route builder
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Apply caching middleware layer to the advisory-summary route if caching is configured at the route level

## Implementation Notes
- Follow the existing caching pattern described in the repository conventions: "Uses tower-http caching middleware; cache configuration in endpoint route builders." Examine other endpoints in `modules/fundamental/src/sbom/endpoints/mod.rs` for examples of how caching middleware is applied to routes.
- Set cache TTL to 5 minutes (300 seconds) using appropriate `tower-http` cache control headers or middleware configuration.
- Ensure the cache key includes both the SBOM ID path parameter and the threshold query parameter, so that `GET /api/v2/sbom/123/advisory-summary` and `GET /api/v2/sbom/123/advisory-summary?threshold=critical` are cached separately.
- Per Caching convention: uses tower-http caching middleware; cache configuration in endpoint route builders. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint file scope.
- Per Endpoint registration convention: each module's endpoints/mod.rs registers routes; server/main.rs mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Examine existing route definitions to see how tower-http caching middleware is applied to other SBOM endpoints

## Acceptance Criteria
- [ ] Advisory-summary endpoint responses include cache control headers with 5-minute TTL
- [ ] Repeated requests within the cache window return cached responses
- [ ] Different query parameters (e.g., different threshold values) are cached independently
- [ ] Cache does not interfere with 404 responses for non-existent SBOMs

## Test Requirements
- [ ] Test verifying cache control headers are present in the advisory-summary response
- [ ] Test verifying repeated requests within cache window return consistent results

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
