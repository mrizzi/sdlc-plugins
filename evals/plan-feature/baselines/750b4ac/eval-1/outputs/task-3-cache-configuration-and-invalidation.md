# Task 3 — Add cache configuration for advisory-summary endpoint and cache invalidation in advisory ingestion

## Repository
trustify-backend

## Target Branch
main

## Description
Configure 5-minute response caching for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint using the existing `tower-http` caching middleware. Additionally, add cache invalidation logic in the advisory ingestion pipeline so that cached summaries are cleared when new advisories are linked to an SBOM, ensuring data freshness.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add tower-http cache configuration (5-minute TTL) to the advisory-summary route handler or route builder
- `modules/fundamental/src/sbom/endpoints/mod.rs` — apply caching middleware layer to the advisory-summary route if cache is configured at the route level
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation logic when new advisories are correlated with SBOMs

## Implementation Notes
- Per the repo conventions, caching uses `tower-http` caching middleware with cache configuration in endpoint route builders. Apply the same caching pattern used by other endpoints in the SBOM module.
- Set the cache TTL to 300 seconds (5 minutes) as specified in the requirements.
- For cache invalidation in `modules/ingestor/src/graph/advisory/mod.rs`: when the advisory ingestion pipeline links a new advisory to an SBOM (via the `sbom_advisory` join table), invalidate the cached advisory-summary response for that SBOM. Follow the existing ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` (parse, store, correlate) to identify the correct insertion point.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the SBOM ingestion pattern to understand how the ingestion pipeline is structured and where correlation happens.
- The invalidation mechanism depends on the specific caching infrastructure — if using in-memory cache, clear the relevant cache key; if using HTTP cache headers, ensure the endpoint sets appropriate `Cache-Control` headers and the invalidation updates a version/ETag.
- Per CONVENTIONS.md §Caching: uses tower-http caching middleware; cache configuration in endpoint route builders.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration with caching middleware; reference for how tower-http cache layers are applied to routes
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion pipeline; locate the correlation step where advisories are linked to SBOMs
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for ingestion structure and patterns

## Acceptance Criteria
- [ ] The advisory-summary endpoint response is cached for 5 minutes
- [ ] Subsequent requests within the 5-minute window return the cached response
- [ ] When the advisory ingestion pipeline links new advisories to an SBOM, the cached advisory-summary for that SBOM is invalidated
- [ ] After cache invalidation, the next request returns fresh data reflecting the newly linked advisories

## Test Requirements
- [ ] Integration test verifying that repeated requests within the cache window return consistent results without re-querying
- [ ] Integration test verifying that cache is invalidated when new advisories are ingested and linked to an SBOM

## Verification Commands
- `cargo build` — project compiles without errors
- `cargo test` — all existing tests continue to pass

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint and route registration

[sdlc-workflow] Description digest: sha256-md:2b9bc73290f40a38822323d6ae3a4b3e35244aaa00064cfdcbf87ed9adab982c
