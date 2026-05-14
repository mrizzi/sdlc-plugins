## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are correlated with an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory-to-SBOM correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a call to invalidate the cached advisory summary for each affected SBOM ID. This ensures that the next request to the advisory-summary endpoint fetches fresh data from the database.

## Implementation Notes
- Locate the section in `modules/ingestor/src/graph/advisory/mod.rs` where the ingestion pipeline writes to the `sbom_advisory` join table (i.e., where `entity::sbom_advisory` records are inserted). After this write, collect the affected SBOM IDs.
- Follow the existing `tower-http` caching pattern used by the project. If the project uses an in-memory cache layer (e.g., `tower-http`'s built-in cache store), invalidation may require clearing cache entries keyed by the response URI (`/api/v2/sbom/{id}/advisory-summary`). Check how the cache middleware is configured in `server/src/main.rs` and `modules/fundamental/src/sbom/endpoints/mod.rs`.
- If the caching mechanism is purely HTTP header-based (`Cache-Control: max-age=300`) without a server-side cache store, then explicit invalidation is not possible at the middleware level. In that case, implement a lightweight in-memory cache (e.g., `moka` or `mini-moka` crate) in the service layer (`modules/fundamental/src/sbom/service/sbom.rs`) for the advisory summary specifically, and invalidate entries in that cache from the ingestor. Add the cache dependency to `modules/fundamental/Cargo.toml` and `modules/ingestor/Cargo.toml`.
- The invalidation must handle the case where a single advisory is linked to multiple SBOMs — all affected SBOM caches must be invalidated.
- Use error logging (not hard failure) if cache invalidation fails, so that ingestion is not blocked by cache issues.

## Acceptance Criteria
- [ ] After advisory ingestion links new advisories to SBOMs, the cached advisory summary for those SBOMs is invalidated
- [ ] Subsequent requests to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting newly ingested advisories
- [ ] Cache invalidation handles the case where one advisory affects multiple SBOMs
- [ ] Cache invalidation failure does not cause advisory ingestion to fail (logged as warning, not error-level abort)

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: ingest an advisory linked to multiple SBOMs, verify all affected SBOM summaries are updated

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (the cache to invalidate must exist first)
