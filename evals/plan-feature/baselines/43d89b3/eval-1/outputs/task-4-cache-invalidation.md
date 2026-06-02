## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. When the advisory ingestion process correlates a new advisory with an SBOM (creating a new `sbom_advisory` record), it must invalidate the cached advisory-summary for the affected SBOM ID. This ensures dashboard consumers always see up-to-date severity counts after new advisories are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation

## Implementation Notes
The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where `sbom_advisory` records are created), add a cache invalidation call for the affected SBOM's advisory-summary cache key.

The caching infrastructure uses `tower-http` middleware. Determine the cache invalidation mechanism by inspecting how existing cached routes are configured in `modules/fundamental/src/sbom/endpoints/mod.rs`. Common patterns include:
- Cache-key-based invalidation using the endpoint path pattern
- Shared cache store that supports programmatic eviction
- Event-based invalidation via a notification channel

The SBOM ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` may have existing cache invalidation patterns to follow.

Per CONVENTIONS.md §Error handling: wrap cache invalidation errors with `.context()` and handle gracefully — cache invalidation failures should log a warning but not fail the ingestion.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; may contain existing cache invalidation patterns to follow
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion pipeline; the target file, inspect existing correlation logic to identify the insertion point

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the advisory-summary cache for that SBOM is invalidated
- [ ] Cache invalidation failures are logged as warnings but do not fail the advisory ingestion process
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory for an SBOM, the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Test verifying that cache invalidation failure does not block advisory ingestion

## Verification Commands
- `cargo check -p trustify-ingestor` — Compiles without errors

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
