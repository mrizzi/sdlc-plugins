## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM during ingestion, the cached advisory-summary response for that SBOM is invalidated. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale severity counts for up to 5 minutes after new advisories are correlated, which could cause dashboards to display outdated severity breakdowns and alerting integrations to miss new critical advisories.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes; when an advisory is linked to an SBOM, invalidate the cached advisory-summary for that SBOM ID

## Implementation Notes
- The advisory ingestion module in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. Locate the point in the ingestion flow where `sbom_advisory` relationships are created (the correlation step) and add cache invalidation after this step.
- Use the existing `tower-http` caching infrastructure to invalidate cached responses. Determine the cache key pattern used for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint and invalidate entries matching the affected SBOM IDs.
- If `tower-http` caching does not support programmatic invalidation, consider an application-level cache (e.g., an in-memory cache with a shared state behind an `Arc<RwLock<HashMap<Uuid, CachedSummary>>>`) that the endpoint reads from and the ingestion pipeline can clear. Check the existing caching patterns used in the codebase before deciding on the approach.
- The invalidation must handle batch ingestion -- if a single advisory correlates with multiple SBOMs, all affected SBOM summaries must be invalidated.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for how SBOM ingestion handles post-processing hooks; follow a similar pattern for the invalidation hook.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect the advisory ingestion code before modifying; follow established patterns for how the ingestion pipeline interacts with other modules. Do not duplicate existing cache management logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; the correlation step where `sbom_advisory` records are created is the insertion point for cache invalidation
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how SBOM ingestion is structured; may contain similar post-processing patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — top-level service that orchestrates ingestion; may provide context for where cache invalidation fits in the pipeline

## Acceptance Criteria
- [ ] After an advisory is correlated with an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts reflecting the newly linked advisory
- [ ] Batch ingestion that links one advisory to multiple SBOMs invalidates all affected SBOM summaries
- [ ] No new database tables are introduced (per non-functional requirements)
- [ ] Existing advisory ingestion behavior is preserved

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Integration test: ingest an advisory affecting multiple SBOMs, verify all affected summaries are invalidated

## Verification Commands
- `cargo check -p trustify-module-ingestor` — compiles without errors
- `cargo test -p trustify-module-ingestor -- cache_invalidation` — relevant tests pass

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint with caching
