## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would return stale severity counts for up to 5 minutes after new advisories are correlated. The invalidation must trigger whenever the ingestion pipeline creates or updates entries in the `sbom_advisory` join table.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after the advisory-SBOM correlation step, targeting the cached advisory-summary for the affected SBOM ID(s)

## Implementation Notes
- Locate the code path in `modules/ingestor/src/graph/advisory/mod.rs` where new advisory-to-SBOM relationships are created in the `sbom_advisory` join table. This is the correlation step during advisory ingestion.
- After the correlation step completes, invalidate the cached advisory-summary for each affected SBOM ID. The exact invalidation mechanism depends on the existing cache infrastructure — look at how the tower-http caching middleware is configured and whether there is a cache store reference available in the ingestion context.
- If the caching layer uses HTTP-level caching (CDN or reverse proxy), consider emitting cache purge signals or using surrogate keys per SBOM ID.
- If the caching layer is application-level (in-memory or Redis), call the cache eviction method for the key pattern matching `/api/v2/sbom/{affected_sbom_id}/advisory-summary`.
- Follow the existing ingestion pipeline patterns in `modules/ingestor/src/graph/advisory/mod.rs` and `modules/ingestor/src/graph/sbom/mod.rs` for how post-processing hooks are structured.
- Per constraints (section 5.1), keep changes scoped to the advisory ingestion pipeline — do not modify unrelated ingestion code.
- No new database tables are required per the non-functional requirements.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion pipeline; the correlation step is the insertion point for invalidation logic
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for post-processing hook patterns if any exist
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service context that may hold cache references or event emitters

## Acceptance Criteria
- [ ] Cache invalidation is triggered when new advisories are linked to an SBOM during ingestion
- [ ] Invalidation targets only the affected SBOM's advisory-summary cache entry, not all cached entries
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion reflect the new advisory counts
- [ ] No new database tables are introduced
- [ ] `cargo check -p trustify-ingestor` compiles with no errors

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that a subsequent GET to advisory-summary returns updated counts (not stale cached data)
- [ ] Test that cache invalidation only affects the targeted SBOM, not other SBOMs' cached summaries

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor advisory` — ingestion tests pass

## Dependencies
- Depends on: Task 3 — Endpoint (cache must exist before invalidation can target it)
