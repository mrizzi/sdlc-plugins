## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns up-to-date severity counts after new advisory data is ingested, preventing stale cache entries from showing outdated severity breakdowns.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-to-SBOM correlation step to clear cached summary for affected SBOMs

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where new advisories are linked to SBOMs via the `sbom_advisory` join table), add a cache invalidation call for each affected SBOM ID.
- The caching infrastructure uses `tower-http` caching middleware as noted in the repository's Key Conventions. Investigate how the existing cache layer exposes invalidation capabilities — this may involve a shared cache store that supports key-based eviction, or it may require sending cache-busting signals.
- If the cache infrastructure uses an in-memory store or Redis, invalidate by constructing the cache key for the advisory-summary endpoint (e.g., keyed by SBOM ID) and explicitly evicting it.
- If `tower-http` caching relies purely on HTTP cache headers without a backing store, invalidation may need to use a version counter or ETag-based approach. Inspect the existing cache setup to determine the correct approach.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the SBOM ingestion pattern to understand how the ingestion pipeline is structured and how post-ingestion side effects are handled.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before modifying (constraint 5.2), do not duplicate existing functionality (constraint 5.4).

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Contains the advisory ingestion and correlation logic where invalidation must be inserted
- `modules/ingestor/src/graph/sbom/mod.rs` — Shows the ingestion pipeline pattern and post-ingestion processing steps
- `modules/ingestor/src/service/mod.rs::IngestorService` — May contain shared utilities for post-ingestion operations

## Acceptance Criteria
- [ ] After advisory ingestion links new advisories to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated severity counts
- [ ] Cache invalidation only targets affected SBOMs, not all cached summaries globally
- [ ] No regression in advisory ingestion performance or correctness

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify the advisory-summary endpoint reflects the updated counts without waiting for cache expiry
- [ ] Integration test: verify that cache invalidation targets only the affected SBOM and does not invalidate unrelated SBOM summaries

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
