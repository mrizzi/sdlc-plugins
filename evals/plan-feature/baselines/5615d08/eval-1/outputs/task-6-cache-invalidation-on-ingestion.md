## Repository
trustify-backend

## Description
Ensure that when the advisory ingestion pipeline links new advisories to an SBOM, any cached advisory summary for that SBOM is invalidated. Without this, users would see stale severity counts for up to 5 minutes after new advisories are correlated, which could mask critical vulnerabilities.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory-to-SBOM correlation step, emit a cache invalidation call for the affected SBOM IDs
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a `invalidate_advisory_summary_cache(&self, sbom_id: Uuid)` method to `SbomService` (or a shared cache manager) that evicts the cached entry

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion flow correlates advisories with SBOMs by inserting rows into the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`). After the correlation step completes, collect the affected SBOM IDs and call the cache invalidation method.
- If the caching is HTTP-level only (via `Cache-Control` headers), invalidation is implicit — new data will be served after the TTL expires. However, if an application-level cache was introduced in Task 4, the ingestor must explicitly evict entries.
- If using an application-level cache, the cache should be accessible from both the `fundamental` module (for reads) and the `ingestor` module (for invalidation). This likely means the cache instance lives in the shared app state and is injected into both modules.
- Keep the invalidation logic minimal — just evict the cache key for the affected SBOM IDs. Do not re-compute the summary eagerly; let the next request trigger a fresh computation.
- Follow the existing service interaction patterns in `modules/ingestor/src/service/mod.rs` (`IngestorService`) for how the ingestor calls into other modules' services.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory correlation logic where invalidation must be hooked in
- `modules/ingestor/src/service/mod.rs::IngestorService` — Pattern for cross-module service calls from the ingestor

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent requests to the advisory-summary endpoint after ingestion return fresh (updated) counts
- [ ] Invalidation is scoped to the affected SBOM ID(s) only — other cached summaries are not evicted
- [ ] No errors or panics if invalidation is called for an SBOM ID that has no cached entry

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory summary endpoint reflects the new advisory count
- [ ] Integration test: verify that ingesting an advisory for SBOM-A does not invalidate the cache for SBOM-B

## Dependencies
- Depends on: Task 4 — Advisory summary caching (provides the cache layer that this task invalidates)
