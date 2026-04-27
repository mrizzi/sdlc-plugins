# Task 4 — Add cache invalidation for advisory-summary on advisory ingestion

## Repository
trustify-backend

## Description
Ensure that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM during the advisory ingestion pipeline. Without cache invalidation, the severity summary could show stale counts for up to 5 minutes after new advisories are correlated, which is unacceptable for security-sensitive dashboards. This task modifies the advisory ingestion flow to clear the cached summary for affected SBOMs.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisories are linked to an SBOM during advisory ingestion/correlation

## Implementation Notes
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step (where `sbom_advisory` rows are inserted), add a call to invalidate the cached advisory-summary for each affected SBOM ID.
- Identify the exact location in the advisory ingestion flow where SBOM-advisory links are created. The invalidation call should happen immediately after successful insertion of these links.
- Cache invalidation approach depends on the project's caching infrastructure. Investigate how `tower-http` caching is configured in the project:
  - If using an in-memory cache layer (e.g., `tower-http`'s `CacheLayer`), there may not be a direct programmatic invalidation API — in that case, consider switching to an application-level cache (e.g., a shared `HashMap` with TTL or a `moka` cache) that supports explicit key removal.
  - If using an external cache (Redis, etc.), invalidate the key corresponding to the SBOM's advisory-summary.
  - At minimum, if programmatic invalidation is not feasible with the current caching setup, document this limitation and ensure the 5-minute TTL provides acceptable staleness bounds.
- Per `docs/constraints.md` §5.2: Inspect `modules/ingestor/src/graph/advisory/mod.rs` before modifying to understand the ingestion flow, the correlation step, and where SBOM IDs are available.
- Per `docs/constraints.md` §5.1: Only modify the files listed — do not refactor unrelated ingestion logic.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic; the invalidation point is where SBOM-advisory links are created
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module for reference on how ingestion modules are structured and whether cache invalidation patterns already exist

## Acceptance Criteria
- [ ] After new advisories are linked to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent GET requests to `/api/v2/sbom/{id}/advisory-summary` after ingestion return updated counts
- [ ] No regression in advisory ingestion performance or behavior

## Test Requirements
- [ ] Integration test: Ingest a new advisory linked to an SBOM, verify that the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Integration test: Verify that cache invalidation only affects the specific SBOM(s) linked to the new advisory, not all cached summaries

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
