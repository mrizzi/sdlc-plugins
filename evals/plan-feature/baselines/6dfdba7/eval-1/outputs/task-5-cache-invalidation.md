## Repository
trustify-backend

## Description
Ensure that cached advisory summary responses are invalidated when new advisories are ingested and linked to an SBOM. The advisory ingestion pipeline in the ingestor module correlates advisories with SBOMs; after this correlation step, any cached summary for the affected SBOM(s) must be invalidated. This satisfies the TC-9001 non-functional requirement that advisory ingestion invalidates cached summaries.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After the advisory-to-SBOM correlation step, trigger cache invalidation for affected SBOM IDs. This may involve calling a cache-busting mechanism or publishing an invalidation event.

## Implementation Notes
- Examine `modules/ingestor/src/graph/advisory/mod.rs` to understand the advisory ingestion flow. Look for where advisory-SBOM relationships are created (likely inserting into the `sbom_advisory` join table via `entity/src/sbom_advisory.rs`).
- The invalidation strategy depends on how `tower-http` caching is configured:
  1. **If using HTTP-level caching only** (Cache-Control headers with no server-side cache): The 5-minute TTL is self-invalidating, and no explicit invalidation is needed. In this case, this task becomes documenting that the 5-minute staleness window is acceptable.
  2. **If there is a server-side cache layer** (e.g., an in-memory cache or Redis): Add an explicit invalidation call after SBOM-advisory linking. This would be a method call like `cache.invalidate(format!("advisory-summary:{}", sbom_id))`.
- If the codebase uses only HTTP Cache-Control headers (most likely given the `tower-http` convention), then explicit invalidation is not needed, and this task should document the staleness window trade-off and add a comment in the ingestion code noting the dependency.
- Check `modules/ingestor/src/service/mod.rs` (`IngestorService`) for any existing cache invalidation patterns that can be followed.
- At minimum, add a code comment at the advisory correlation point in `modules/ingestor/src/graph/advisory/mod.rs` documenting that advisory summary caches have a 5-minute TTL and will be stale until expiry after new advisory ingestion.

## Acceptance Criteria
- [ ] Advisory ingestion code documents or implements cache invalidation for advisory summary
- [ ] If server-side caching exists, explicit invalidation is triggered when new advisory-SBOM links are created
- [ ] If only HTTP-level caching, the staleness window is documented and accepted as within requirements
- [ ] No regression in advisory ingestion functionality

## Test Requirements
- [ ] Test: after ingesting a new advisory linked to an SBOM, a subsequent call to the advisory summary endpoint reflects the new advisory (may require waiting for cache expiry or verifying invalidation)

## Verification Commands
- `cargo check -p trustify-ingestor` — should compile without errors

## Dependencies
- Depends on: Task 4 — Response caching (need to understand the caching mechanism before implementing invalidation)
