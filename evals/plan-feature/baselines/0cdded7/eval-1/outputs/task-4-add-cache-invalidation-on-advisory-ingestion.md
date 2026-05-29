## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after the advisory correlation pipeline processes new advisories, preventing stale severity counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The cache invalidation should be triggered after the correlation step that links advisories to SBOMs.
- Reference the existing `tower-http` caching infrastructure used by the repository. The cache invalidation mechanism depends on how the cache is configured — it may involve clearing a cache key derived from the SBOM ID, or using cache tags/groups. Inspect the caching setup in `modules/fundamental/src/sbom/endpoints/mod.rs` (where cache is configured for route builders) to understand the cache key strategy.
- The SBOM ingestion module at `modules/ingestor/src/graph/sbom/mod.rs` may provide a pattern for how ingestion pipelines interact with other modules — inspect it for cross-module call patterns.
- The invalidation must target cached responses for all SBOMs affected by the newly ingested advisory, not just a single SBOM. An advisory may be linked to multiple SBOMs during correlation.
- Follow the error handling pattern from `common/src/error.rs` — cache invalidation failures should be logged but not block the ingestion pipeline (advisory ingestion is more important than cache freshness).

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic where the invalidation hook will be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion patterns showing how ingestion modules interact with other subsystems
- `modules/fundamental/src/sbom/endpoints/mod.rs` — cache configuration that reveals the caching mechanism and key strategy

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation covers all SBOMs affected by a single advisory ingestion event
- [ ] Cache invalidation failures are logged but do not cause advisory ingestion to fail

## Test Requirements
- [ ] Test that ingesting a new advisory for an SBOM causes the cached summary to be refreshed on the next request
- [ ] Test that cache invalidation failure does not block advisory ingestion

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint (cache must exist before it can be invalidated)

[sdlc-workflow] Description digest: sha256:d05cc6be308d16ed7db8f0c092be993813a552b6598e004ddda94d95a14438b8
