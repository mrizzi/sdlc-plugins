## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures the advisory-summary endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation step to clear cached advisory-summary responses for affected SBOMs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles advisory parsing, storage, and correlation with SBOMs. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), add a call to invalidate the cached advisory-summary for each affected SBOM ID.
- The caching layer uses tower-http caching middleware (per repository conventions). Determine the cache invalidation mechanism used by the existing tower-http setup — this may involve:
  - Emitting a cache-busting signal or cache key invalidation
  - Setting a cache tag on the advisory-summary response and invalidating by tag
  - Using an application-level cache (e.g., a shared HashMap or Redis) that can be explicitly cleared by key
- If the existing caching infrastructure does not support programmatic invalidation (tower-http's built-in cache is HTTP-level and may not support explicit purging), consider implementing an application-level cache layer (e.g., `moka` or a `DashMap`-based TTL cache) specifically for advisory-summary responses, which can be invalidated by SBOM ID.
- Keep the invalidation scoped to only the affected SBOMs — do not purge the entire cache. Extract the list of SBOM IDs from the advisory correlation results to determine which cache entries to invalidate.
- The ingestion pipeline is in the `ingestor` module which is a separate crate from `fundamental`. Ensure the cache invalidation mechanism is accessible cross-crate (e.g., via a shared service or trait in `common/`).

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion pipeline where invalidation logic will be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline for reference on how ingestion hooks are structured
- `common/src/db/mod.rs` — shared database utilities that may host a cache service

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET /api/v2/sbom/{id}/advisory-summary requests after invalidation return updated counts
- [ ] Cache invalidation is scoped to affected SBOMs only — unrelated cached responses are not purged
- [ ] No performance regression in the advisory ingestion pipeline (invalidation is lightweight)

## Test Requirements
- [ ] Test that after ingesting a new advisory linked to an SBOM, the advisory-summary endpoint returns updated counts (not stale cached values)
- [ ] Test that cache invalidation for one SBOM does not affect cached responses for other SBOMs

## Verification Commands
- `cargo check -p trustify-module-ingestor` — compiles without errors
- `cargo test -p trustify-module-ingestor advisory` — ingestion tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
