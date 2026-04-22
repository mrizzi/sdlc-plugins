## Repository
trustify-backend

## Description
Add 5-minute response caching to the advisory-summary endpoint using the existing tower-http caching middleware. Additionally, implement cache invalidation in the advisory ingestion pipeline so that cached summaries are cleared when new advisories are linked to an SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add caching middleware configuration to the advisory-summary route with a 5-minute TTL
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation logic after advisory-to-SBOM correlation completes during ingestion

## Implementation Notes
1. **Caching**: The project uses `tower-http` caching middleware as noted in the repository conventions. In `modules/fundamental/src/sbom/endpoints/mod.rs`, apply cache configuration to the advisory-summary route using the same pattern used for other cached routes. Set `Cache-Control: max-age=300` (5 minutes) on the response, or configure the tower-http cache layer with a 300-second TTL.
2. **Cache invalidation**: In `modules/ingestor/src/graph/advisory/mod.rs`, after the advisory ingestion pipeline links an advisory to an SBOM (the correlation step), invalidate the cached advisory-summary for the affected SBOM ID. This may involve:
   - If using HTTP-level caching (Cache-Control headers), the cache will naturally expire. For forced invalidation, maintain a cache key registry or use an in-process cache (e.g., `moka` or `mini-moka`) that supports explicit eviction by key.
   - If using an application-level cache, add an eviction call keyed by SBOM ID after the `sbom_advisory` record is inserted.
3. The ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories -- the invalidation should occur after the correlate step where `sbom_advisory` rows are written.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route builder where caching middleware is applied
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion pipeline where invalidation must be triggered

## Acceptance Criteria
- [ ] Advisory-summary endpoint responses include `Cache-Control: max-age=300` header (or equivalent caching with 5-minute TTL)
- [ ] Repeated requests within 5 minutes are served from cache (faster response, no repeated DB query)
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, cached summary for that SBOM is invalidated
- [ ] After invalidation, next request to advisory-summary returns fresh data from the database

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors
- `cargo check -p trustify-ingestor` — Compiles without errors

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint and register route
