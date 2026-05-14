# Task 3 — Add cache invalidation for advisory summaries in advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
When new advisories are ingested and linked to SBOMs, the cached advisory severity summaries for affected SBOMs must be invalidated. This ensures that the 5-minute cache introduced in Task 2 does not serve stale data after the advisory ingestion pipeline links new advisories. Modify the advisory ingestion pipeline to invalidate cached summaries when new advisory-SBOM relationships are created.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory ingestion correlates advisories with SBOMs (creating `sbom_advisory` records), invalidate the cached advisory-summary response for each affected SBOM ID. Use the same cache invalidation mechanism available through the `tower-http` caching infrastructure.

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. Locate the point where `sbom_advisory` join records are created during correlation.
- Cache invalidation approach depends on the existing `tower-http` caching infrastructure pattern used in the project. Common approaches include:
  1. If using an in-memory cache store (e.g., `tower-http` `CacheLayer` with a shared store), inject the cache handle and call `remove()` or `invalidate()` for the affected SBOM advisory-summary cache keys.
  2. If using HTTP cache-control headers only (no server-side store), consider adding a cache-busting mechanism such as an ETag based on a last-modified timestamp on the `sbom_advisory` relationship, or reducing cache TTL and accepting eventual consistency.
- Inspect the `IngestorService` at `modules/ingestor/src/service/mod.rs` to understand how the ingestion pipeline is orchestrated and where cache handles could be injected.
- Follow existing error handling patterns: use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Per `docs/constraints.md` section 5.2: inspect existing code before modifying. Per section 5.4: reuse existing cache infrastructure rather than introducing a new caching mechanism.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic; extend rather than replace
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service orchestrator; reference for dependency injection patterns

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Existing advisory ingestion behavior is not altered (ingestion still stores and correlates correctly)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory-summary endpoint reflects the updated counts after ingestion (not stale cached values)
- [ ] Verify that advisory ingestion for an SBOM with no cached summary does not error (no-op invalidation)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
