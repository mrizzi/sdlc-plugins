## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are cleared when new advisories are linked to an SBOM. Without this, dashboard widgets could display stale severity counts after new vulnerability advisories are correlated. The ingestion pipeline must invalidate the cache for any SBOM that gains new advisory links during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation completes

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles "Advisory ingestion: parse, store, correlate." After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`), add logic to invalidate the cached advisory-summary for all affected SBOM IDs.
- The invalidation mechanism depends on the caching infrastructure. If using tower-http's cache layer with in-memory storage, you may need to expose a cache handle or use a shared cache state that can be cleared by key pattern. If using HTTP cache headers only (no server-side cache store), invalidation may be handled by bumping a cache-busting version or reducing the cache TTL scope.
- Look at how the existing caching middleware is configured (per the Caching convention: "Uses tower-http caching middleware; cache configuration in endpoint route builders") to determine the appropriate invalidation approach.
- Identify all SBOM IDs affected by the ingestion batch and invalidate their cache entries specifically, rather than flushing the entire cache.
- Per Error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — The existing advisory ingestion correlation logic; add invalidation after the link-creation step
- `modules/ingestor/src/service/mod.rs::IngestorService` — Check if there is a shared service layer that could host cache invalidation coordination
- `entity/src/sbom_advisory.rs` — The join table entity used during correlation; use it to identify affected SBOM IDs

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET requests to `/api/v2/sbom/{id}/advisory-summary` for affected SBOMs return fresh data
- [ ] Cache invalidation is scoped to affected SBOMs only, not a global cache flush
- [ ] Ingestion pipeline continues to function correctly with no performance regression

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the advisory-summary endpoint returns updated counts
- [ ] Test verifying cache invalidation targets only the affected SBOM, not unrelated SBOMs

## Dependencies
- Depends on: Task 4 — Add endpoint caching
