## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, any cached advisory-summary response for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory ingestion completes, rather than serving stale cached counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisories are correlated with SBOMs during ingestion

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where `sbom_advisory` join records are created), add a call to invalidate the cached advisory-summary for the affected SBOM IDs.
- Follow the existing `tower-http` caching infrastructure used in the project. Determine how cached responses are keyed (likely by URL path including the SBOM ID) and use the appropriate invalidation mechanism (cache eviction by key, or cache busting via a version/generation counter).
- If the caching layer does not support programmatic invalidation, consider alternative approaches: (a) use ETag-based caching where the ETag changes when advisory counts change, (b) reduce cache TTL and rely on natural expiration, or (c) store a per-SBOM cache generation counter that the endpoint checks.
- The ingestion pipeline may process multiple advisories for multiple SBOMs in a single batch. Collect all affected SBOM IDs during the correlation step and invalidate caches for all of them.
- Reference `modules/ingestor/src/service/mod.rs` (`IngestorService`) for the overall ingestion flow and how services are composed.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion and correlation logic where invalidation hooks should be added
- `modules/ingestor/src/service/mod.rs::IngestorService` — the ingestion service orchestrator; may provide access to shared services or cache handles

## Acceptance Criteria
- [ ] After advisory ingestion links new advisories to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation targets only the affected SBOM IDs, not all cached summaries
- [ ] Existing advisory ingestion behavior is not altered beyond the added invalidation
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Integration test: ingest advisories for an SBOM, call advisory-summary (populates cache), ingest additional advisories for the same SBOM, call advisory-summary again and verify counts reflect the new advisories
- [ ] Test: verify that ingesting advisories for SBOM A does not invalidate the cache for SBOM B

## Verification Commands
- `cargo check -p ingestor` — expected: compiles without errors
- `cargo test -p ingestor` — expected: all tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256:10ccdcef125a410b2f6faf032d36f47fb9708718e034cc2d9eb9bb3a11cf4be6
