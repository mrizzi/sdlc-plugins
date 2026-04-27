## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-to-SBOM correlation step
- `modules/ingestor/src/service/mod.rs` — Pass cache handle or invalidation service to the advisory ingestion graph if not already available

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where an advisory is linked to an SBOM via the `sbom_advisory` join table in `entity/src/sbom_advisory.rs`), add a call to invalidate the cached advisory-summary for the affected SBOM ID(s).
- The caching infrastructure uses `tower-http` caching middleware. Examine how cache keys are constructed for the advisory-summary endpoint (set up in Task 3) and use the corresponding invalidation mechanism.
- If the caching layer does not expose a direct invalidation API, consider setting a cache-busting version key in the database or using a short-lived cache that the ingestion pipeline can signal to evict. Follow whichever pattern the existing caching infrastructure supports.
- Reference the SBOM ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` for the established pattern of post-ingestion hooks and service interactions.
- The `IngestorService` in `modules/ingestor/src/service/mod.rs` orchestrates ingestion; it may need to receive a cache handle or invalidation service as a dependency.
- Per the repository's key conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; follow its pattern for post-ingestion hooks and service interactions.
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion pipeline; the correlation step where SBOM-advisory links are created is the insertion point for cache invalidation.

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation does not degrade ingestion pipeline performance (invalidation is targeted, not a full cache flush)
- [ ] No new database tables are created

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify advisory-summary endpoint returns updated counts after ingestion
- [ ] Integration test: verify that advisory-summary for unrelated SBOMs is not invalidated when an advisory is ingested for a specific SBOM

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
