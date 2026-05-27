## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale counts for up to 5 minutes after new advisories are correlated with an SBOM.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory summary cache key.
- Follow the existing caching infrastructure pattern — `tower-http` caching middleware typically uses response-level caching. The invalidation approach should be consistent with how the project handles cache invalidation for other cached responses.
- If the project uses an explicit cache store (e.g., an in-memory cache or Redis), call the invalidation method directly. If caching is purely header-based (`Cache-Control`), document that cache invalidation is handled by TTL expiration and no programmatic invalidation is needed.
- Reference the `IngestorService` in `modules/ingestor/src/service/mod.rs` to understand the ingestion lifecycle and where the invalidation hook fits.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic to extend
- `modules/ingestor/src/service/mod.rs::IngestorService` — ingestion service orchestrating the pipeline

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, any cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return fresh counts reflecting the newly linked advisory
- [ ] The invalidation does not affect cached summaries for unrelated SBOMs

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts reflecting the new advisory
- [ ] Integration test: verify that ingesting an advisory for one SBOM does not invalidate the cache for a different SBOM

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching
