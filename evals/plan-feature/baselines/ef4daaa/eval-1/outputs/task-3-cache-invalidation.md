# Task 3 — Add cache invalidation for advisory summary in the ingestion pipeline

## Repository
trustify-backend

## Description
Ensure that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM through the advisory ingestion pipeline. When the ingestor correlates a new advisory with an SBOM, it must invalidate the cached advisory-summary response for that SBOM so subsequent requests return fresh data. This prevents stale severity counts from being served after new vulnerability advisories are discovered.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation
- `modules/ingestor/src/service/mod.rs` — add cache invalidation dependency/interface if needed

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where an advisory is linked to an SBOM via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory-summary cache entry.
- Use the existing `tower-http` cache infrastructure. The invalidation approach depends on the specific caching middleware configuration:
  - If using in-memory cache: invalidate by cache key pattern (e.g., `/api/v2/sbom/{id}/advisory-summary` for each affected SBOM ID)
  - If using HTTP cache-control headers: the 5-minute TTL from Task 2 serves as a natural invalidation, but consider adding a cache-busting mechanism for real-time accuracy
- Follow the existing ingestion pipeline patterns in `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion) for understanding how the pipeline is structured and where to inject post-processing hooks.
- The cache invalidation must target only the specific SBOM IDs affected by the new advisory correlation — do not invalidate all cached summaries.
- Per the non-functional requirements: "Cache invalidation: advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM."
- Per constraints doc section 5.2: Inspect the ingestion pipeline code before modifying it to understand the advisory-SBOM correlation flow.
- Per constraints doc section 5.8: Compare with sibling implementations (SBOM ingestion pipeline) for parity on cross-cutting concerns.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic; the invalidation hook goes here
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for understanding pipeline structure and post-processing patterns

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Only the affected SBOM's cache entry is invalidated, not all cached summaries
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that a subsequent advisory-summary request returns updated counts (not stale cached data)
- [ ] Integration test: verify that ingesting an advisory for SBOM-A does not invalidate the cache for SBOM-B

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching and route registration
