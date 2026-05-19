## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached severity summaries when new advisories are linked to an SBOM. Without this, the 5-minute cached responses will serve stale data after new advisory correlations are ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- After the advisory-to-SBOM correlation step completes, add cache invalidation logic for the affected SBOM IDs' advisory-summary responses. This ensures newly ingested advisories are reflected in subsequent summary queries.

## Implementation Notes
The advisory ingestion module in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step that links an advisory to one or more SBOMs (which writes to the `sbom_advisory` join table in `entity/src/sbom_advisory.rs`), the cache for affected SBOM advisory summaries must be invalidated.

The project uses `tower-http` caching middleware. Cache invalidation should follow whatever pattern the existing caching infrastructure supports -- this may involve:
- Programmatic cache eviction by key if the cache layer supports it
- Setting `Cache-Control: no-cache` or `must-revalidate` directives
- Or a cache-busting approach consistent with the existing tower-http setup

Inspect the existing caching configuration in `modules/fundamental/src/sbom/endpoints/mod.rs` and `server/src/main.rs` to determine the correct invalidation mechanism.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- The existing advisory correlation logic; add invalidation after the correlation step
- `modules/ingestor/src/service/mod.rs::IngestorService` -- Reference for how the ingestor interacts with other services

## Acceptance Criteria
- [ ] When a new advisory is correlated with an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent `GET /api/v2/sbom/{id}/advisory-summary` calls after ingestion return updated counts
- [ ] Existing advisory ingestion functionality is not broken

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify the summary endpoint returns updated counts without waiting for cache expiry

## Verification Commands
- `cargo check -p trustify-ingestor` -- compiles without errors
- `cargo test -p trustify-ingestor` -- all tests pass

## Dependencies
- Depends on: Task 3 -- Endpoint with caching (the cache must exist before invalidation logic can be implemented)
