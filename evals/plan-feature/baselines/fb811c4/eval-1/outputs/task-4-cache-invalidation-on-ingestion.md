## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, any cached advisory severity summaries for that SBOM are invalidated. This ensures dashboard widgets always show up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation completes

## Implementation Notes
1. **Invalidation point**: In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion flow parses, stores, and then correlates advisories with SBOMs. After the correlation step completes (where `sbom_advisory` join records are inserted), add a cache invalidation call for the affected SBOM IDs.

2. **Cache key pattern**: The cache key for the advisory-summary endpoint follows the tower-http URI-based caching pattern. Invalidate entries matching the pattern `/api/v2/sbom/{sbom_id}/advisory-summary*` (including any query parameter variants) for each SBOM ID that received new advisory links.

3. **Identifying affected SBOMs**: The correlation step in `modules/ingestor/src/graph/advisory/mod.rs` already knows which SBOM IDs are being linked. Collect these IDs during correlation and pass them to the invalidation logic.

4. **Error handling**: Cache invalidation failures should be logged as warnings but should not fail the ingestion transaction. Use `.context()` wrapping consistent with `common/src/error.rs` patterns, but convert the error to a log warning rather than propagating it.

5. **IngestorService integration**: If the cache handle is not directly accessible from the graph module, pass it through `modules/ingestor/src/service/mod.rs` (`IngestorService`) which coordinates the ingestion pipeline and has access to shared application state.

## Acceptance Criteria
- [ ] After advisory ingestion links new advisories to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation failure does not cause advisory ingestion to fail
- [ ] Only affected SBOM caches are invalidated (not all caches globally)
- [ ] Crate compiles without errors

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint (establishes the cache configuration to invalidate)

[sdlc-workflow] Description digest: sha256-md:a897f178f9874c2f2571624a9ff19020350ac9c3a0f69fb7ebbe8cd69a3379e7
