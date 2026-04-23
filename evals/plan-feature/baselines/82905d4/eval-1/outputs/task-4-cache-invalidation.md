## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, any cached advisory-summary responses for that SBOM are invalidated. This ensures that the 5-minute cache does not serve stale severity counts after new advisory data is ingested.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add a cache invalidation call after the step that correlates/links advisories to SBOMs. When an advisory is stored and linked to one or more SBOMs, emit a cache invalidation signal for each affected SBOM's advisory-summary cache key.

## Implementation Notes
- The advisory ingestion flow is in `modules/ingestor/src/graph/advisory/mod.rs`. Locate the point where the ingestion pipeline calls the correlation step (linking an advisory to SBOMs via the `sbom_advisory` join table in `entity/src/sbom_advisory.rs`). After that step completes, add the invalidation logic.
- The caching approach uses tower-http cache-control headers (Cache-Control: max-age=300). For server-side invalidation, there are two strategies:
  1. **If using an in-process cache layer** (e.g., a shared `HashMap` or `moka` cache): remove the cache entry keyed by the SBOM ID.
  2. **If relying purely on HTTP cache headers**: the invalidation is implicit (responses expire after 5 minutes). In this case, the task reduces to ensuring the cache TTL is short enough and documenting that staleness of up to 5 minutes is acceptable.
- Check the existing caching infrastructure in the codebase. If there is a shared cache service or cache store, inject it into the ingestor and call its invalidation method. If not, consider adding a lightweight cache store (e.g., `moka::sync::Cache` or `dashmap::DashMap`) shared between the endpoint and the ingestor via Axum state.
- Reference `modules/ingestor/src/service/mod.rs` (IngestorService) for how dependencies are injected into the ingestion pipeline.
- Reference `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (from Task 3) to ensure the same cache key format is used for both caching and invalidation.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion flow; the invalidation hook attaches here
- `modules/ingestor/src/service/mod.rs::IngestorService` — Pattern for dependency injection into the ingestion pipeline

## Acceptance Criteria
- [ ] After advisory ingestion links a new advisory to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to GET /api/v2/sbom/{id}/advisory-summary after ingestion return updated counts (not stale cached values)
- [ ] Invalidation targets only the affected SBOM(s), not all cached summaries
- [ ] No performance regression in the advisory ingestion pipeline (invalidation is a lightweight operation)
- [ ] `cargo check -p trustify-module-ingestor` passes

## Test Requirements
- [ ] Integration test that ingests an SBOM, queries advisory-summary (expect zero counts), ingests an advisory linked to the SBOM, then queries advisory-summary again and verifies updated non-zero counts
- [ ] Test that ingesting an advisory linked to SBOM-A does not invalidate the cache for SBOM-B
- [ ] Test that the ingestion pipeline completes successfully with the invalidation logic added (no regressions)

## Verification Commands
- `cargo check -p trustify-module-ingestor` — compiles without errors
- `cargo test -p trustify-module-ingestor advisory` — ingestion tests pass
- `cargo test advisory_summary` — end-to-end cache invalidation test passes

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (the cache being invalidated must exist first)
