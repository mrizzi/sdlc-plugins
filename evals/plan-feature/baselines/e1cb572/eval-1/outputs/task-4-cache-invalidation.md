# Task 4: Add cache invalidation for advisory summaries in advisory ingestion pipeline

## Repository
trustify-backend

## Target Branch
main

## Description
Modify the advisory ingestion pipeline to invalidate cached advisory severity summaries when new advisories are linked to an SBOM. Without cache invalidation, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale severity counts for up to 5 minutes after new advisories are correlated with an SBOM. This task ensures that cached responses are purged whenever the advisory-to-SBOM relationship changes during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call after the step where an advisory is linked to an SBOM via the `sbom_advisory` join table. Invalidate the cached advisory summary for each affected SBOM ID.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — extract the cache key generation logic (if not already shared) so the ingestor can reference the same key pattern used by the advisory-summary route's `tower-http` cache layer

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the section where the ingestion pipeline inserts rows into the `sbom_advisory` join table (correlating an advisory with one or more SBOMs). After each successful insert, emit a cache invalidation for the affected SBOM's advisory-summary endpoint.
- The `tower-http` caching middleware uses the request URI as the cache key. The invalidation must target the key pattern `/api/v2/sbom/{sbom_id}/advisory-summary`. If the cache layer exposes a programmatic purge API, call it directly. If not, implement invalidation by storing a per-SBOM version counter or timestamp in a shared state (e.g., `Arc<DashMap<Uuid, Instant>>`) that the endpoint checks before serving a cached response.
- Reference the existing ingestion flow in `modules/ingestor/src/graph/sbom/mod.rs` to understand how the SBOM ingestion pipeline structures its database writes -- the advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` follows a similar pattern.
- Use the `entity::sbom_advisory` entity from `entity/src/sbom_advisory.rs` to identify which SBOM IDs are affected when an advisory is linked.
- Wrap any new error paths with `.context()` using `AppError` from `common/src/error.rs`, consistent with the existing error handling in the ingestor module.
- Cache invalidation failures should log a warning but not fail the advisory ingestion pipeline (graceful degradation).
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` service files scope.
- Per Key Conventions §Caching: uses `tower-http` caching middleware; cache configuration in endpoint route builders. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint cache configuration scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion pipeline; add invalidation after SBOM-advisory linkage step
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion pipeline structure and how shared state is accessed
- `modules/fundamental/src/sbom/endpoints/mod.rs` — cache configuration for the advisory-summary route; may need to expose cache key or shared invalidation state
- `entity/src/sbom_advisory.rs` — entity for the SBOM-advisory join table, used to identify affected SBOM IDs
- `common/src/error.rs::AppError` — error type for consistent error handling

## Acceptance Criteria
- [ ] Advisory ingestion pipeline invalidates cached advisory summary for each SBOM linked to a newly ingested advisory
- [ ] Cache invalidation targets only the affected SBOM IDs, not all cached advisory summaries globally
- [ ] After ingestion of a new advisory linked to an SBOM, the next `GET /api/v2/sbom/{id}/advisory-summary` call returns updated counts (not stale cached data)
- [ ] Error during cache invalidation does not prevent advisory ingestion from completing (invalidation failure is logged but non-fatal)
- [ ] Existing advisory ingestion behavior is preserved -- no regressions in advisory storage or correlation

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent `GET /api/v2/sbom/{id}/advisory-summary` call reflects the new advisory in its counts
- [ ] Integration test: ingest an advisory linked to multiple SBOMs, verify that cached summaries for all affected SBOMs are invalidated
- [ ] Integration test: verify that advisory ingestion succeeds even when cache invalidation encounters an error (non-fatal behavior)

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor -- graph::advisory` — advisory ingestion tests pass
- `cargo check -p trustify-fundamental` — compiles without errors (if endpoint module was modified)

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint handler and route registration

---

> [sdlc-workflow] Description digest: sha256-md:d4a7f8c39e6b218064g3d9a57c8eb1f34h1dcg15g7e94380fba6c52d7g0e9143
