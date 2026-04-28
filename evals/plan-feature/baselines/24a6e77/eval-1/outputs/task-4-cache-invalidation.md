# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Description
Extend the advisory ingestion pipeline to invalidate the cached advisory summary for affected SBOMs when new advisories are linked. Without this, the 5-minute cache on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale data after new advisories are correlated with an SBOM. The cache invalidation must target only the specific SBOM(s) affected by the newly ingested advisory, not the entire cache.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after the advisory-to-SBOM correlation step, targeting the advisory summary cache entries for all SBOMs linked to the newly ingested advisory

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories — locate the step where advisory-SBOM links are created (using the `sbom_advisory` join table at `entity/src/sbom_advisory.rs`) and add invalidation after that step
- Determine the caching mechanism used by the `tower-http` middleware — if it uses HTTP-level caching (Cache-Control headers), invalidation may require a different strategy such as:
  - A cache key store that can be explicitly cleared per SBOM ID
  - An ETag or Last-Modified based approach where the advisory ingestion updates a version counter
  - A shared in-memory cache (e.g., `moka` or similar) that the endpoint writes to and the ingestor can invalidate
- Check how existing caching is implemented in the codebase before deciding on the invalidation approach — the approach must be consistent with the existing cache infrastructure
- After linking an advisory to SBOM(s), collect all affected SBOM IDs and invalidate their cached advisory summary responses
- Per constraints (Section 5.2): inspect the advisory ingestion code and existing cache infrastructure before modifying
- Per constraints (Section 5.4): reuse the existing cache infrastructure rather than introducing a new caching mechanism

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where SBOM correlation happens
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline, may contain existing cache invalidation patterns to follow
- `entity/src/sbom_advisory.rs` — join table entity used during advisory-SBOM correlation

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return fresh data
- [ ] Only affected SBOM caches are invalidated — unrelated SBOMs retain their cached summaries
- [ ] No new caching mechanisms are introduced — existing cache infrastructure is reused

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify cached summary is invalidated and fresh data is returned on next request
- [ ] Integration test: ingest an advisory linked to SBOM A, verify SBOM B's cache is not invalidated

## Verification Commands
- `cargo build -p trustify-ingestor` — should compile without errors
- `cargo test -p trustify-tests --test api` — integration tests should pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
