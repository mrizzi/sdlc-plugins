# Task 4 — Add cache invalidation for advisory severity summary on advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory severity summary for that SBOM is invalidated. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after new advisories are correlated with an SBOM, meeting the non-functional requirement that the advisory ingestion pipeline must invalidate cached summaries.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are correlated to SBOMs during ingestion; after the advisory-SBOM link is created, invalidate the cached advisory summary for the affected SBOM ID

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the point where SBOM-advisory links are created (where `sbom_advisory` join table entries are inserted) and add a cache invalidation call after the link is created.
- Use the existing `tower-http` cache infrastructure — reference how cache invalidation is done elsewhere in the codebase (if any patterns exist). If the caching layer uses a key-based cache, invalidate the cache key for the specific SBOM's advisory summary endpoint.
- If the caching middleware uses HTTP cache headers (passive caching), consider whether an active invalidation mechanism is needed or whether a shorter cache TTL is sufficient. The feature requirement specifies active invalidation on advisory ingestion.
- Ensure the invalidation is scoped to only the affected SBOM IDs, not a global cache flush.
- Use `.context()` wrapping for any error handling, consistent with `common/src/error.rs`.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — the advisory ingestion module where SBOM-advisory correlations are created; this is the exact location where cache invalidation should be triggered
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module; reference for ingestion pipeline patterns and how post-ingestion side effects are handled

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates the cached advisory severity summary for affected SBOMs when new advisories are linked
- [ ] Cache invalidation is scoped to the specific SBOM IDs affected, not a global cache flush
- [ ] Existing advisory ingestion behavior is unchanged (no regressions)
- [ ] Cache invalidation errors are handled gracefully (logged, not fatal to ingestion)

## Test Requirements
- [ ] Integration test: after ingesting a new advisory linked to an SBOM, verify that the advisory summary endpoint returns updated counts reflecting the new advisory
- [ ] Integration test: verify that cache invalidation only affects the target SBOM's summary, not other SBOMs' cached summaries
- [ ] Test that advisory ingestion completes successfully even if cache invalidation encounters an error

## Verification Commands
- `cargo build -p trustify-ingestor` — expected outcome: compiles without errors
- `cargo test --test api` — expected outcome: integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
