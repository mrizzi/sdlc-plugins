# Task 4 — Add Cache Invalidation for Advisory Summary in Ingestion Pipeline

## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisory correlations are ingested, preventing stale severity counts from being served.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The correlation step links advisories to SBOMs via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- After the correlation step successfully links a new advisory to an SBOM, invalidate the cached advisory summary for the affected SBOM ID.
- Use the existing `tower-http` caching infrastructure to perform the invalidation. Identify how the cache layer is configured in the endpoint (Task 3) and use the corresponding invalidation mechanism.
- If the project uses an in-memory cache (e.g., `tower-http` `SetResponseHeader` or a shared cache store), the invalidation should clear the cache entry keyed by the SBOM ID.
- If the project uses HTTP cache-control headers only (no server-side cache store), the invalidation approach may involve updating a version/etag marker so subsequent requests bypass the cache.
- Inspect `modules/ingestor/src/service/mod.rs` (`IngestorService`) to understand the ingestion orchestration and find the right hook point for invalidation.
- Per `docs/constraints.md` §5.2: inspect the ingestion code before modifying it.
- Per `docs/constraints.md` §5.1: changes must be scoped to the files listed.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic; identify the exact function where SBOM-advisory links are created
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for understanding the ingestion flow and any existing cache invalidation patterns

## Acceptance Criteria
- [ ] After a new advisory is correlated to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting the newly linked advisory
- [ ] Invalidation only affects the specific SBOM(s) linked to the newly ingested advisory, not all cached summaries
- [ ] No performance regression in the advisory ingestion pipeline

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the advisory summary endpoint returns updated counts without waiting for cache expiry
- [ ] Integration test: verify that caching still works for SBOMs not affected by the new ingestion (no unnecessary invalidation)

## Dependencies
- Depends on: Task 3 — Add Advisory Summary Endpoint with Caching
