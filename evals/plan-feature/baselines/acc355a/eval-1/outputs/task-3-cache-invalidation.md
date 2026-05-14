## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts for up to 5 minutes after new advisory correlations are processed.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation is established, clearing the cached advisory-summary for affected SBOM IDs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where `sbom_advisory` rows are inserted), add a cache invalidation call for each affected SBOM ID.
- Follow the existing caching infrastructure used by `tower-http` caching middleware. The invalidation mechanism depends on the cache backend — review how caching is configured in the endpoint route builders to determine the correct invalidation API (e.g., cache key pattern matching on the SBOM ID path segment).
- The cache key for the advisory-summary endpoint will include the SBOM ID in the URL path (`/api/v2/sbom/{id}/advisory-summary`). Invalidation should target this specific path pattern for the affected SBOM IDs.
- Ensure the invalidation is performed within the same transaction or immediately after the advisory correlation commits, to prevent a race where a request reads stale data after the correlation is committed but before invalidation occurs.
- Reference the `IngestorService` in `modules/ingestor/src/service/mod.rs` for the overall ingestion flow to understand where the correlation step fits in the pipeline.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion module where the correlation step lives; this is the insertion point for cache invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — the ingestion service orchestrator; reference for understanding the ingestion pipeline flow
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity; used to identify which SBOMs are affected when a new advisory is correlated

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated severity counts
- [ ] Invalidation targets only the affected SBOM IDs, not the entire cache

## Test Requirements
- [ ] Test that after ingesting a new advisory linked to an SBOM, the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Test that invalidation is scoped to the affected SBOM — other SBOMs' cached summaries remain intact

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
