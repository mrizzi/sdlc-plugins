## Repository
trustify-backend

## Description
Update the advisory ingestion pipeline to invalidate cached advisory-summary responses when new advisories are linked to an SBOM. Without this, the 5-minute cache on the advisory-summary endpoint could serve stale data after new advisories are ingested and correlated. The ingestion code must signal cache invalidation for affected SBOMs after advisory correlation completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-to-SBOM correlation is complete
- `modules/ingestor/src/service/mod.rs` — Ensure `IngestorService` has access to the cache invalidation mechanism (e.g., cache handle or invalidation channel)

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, after the advisory ingestion logic correlates advisories to SBOMs (linking rows in the `sbom_advisory` join table from `entity/src/sbom_advisory.rs`), add a call to invalidate the cached advisory-summary response for each affected SBOM ID.
- The invalidation mechanism depends on the existing `tower-http` caching setup. Common approaches: (1) use a shared cache store handle that supports key-based invalidation, keyed by the endpoint path `/api/v2/sbom/{id}/advisory-summary`; (2) use a cache-busting version counter stored alongside the SBOM; (3) publish an event that the caching layer listens to.
- Follow whatever cache invalidation pattern is already established in the codebase. If no invalidation pattern exists yet, the simplest approach is to add a cache store (e.g., `moka` or `mini-moka` in-memory cache) that the endpoint handler writes to and the ingestor can clear entries from.
- The `IngestorService` in `modules/ingestor/src/service/mod.rs` will need to receive the cache handle via dependency injection (constructor parameter), following the same pattern used to inject the database connection pool.
- Collect the set of affected SBOM IDs from the correlation step before triggering invalidation, to avoid invalidating the entire cache.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory correlation logic that links advisories to SBOMs; invalidation should happen right after this step
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service struct where cache handle dependency should be injected
- `entity/src/sbom_advisory.rs` — Join table entity used during correlation; query affected SBOM IDs from here

## Acceptance Criteria
- [ ] After advisory ingestion links new advisories to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Only affected SBOM caches are invalidated, not the entire cache
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` for the affected SBOM return fresh data
- [ ] Non-affected SBOM advisory-summary caches remain valid

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, then verify the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: verify that ingesting an advisory for SBOM A does not invalidate the cache for SBOM B

## Dependencies
- Depends on: Task 3 — Endpoint (cache invalidation requires the cached endpoint to exist)
