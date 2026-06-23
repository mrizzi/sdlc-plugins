## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory correlation completes, meeting the non-functional requirement that cached summaries stay current with ingested advisory data.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation completes

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles advisory parsing, storage, and correlation with SBOMs. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a cache invalidation call for the affected SBOM's advisory summary.
- Identify how `tower-http` caching middleware manages cache keys. The cache key for the advisory summary endpoint is likely based on the request path (`/api/v2/sbom/{id}/advisory-summary`). Invalidate by clearing the cache entry for the specific SBOM ID that was updated.
- If `tower-http` does not support fine-grained cache invalidation by key, consider alternative strategies:
  - Use a shared cache store (e.g., an in-memory `HashMap` with TTL) that can be explicitly invalidated from the ingestion pipeline
  - Add an ETag or last-modified timestamp to the response and check it during cache validation
- Follow the existing ingestion pipeline pattern in `modules/ingestor/src/graph/advisory/mod.rs` for where to insert the invalidation call — it should occur after successful advisory-SBOM linking, not before.
- Ensure the invalidation is idempotent — invalidating a cache entry that does not exist should be a no-op.
- Per CONVENTIONS.md §Error handling: use `.context()` wrapping for any errors during cache invalidation to provide clear error context.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion flow; extend the existing correlation logic rather than adding a separate post-processing step
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; check if it already performs cache invalidation that can be used as a pattern

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM via the ingestion pipeline, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting the newly linked advisory
- [ ] Cache invalidation is idempotent — no errors if the cache entry does not exist

## Test Requirements
- [ ] Integration test: after ingesting a new advisory for an SBOM, the advisory summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: cache invalidation does not error when no cache entry exists for the SBOM

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

[sdlc-workflow] Description digest: sha256-md:e633f4504c7626f0a9e6c3dc26039922d169d3119f96ce4655a8f79f1bf9200e
