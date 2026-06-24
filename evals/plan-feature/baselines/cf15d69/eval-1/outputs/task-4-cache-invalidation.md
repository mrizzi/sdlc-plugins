## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures the severity counts endpoint always reflects the latest advisory data after ingestion completes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after advisory-SBOM correlation step to evict cached advisory-summary entries for affected SBOM IDs

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the advisory ingestion pipeline parses, stores, and correlates advisories with SBOMs. After the correlation step (where entries are written to the `sbom_advisory` join table represented by `entity/src/sbom_advisory.rs`), collect the affected SBOM IDs and invalidate their cached advisory-summary responses.

Follow the existing caching patterns described in Key Conventions. The `tower-http` caching middleware uses HTTP cache semantics, so invalidation should be done by either: (a) sending a cache-bust header on responses after ingestion, (b) using an explicit cache store eviction if available, or (c) tagging cached responses with SBOM-specific keys and invalidating by key. Examine the existing cache configuration patterns in endpoint route builders to determine the appropriate invalidation mechanism.

Per Key Conventions (Caching): Uses `tower-http` caching middleware; cache configuration in endpoint route builders. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's caching scope.

Per Key Conventions (Error handling): All functions return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` files scope.

## Acceptance Criteria
- [ ] Advisory ingestion invalidates cached advisory-summary for all SBOM IDs affected by newly linked advisories
- [ ] Cache invalidation does not break existing ingestion flow
- [ ] Invalidation only affects advisory-summary cache entries, not other cached responses
- [ ] No new database tables are introduced for cache management

## Test Requirements
- [ ] Integration test: ingest advisory, verify cached summary is stale and next request returns updated counts
- [ ] Test that ingestion of an advisory not linked to any SBOM does not trigger unnecessary invalidation

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor graph::advisory` — advisory ingestion tests pass

## Dependencies
- Depends on: Task 3 — advisory summary endpoint (cache must exist before it can be invalidated)

[sdlc-workflow] Description digest: sha256-md:9532af4b74705944baa8f39d9e00b4ba5dd3329a2d2f60b90164cc8ced7729e2
