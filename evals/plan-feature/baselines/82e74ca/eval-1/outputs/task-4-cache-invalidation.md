# Task 4 — Add cache invalidation for advisory summary on advisory ingestion

## Repository
trustify-backend

## Description
When new advisories are linked to an SBOM during the advisory ingestion pipeline, the cached advisory summary for that SBOM must be invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns up-to-date severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after advisories are correlated/linked to SBOMs

## Implementation Notes
- The advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. Identify the point where advisory-SBOM links are created (i.e., new rows inserted into the `sbom_advisory` join table).
- After the correlation step, invalidate the cached advisory summary for each affected SBOM ID. The invalidation mechanism depends on the caching infrastructure:
  - If `tower-http` cache is in-process and keyed by request path, invalidation may require a cache store reference or a signaling mechanism. Inspect the existing cache setup in `modules/fundamental/src/sbom/endpoints/mod.rs` to understand how caching is configured and what invalidation patterns exist.
  - If caching uses an external store (e.g., Redis), use the appropriate key pattern to delete the cached entry for `/api/v2/sbom/{sbom_id}/advisory-summary`.
- Follow the error handling patterns in the ingestor module — wrap errors with `.context()` per the `AppError` pattern in `common/src/error.rs`.
- Ensure invalidation does not fail the ingestion pipeline — cache invalidation failures should be logged but not cause the overall ingestion to error out.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and SBOM correlation logic; the invalidation call should be added adjacent to the correlation step
- `modules/fundamental/src/sbom/endpoints/mod.rs` — inspect how tower-http caching is configured to determine the correct invalidation approach

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation failures do not cause the advisory ingestion to fail
- [ ] Cache invalidation is logged for observability

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify the advisory summary endpoint returns updated counts reflecting the new advisory
- [ ] Integration test: verify that a cached response is no longer served after advisory ingestion adds new advisories to the SBOM

## Verification Commands
- `cargo build -p trustify-module-ingestor` — should compile without errors
- `cargo test --test api advisory_summary_invalidation` — cache invalidation tests should pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
