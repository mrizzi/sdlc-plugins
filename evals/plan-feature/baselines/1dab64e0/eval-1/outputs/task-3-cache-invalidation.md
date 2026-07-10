## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs.
- After the correlation step (where advisories are linked to SBOMs via the `sbom_advisory` join table), invalidate the cached advisory-summary for the affected SBOM IDs.
- Use the same cache invalidation mechanism used by the tower-http caching middleware configured in the endpoint route builders.
- Per CONVENTIONS.md §Error handling: wrap any cache invalidation errors with `.context()` to provide clear error messages.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust syntax scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for understanding the ingestion pipeline pattern and how cache invalidation might be integrated
- `modules/fundamental/src/sbom/endpoints/mod.rs` — where cache configuration is defined for the advisory-summary route; reference for the cache invalidation API

## Acceptance Criteria
- [ ] When a new advisory is ingested and correlated to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation does not block or degrade ingestion pipeline performance

## Test Requirements
- [ ] Integration test: ingest an advisory, verify cached summary is invalidated and new counts are returned
- [ ] Test that cache invalidation targets only the affected SBOM's cached summary, not all cached summaries

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching and threshold filter
