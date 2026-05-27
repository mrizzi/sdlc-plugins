## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table in `entity/src/sbom_advisory.rs`), add a cache invalidation call to clear the cached response for the affected SBOM's advisory summary endpoint.

The caching infrastructure uses `tower-http` caching middleware (per repo conventions). Inspect the existing cache configuration in `modules/fundamental/src/sbom/endpoints/mod.rs` to determine the exact cache layer being used (in-memory cache, Redis, or HTTP cache-control headers). The invalidation approach depends on the cache type:

- **HTTP cache-control headers only**: No server-side invalidation needed — the 5-minute TTL handles staleness naturally. However, document this limitation.
- **Server-side cache (in-memory or Redis)**: Add an explicit invalidation call using the cache key pattern for the advisory summary endpoint. Identify the cache key structure by inspecting the middleware configuration.

Inspect `modules/ingestor/src/service/mod.rs` (`IngestorService`) for the ingestion orchestration pattern and `modules/ingestor/src/graph/advisory/mod.rs` for where the SBOM-advisory correlation happens. The invalidation call should be placed immediately after new `sbom_advisory` records are inserted.

Per constraints §5.2: inspect the advisory ingestion code and cache configuration before modifying.
Per constraints §5.4: reuse the existing cache infrastructure rather than introducing a new caching mechanism.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion and correlation logic; the file where invalidation must be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for ingestion patterns and any existing cache invalidation examples

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates cached advisory severity summaries after linking new advisories to SBOMs
- [ ] Invalidation targets only the affected SBOM's cache entry, not all cached summaries
- [ ] Existing advisory ingestion behavior is unchanged — no regressions in advisory storage or correlation
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that a subsequent `GET /api/v2/sbom/{id}/advisory-summary` call reflects the updated counts (not stale cached data)
- [ ] Integration test: verify that ingesting an advisory for SBOM-A does not invalidate the cache for SBOM-B

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint handler


[sdlc-workflow] Description digest: sha256:9e1bfc5d7944bf9cd89b487bbe035219722c71f6914a82c39e46b756da0ef48c
