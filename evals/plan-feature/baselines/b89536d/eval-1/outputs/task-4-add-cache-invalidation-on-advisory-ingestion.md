# Task 4 -- Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisories are correlated with an SBOM, rather than serving stale cached counts.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- add cache invalidation call after advisory-to-SBOM correlation completes, targeting the advisory-summary cache entries for affected SBOM IDs

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs
- After the correlation step (where advisory-SBOM links are created in the `sbom_advisory` join table), identify which SBOM IDs were affected and invalidate their cached advisory summary responses
- The caching infrastructure uses `tower-http` caching middleware -- investigate the existing cache layer to determine the correct invalidation mechanism (e.g., cache key eviction, cache-busting headers, or an application-level cache store)
- If the cache uses an application-level cache store (e.g., an in-memory cache like `moka` or `cached`), call the eviction/invalidation method with the affected SBOM IDs
- If the cache is purely HTTP-level (`tower-http` response caching), consider implementing an application-level cache layer that can be explicitly invalidated, or use cache-busting strategies such as versioned cache keys
- Ensure invalidation is performed within the same transaction or after the transaction commits successfully -- do not invalidate cache for advisory links that might be rolled back
- Follow error handling patterns from the ingestor service in `modules/ingestor/src/service/mod.rs`

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- existing advisory ingestion and correlation logic where invalidation must be inserted
- `modules/ingestor/src/graph/sbom/mod.rs` -- sibling ingestion module for reference on post-ingestion hooks or event patterns

## Acceptance Criteria
- [ ] After new advisories are linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` return updated counts reflecting newly ingested advisories
- [ ] Cache invalidation does not affect advisory summaries for unrelated SBOMs
- [ ] Cache invalidation only occurs after the advisory-SBOM link transaction commits successfully

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that the advisory summary endpoint returns updated counts (not stale cached values)
- [ ] Integration test: ingest an advisory linked to SBOM-A, verify that SBOM-B's cached summary is not affected

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
