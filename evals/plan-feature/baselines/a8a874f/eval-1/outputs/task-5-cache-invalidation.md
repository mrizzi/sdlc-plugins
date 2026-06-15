# Task 5: Add cache invalidation for advisory-summary on advisory ingestion

## Repository

trustify-backend

## Target Branch

main

## Dependencies

- Task 3 (advisory-summary endpoint with caching)

## Description

When the advisory ingestion pipeline links new advisories to an SBOM, cached advisory-summary responses for that SBOM must be invalidated. This ensures that dashboard widgets and API consumers see updated severity counts after new advisories are correlated. Implement cache invalidation in the advisory ingestion path so that the 5-minute cached responses do not serve stale data after ingestion events.

## Files to Modify

- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-to-SBOM correlation completes

## Implementation Notes

- The advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the point where advisory-SBOM links are created (likely after inserting into the `sbom_advisory` join table referenced in `entity/src/sbom_advisory.rs`).
- The caching strategy uses `tower-http` caching middleware. Investigate how the existing cache infrastructure supports key-based invalidation. If it uses an in-memory cache layer, invalidate the cache entry keyed by the SBOM ID. If it relies purely on HTTP `Cache-Control` headers with no server-side cache store, document this limitation and ensure the TTL is the only cache mechanism (no additional work needed beyond the 5-minute TTL).
- If server-side cache invalidation is supported, call the invalidation after the transaction that links advisories to SBOMs commits successfully.
- Reference `modules/ingestor/src/service/mod.rs` (`IngestorService`) for the service layer patterns used during ingestion.

### Applicable Conventions

- **Error handling**: Applies: task modifies `mod.rs` in the ingestor graph module matching the convention's Rust source file scope -- cache invalidation errors should be logged but not fail the ingestion transaction.

## Acceptance Criteria

- [ ] After advisory ingestion links a new advisory to an SBOM, the advisory-summary cache for that SBOM is invalidated (or documented as TTL-only if server-side invalidation is not supported)
- [ ] Cache invalidation does not cause advisory ingestion to fail -- errors are logged, not propagated
- [ ] Cache invalidation occurs after the database transaction commits, not before

## Test Requirements

- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent advisory-summary request reflects the new advisory (not stale cached data)
- [ ] Integration test: cache invalidation failure (if testable) does not cause ingestion to fail

[Description digest: sha256-md:e7b1f6a5d4c3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7 would be posted as a comment]
