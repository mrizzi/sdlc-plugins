## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures the `GET /api/v2/sbom/{id}/advisory-summary` endpoint always returns current data after new advisories are ingested, fulfilling the non-functional requirement that advisory ingestion triggers cache invalidation.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- after correlating an advisory with an SBOM, call cache invalidation for the affected SBOM's advisory-summary key
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- expose a cache key generation function or constant that the ingestor can reference for invalidation

## Implementation Notes
The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where `entity/src/sbom_advisory.rs` join records are inserted), add a call to invalidate the cached advisory-summary for each affected SBOM ID.

The cache invalidation mechanism depends on how the tower-http caching layer is configured. Common approaches:
1. If using an in-memory cache (e.g., tower-http's built-in), expose a shared cache handle and call `.remove(key)` for the affected SBOM's advisory-summary cache key.
2. If using a cache key based on the request URI, the key will be `/api/v2/sbom/{sbom_id}/advisory-summary`.

Ensure the cache key used in the endpoint (Task 2) and the invalidation call here are consistent. Consider creating a shared helper function in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` like `advisory_summary_cache_key(sbom_id: Uuid) -> String` that both the endpoint and ingestor can reference.

The `IngestorService` in `modules/ingestor/src/service/mod.rs` may need an additional dependency (the cache handle) injected into its constructor.

Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` -- existing advisory correlation logic; the invalidation call should be placed directly after the SBOM-advisory link insertion
- `modules/ingestor/src/service/mod.rs::IngestorService` -- service struct that may need the cache handle added to its dependencies

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Cache invalidation only targets the specific SBOM(s) affected by the ingested advisory, not all cached summaries
- [ ] No regression in advisory ingestion performance

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify that `GET /api/v2/sbom/{id}/advisory-summary` reflects the updated count
- [ ] Test that ingesting an advisory linked to SBOM A does not invalidate the cache for SBOM B

## Verification Commands
- `cargo build -p trustify-ingestor` -- compiles without errors
- `cargo test -p trustify-ingestor` -- existing tests pass with no regressions

## Dependencies
- Depends on: Task 2 -- Implement advisory-summary REST endpoint with caching
