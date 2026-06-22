# Task 4 — Add cache invalidation for advisory summaries

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always reflects the latest advisory correlation data within the cache TTL window.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are correlated with SBOMs during ingestion

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The correlation step links advisories to SBOMs via the `sbom_advisory` join table — this is the point where cache invalidation must be triggered.
- Use the existing cache infrastructure. Examine how `tower-http` caching is configured in the endpoint route builders to determine the cache invalidation mechanism (e.g., cache key eviction, cache store API). The cache key likely includes the SBOM ID and the endpoint path.
- If the caching middleware does not support programmatic invalidation (common with `tower-http`'s CacheLayer), consider an alternative approach: use a short-lived in-memory cache at the service layer (e.g., a `HashMap` with TTL) instead of or in addition to the HTTP cache layer, which can be explicitly invalidated.
- Follow error handling patterns from `modules/ingestor/src/service/mod.rs` (IngestorService) for any new error paths introduced by cache invalidation.
- Cache invalidation failures should be logged as warnings but must not fail the advisory ingestion pipeline — ingestion integrity takes priority over cache freshness.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic; the invalidation hook is added at the point where SBOM-advisory links are created
- `modules/ingestor/src/service/mod.rs::IngestorService` — reference for service-layer patterns and error handling in the ingestor module
- `modules/fundamental/src/sbom/endpoints/mod.rs` — contains the cache configuration for SBOM endpoints; reference to understand cache key structure

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Cache invalidation failures are logged as warnings and do not block advisory ingestion
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return updated counts

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory summary endpoint reflects the new advisory in its counts
- [ ] Test: verify that cache invalidation failure does not cause the ingestion to fail

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
