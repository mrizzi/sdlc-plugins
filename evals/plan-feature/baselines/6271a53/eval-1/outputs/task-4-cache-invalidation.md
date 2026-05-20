# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns fresh data after new advisories are correlated with an SBOM, meeting the non-functional requirement that the cache does not serve stale severity counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step to invalidate the advisory-summary cache entry for the affected SBOM(s)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — if cache invalidation requires a shared cache key pattern or cache handle, expose or extract the cache key construction used by the advisory-summary route

## Implementation Notes
- Inspect the advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` to find the point where advisories are linked to SBOMs (the correlation step). The cache invalidation hook should be placed immediately after this correlation completes.
- The cache invalidation strategy depends on how `tower-http` caching is configured for the advisory-summary route. Two common patterns:
  1. If using an in-memory cache store with key-based invalidation, extract the cache key for `/api/v2/sbom/{id}/advisory-summary` and invalidate it.
  2. If using HTTP cache-control headers only, the 5-minute TTL may be sufficient and explicit invalidation may not be needed — verify with the cache middleware configuration.
- If the ingestion pipeline processes advisories in bulk, identify all SBOM IDs affected by the ingestion batch and invalidate cache entries for each one.
- Follow the existing error handling patterns in the ingestor module (see `modules/ingestor/src/service/mod.rs` for `IngestorService` patterns).
- Per constraints doc section 5.2: read the advisory ingestion module before modifying to understand the correlation step and available cache infrastructure.
- Per constraints doc section 5.4: reuse existing cache infrastructure rather than introducing a new caching mechanism.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic where the invalidation hook will be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module for reference on how ingestion modules are structured
- `modules/fundamental/src/sbom/endpoints/mod.rs` — cache middleware configuration for the advisory-summary route

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates the advisory-summary cache for affected SBOM(s) after linking new advisories
- [ ] Cache invalidation is triggered only when advisory-SBOM correlations are created or updated, not on every ingestion
- [ ] Existing advisory ingestion behavior is not altered (no regressions)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent `GET /api/v2/sbom/{id}/advisory-summary` reflects the newly ingested advisory (not stale cached data)
- [ ] Integration test: ingest an advisory NOT linked to a specific SBOM, verify that the SBOM's advisory-summary cache is not invalidated unnecessarily

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
