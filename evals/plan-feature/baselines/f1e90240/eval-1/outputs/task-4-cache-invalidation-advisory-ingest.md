# Task 4: Add cache invalidation for advisory summaries on advisory ingestion

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

When the advisory ingestion pipeline links new advisories to an SBOM, cached advisory-summary responses for that SBOM must be invalidated. Modify the advisory ingestion flow to emit a cache invalidation signal after new advisory-SBOM relationships are stored. This ensures that subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return fresh counts rather than stale cached data.

## Acceptance Criteria

- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation targets only the affected SBOM's summary, not all cached summaries globally
- [ ] Ingestion pipeline continues to function correctly (no regressions in advisory storage or correlation)
- [ ] If no cache entry exists for the affected SBOM, the invalidation is a no-op (does not error)

## Test Requirements

- [ ] Unit test verifies that cache invalidation is called after advisory-SBOM linkage
- [ ] Unit test verifies that invalidation targets the correct SBOM ID
- [ ] Integration test verifies that a cached advisory-summary response is refreshed after a new advisory is ingested for the same SBOM

## Dependencies

- Task 3 (advisory-summary endpoint) -- the cache must exist before invalidation logic can target it

## Files to Modify

- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-SBOM relationship is stored

## Implementation Notes

- The advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Add the invalidation call after the step that inserts into the `sbom_advisory` join table (entity defined in `entity/src/sbom_advisory.rs`).
- Use the same cache infrastructure referenced by the `tower-http` caching middleware. If the cache is an in-memory store, inject a handle to it into the ingestor service. If it uses HTTP-level caching headers only, consider adding an application-level cache (e.g., `moka` or `mini-moka`) that the endpoint and ingestor share.
