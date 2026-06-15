## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures that the 5-minute cached responses from the advisory-summary endpoint do not serve stale data after new advisories are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- Locate the advisory ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` where advisories are correlated with SBOMs (the step that inserts into the `sbom_advisory` join table defined in `entity/src/sbom_advisory.rs`).
- After the correlation step, add a cache invalidation call that clears the cached advisory-summary for the affected SBOM IDs.
- The cache invalidation mechanism depends on the existing `tower-http` caching infrastructure. If the cache is in-memory (e.g., a `tower-http` cache layer), the invalidation may require a shared cache handle or a cache-busting strategy (e.g., incrementing a version key, sending an internal event, or using cache tags).
- If the existing caching infrastructure does not support targeted invalidation, consider an alternative approach: use an ETag or Last-Modified based strategy where the ingestion pipeline updates a timestamp that the endpoint checks, allowing the cache layer to serve stale-while-revalidate or force a miss.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the SBOM ingestion pattern to understand how the ingestion pipeline is structured and where post-processing hooks are added.
- Per Key Conventions §Error handling: wrap any cache invalidation errors with `.context()` and handle gracefully — cache invalidation failure should log a warning but not fail the advisory ingestion. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion pipeline structure and post-processing patterns
- `modules/ingestor/src/graph/advisory/mod.rs` — the target file; study the existing correlation step to identify the exact insertion point for cache invalidation

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation failure does not cause the advisory ingestion to fail
- [ ] Cache invalidation is scoped to affected SBOM IDs only, not a full cache purge

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that the advisory-summary endpoint reflects the updated count
- [ ] Test: verify that cache invalidation failure is logged as a warning but does not block advisory ingestion
- [ ] Test: verify that non-affected SBOM summaries remain cached after ingestion of advisories for a different SBOM

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

[sdlc-workflow] Description digest: sha256-md:9f0abeafbef32b4d7164ffdd183914073c4379cbf9e256a01bf607b6be122fd1
