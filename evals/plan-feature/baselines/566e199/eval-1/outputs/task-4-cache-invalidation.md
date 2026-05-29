# Task 4 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Ensure that when new advisories are linked to an SBOM during the advisory ingestion pipeline, any cached advisory-summary response for that SBOM is invalidated. This prevents stale severity counts from being served after new advisories are correlated. The implementation must use the existing cache infrastructure without introducing new dependencies.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step to invalidate the advisory-summary cache entry for the affected SBOM ID(s)

## Implementation Notes
- Inspect `modules/ingestor/src/graph/advisory/mod.rs` to identify the point where advisory-SBOM links are created during ingestion. The invalidation call must happen after this correlation step.
- Use the existing `tower-http` cache infrastructure to invalidate entries. Determine how the caching layer is configured (in-memory cache store, external cache, etc.) by inspecting the cache setup in `server/src/main.rs` and the endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- If the cache is an in-memory store shared via application state, inject the cache handle into the ingestor service and call the appropriate invalidation method.
- If the cache is HTTP-level (Cache-Control headers only), document that invalidation is handled by TTL expiry and no active invalidation is needed — in that case, this task's scope reduces to verifying and documenting the TTL-based invalidation behavior.
- Follow error handling patterns from `common/src/error.rs` for any new error paths.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion logic where SBOM-advisory correlation occurs
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for reference on how the ingestor interacts with graph operations

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated (or TTL-based expiry is documented as the invalidation mechanism)
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion reflect the updated advisory counts
- [ ] No new database tables are introduced
- [ ] Existing advisory ingestion behavior is not broken

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify that the advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Integration test: verify that advisory ingestion for an SBOM not previously queried does not cause errors in cache invalidation

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
