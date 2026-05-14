## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached
advisory-summary responses are cleared when new advisories are linked to an SBOM.
Without this, the advisory-summary endpoint would serve stale severity counts for
up to 5 minutes after new advisories are correlated with an SBOM.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes; when the ingestion pipeline links a new advisory to an SBOM, invalidate the cached advisory-summary for that SBOM ID

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` is where advisories are parsed, stored, and correlated with SBOMs. Locate the correlation step where `sbom_advisory` join records are inserted and add cache invalidation immediately after.
- The caching infrastructure uses `tower-http` caching middleware. Identify how cached responses are keyed and how to programmatically invalidate a specific cache entry. If the cache is an in-process LRU or TTL cache, call its `remove` or `invalidate` method with the cache key corresponding to `/api/v2/sbom/{sbom_id}/advisory-summary`. If cache keys are derived from the request URI, construct the key using the same pattern.
- If `tower-http` does not support programmatic per-key invalidation, consider an alternative approach: use a secondary cache layer (e.g., a shared `HashMap<Uuid, Instant>` tracking last-invalidation timestamps per SBOM) that the endpoint handler checks before returning cached data. The handler would compare the cached response timestamp against the invalidation timestamp and refetch if stale.
- Follow the error handling pattern in `modules/ingestor/src/graph/advisory/mod.rs` — cache invalidation failures should be logged as warnings but not cause the ingestion to fail (cache invalidation is best-effort).
- Inspect `modules/ingestor/src/service/mod.rs` (`IngestorService`) to understand how the ingestion pipeline is structured and where the advisory correlation step is invoked.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing ingestion code before modifying it, and keep changes scoped to cache invalidation only — do not refactor unrelated ingestion logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic where the invalidation hook should be added
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how SBOM ingestion handles post-processing steps, useful as a pattern for adding post-correlation hooks

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint (cache must exist before invalidation can target it)

## Acceptance Criteria
- [ ] When the advisory ingestion pipeline links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation failures are logged as warnings and do not cause ingestion to fail
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return fresh data
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify cached advisory-summary is invalidated and a subsequent request returns updated counts
- [ ] Unit test: verify cache invalidation is called when a new `sbom_advisory` record is created during ingestion
- [ ] Unit test: verify that a cache invalidation failure does not propagate as an error from the ingestion pipeline

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
