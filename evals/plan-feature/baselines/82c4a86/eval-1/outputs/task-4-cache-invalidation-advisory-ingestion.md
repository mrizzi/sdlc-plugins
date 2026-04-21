# Task 4 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Description
When new advisories are ingested and linked to an SBOM, any cached advisory-summary response for that SBOM must be invalidated. This ensures the severity aggregation endpoint always returns accurate counts after new advisory data is correlated with SBOMs.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — ensure the caching mechanism supports key-based invalidation (may require switching from middleware-level caching to an application-level cache if not already structured for invalidation)

## Implementation Notes
- The advisory ingestion pipeline at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After correlation, the ingestion code must invalidate the cached advisory-summary for all affected SBOM IDs.
- Inspect the existing caching infrastructure first. The repo uses `tower-http` caching middleware (per Key Conventions). If the middleware does not support selective key-based invalidation, consider introducing an application-level cache (e.g., a shared `HashMap` behind an `Arc<RwLock<>>` or an LRU cache crate) that the endpoint handler checks before executing the database query.
- The invalidation should be keyed by SBOM ID — when advisory ingestion links an advisory to SBOM X, invalidate the cache entry for SBOM X specifically, not the entire cache.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for how the SBOM ingestion pipeline is structured — the advisory ingestion follows a similar pattern.
- Per constraints §5.2: read the ingestion code before modifying. Per constraints §5.4: reuse existing cache infrastructure rather than introducing a new caching mechanism unless necessary.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where invalidation hook must be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline as a structural reference
- `modules/ingestor/src/service/mod.rs::IngestorService` — service orchestrating ingestion, may be the integration point for cache access

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` requests return updated counts reflecting the newly ingested advisory
- [ ] Cache invalidation is scoped to the affected SBOM IDs, not a global cache flush

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory-summary reflects the new advisory without waiting for cache expiry
- [ ] Integration test: verify that unrelated SBOM caches are not invalidated when a different SBOM receives a new advisory

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
