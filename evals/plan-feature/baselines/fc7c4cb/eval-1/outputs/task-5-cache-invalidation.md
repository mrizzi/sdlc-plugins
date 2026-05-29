## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures the advisory summary endpoint returns fresh data after new advisories are ingested, rather than serving stale cached counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — ensure cache key structure supports per-SBOM invalidation (if not already addressable by the caching middleware)

## Implementation Notes
- The advisory ingestion pipeline is in `modules/ingestor/src/graph/advisory/mod.rs` — this is where advisories are parsed, stored, and correlated with SBOMs. The invalidation hook should be placed after the correlation step that links an advisory to an SBOM.
- Inspect the existing `tower-http` caching middleware configuration in `modules/fundamental/src/sbom/endpoints/mod.rs` to understand how cache keys are structured and how invalidation is triggered. The cache infrastructure is described in the Key Conventions as `tower-http` caching middleware.
- If the caching layer supports programmatic invalidation (e.g., cache store with a `remove` or `invalidate` method), call it with the cache key for the affected SBOM's advisory summary.
- If the caching layer is purely time-based (TTL only) without programmatic invalidation, consider adding a cache-busting mechanism — for example, a version counter or timestamp stored per-SBOM that is incremented during ingestion and included in the cache key.
- The SBOM ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` may also need inspection to understand the ingestion flow and how SBOM-advisory relationships are established.
- Ensure the invalidation is specific to the affected SBOM(s) — do not invalidate the entire cache, only the summaries for SBOMs that received new advisory correlations.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic; the invalidation hook integrates here
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for understanding the ingestion service patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — top-level ingestion service; may provide access to cache infrastructure

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Invalidation is scoped to the specific SBOM(s) affected, not a global cache flush
- [ ] Existing advisory ingestion behavior is not disrupted by the invalidation hook

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the advisory summary endpoint returns updated counts reflecting the new advisory
- [ ] Integration test: verify that ingesting an advisory for SBOM-A does not invalidate the cached summary for SBOM-B

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint

[sdlc-workflow] Description digest: sha256:aa0eebb03fff47d15d7c8eadcead36802aefb42daba39d12e5dce338c2bab7c9
