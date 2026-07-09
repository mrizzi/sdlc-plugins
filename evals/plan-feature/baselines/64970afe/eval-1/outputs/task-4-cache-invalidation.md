## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory summaries are cleared when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint may serve stale severity counts for up to 5 minutes after new advisory data is ingested. This fulfills the non-functional requirement from feature TC-9001 that advisory ingestion must invalidate cached summaries.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisory-SBOM correlation step

## Implementation Notes
- In the advisory ingestion flow (`modules/ingestor/src/graph/advisory/mod.rs`), locate the code path where advisories are correlated with SBOMs (the parse, store, correlate sequence).
- After the correlation step completes, invalidate the cached advisory summary for all SBOM IDs affected by the newly linked advisories.
- Inspect how existing caching and invalidation patterns work in the codebase — check `modules/ingestor/src/graph/sbom/mod.rs` for any patterns where SBOM ingestion triggers cache-related operations.
- If the `tower-http` cache layer does not support key-specific invalidation, consider implementing an application-level caching strategy (e.g., using `moka` or `cached` crate) for the advisory summary that supports targeted invalidation by SBOM ID.
- Ensure invalidation is scoped to affected SBOMs only — do not clear the entire cache or invalidate summaries for unrelated SBOMs.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion flow that may contain existing cache invalidation patterns to follow
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion flow where the invalidation call will be inserted
- `modules/ingestor/src/service/mod.rs::IngestorService` — ingestion service that orchestrates the ingestion pipeline

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated severity counts without waiting for cache expiry
- [ ] Cache invalidation is scoped to affected SBOMs only — unrelated SBOM caches remain intact

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, then verify the summary endpoint returns updated counts without waiting for cache TTL
- [ ] Integration test: verify that ingesting an advisory for SBOM A does not invalidate the cached summary for SBOM B

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
