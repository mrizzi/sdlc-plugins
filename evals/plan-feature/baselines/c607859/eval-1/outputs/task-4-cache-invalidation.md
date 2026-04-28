# Task 4 — Add cache invalidation for advisory summaries

## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint could serve stale severity counts after new advisories are correlated with an SBOM.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are linked to SBOMs during ingestion

## Implementation Notes
- The advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`) is responsible for parsing, storing, and correlating advisories. When the ingestion pipeline links a new advisory to an SBOM (via the `sbom_advisory` join table), it must invalidate the cached advisory summary for that SBOM.
- Investigate the existing caching infrastructure used by `tower-http` in the server setup (`server/src/main.rs`). Determine whether cache invalidation is done via:
  - Cache key eviction through a shared cache store (e.g., in-memory cache with `moka` or similar)
  - Cache-busting headers or versioned ETags
  - A cache invalidation service or signal mechanism
- Follow whichever pattern is already established in the codebase. If no programmatic cache invalidation pattern exists, consider adding a lightweight cache store that supports key-based eviction, keyed by SBOM ID.
- The invalidation must happen within the same database transaction as the advisory-SBOM linking to ensure consistency.
- Per constraints doc section 5.1: changes must be scoped to files listed; do not modify unrelated ingestion logic.
- Per constraints doc section 5.2: inspect the advisory ingestion code before modifying it.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline where the invalidation hook needs to be added
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline, may contain similar cache invalidation patterns if any exist
- `server/src/main.rs` — Axum server setup, likely contains the `tower-http` cache configuration

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory summary for that SBOM is invalidated
- [ ] Cache invalidation happens within the same transaction as the advisory-SBOM linking
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] Existing advisory ingestion behavior is not broken

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, verify that the advisory summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: verify that ingesting an advisory for SBOM A does not invalidate the cache for SBOM B

## Verification Commands
- `cargo build -p trustify-ingestor` — should compile without errors
- `cargo test -p trustify-ingestor advisory` — ingestion tests should pass

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint
