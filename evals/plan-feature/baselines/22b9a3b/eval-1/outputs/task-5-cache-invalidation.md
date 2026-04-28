## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are cleared when new advisories are linked to an SBOM. Without this, dashboard widgets could display stale severity counts after new advisory correlations are ingested. The invalidation must target the specific SBOM(s) affected by the newly ingested advisory.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation is stored

## Implementation Notes
- The advisory ingestion pipeline is in `modules/ingestor/src/graph/advisory/mod.rs`, which handles parsing, storing, and correlating advisories. After the step that links an advisory to SBOM(s) via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), add a cache invalidation call for the affected SBOM IDs.
- Determine how the existing `tower-http` cache is accessed for invalidation. Common patterns include:
  1. A shared cache handle/store injected via Axum state that supports explicit key eviction
  2. A cache-busting approach where the ingestion pipeline increments a version counter or cache tag, and the endpoint includes the tag in its cache key
- If the tower-http cache does not support programmatic invalidation, consider an alternative approach: store a "last-modified" timestamp per SBOM in the database (or in-memory store), check it in the endpoint handler, and bypass the cache when the timestamp is newer than the cached response.
- The invalidation should target only the SBOM IDs that are linked to the newly ingested advisory — not a global cache flush. Extract the affected SBOM IDs from the correlation step in the ingestion pipeline.
- Follow the error handling pattern in `modules/ingestor/src/graph/advisory/mod.rs`: use `Result<T, AppError>` with `.context()` wrapping. Cache invalidation failures should be logged as warnings but should not fail the overall ingestion operation.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic; the invalidation call is added after the existing correlation step
- `entity/src/sbom_advisory.rs` — join table entity; used during correlation to identify affected SBOM IDs
- `modules/ingestor/src/service/mod.rs::IngestorService` — the service orchestrating ingestion; may hold the cache handle in its state

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Only the affected SBOM's cache entries are invalidated — other SBOM caches remain intact
- [ ] Cache invalidation failures are logged as warnings and do not block advisory ingestion
- [ ] After invalidation, the next request to the advisory-summary endpoint returns fresh data reflecting the newly ingested advisory

## Test Requirements
- [ ] Integration test: ingest an SBOM, query its advisory-summary (populating cache), ingest a new advisory linked to the same SBOM, query advisory-summary again, verify the counts reflect the new advisory
- [ ] Integration test: ingest an advisory linked to SBOM-A, verify SBOM-B's cached advisory-summary is not invalidated

## Dependencies
- Depends on: Task 4 — Cache integration for advisory summary
