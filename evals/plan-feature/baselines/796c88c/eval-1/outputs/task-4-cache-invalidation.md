## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory summaries are invalidated when new advisories are linked to an SBOM. When the ingestor correlates a new advisory to an SBOM, the cached summary for that SBOM must be evicted to ensure subsequent requests return fresh data.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — After advisory-SBOM correlation is persisted, emit a cache invalidation call for the affected SBOM IDs
- `modules/ingestor/src/service/mod.rs` — Wire the cache invalidation dependency into `IngestorService` if not already available

## Implementation Notes
- The advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Locate the point where `sbom_advisory` records are inserted (the correlation step) and add invalidation after that transaction commits.
- If the project uses `tower-http` cache layer with an in-memory cache (as indicated by repo conventions), invalidation may require either: (a) a shared cache handle injected into the ingestor, or (b) a TTL-based approach where the cache is short-lived enough that explicit invalidation is not strictly necessary but is added for correctness.
- Follow the existing dependency injection pattern in `IngestorService` at `modules/ingestor/src/service/mod.rs` to pass any required cache handle.
- Identify all SBOM IDs affected by the newly ingested advisory (there may be multiple) and invalidate each.
- Use `.context("invalidating advisory summary cache")` for error wrapping on the invalidation call.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Advisory ingestion and SBOM correlation logic where invalidation hooks should be added
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service struct showing dependency injection patterns for adding cache handle

## Acceptance Criteria
- [ ] When a new advisory is ingested and linked to an SBOM, the cached advisory summary for that SBOM is invalidated
- [ ] Invalidation covers all SBOMs affected by a single advisory ingestion (an advisory may relate to multiple SBOMs)
- [ ] Cache invalidation failures are logged but do not fail the ingestion transaction
- [ ] No regression in existing advisory ingestion behavior

## Test Requirements
- [ ] Test that ingesting an advisory triggers cache invalidation for affected SBOM summaries

## Verification Commands
- `cargo check -p trustify-ingestor` — compiles without errors
- `cargo test -p trustify-ingestor` — existing ingestor tests still pass

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (establishes the cache that needs invalidation)

## Applicable Conventions
- **Error handling**: Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.context()` error wrapping scope.

[sdlc-workflow] Description digest: sha256-md:f40da4b70ed8757bb8d79e401081f64cb1b2d20310b20ca7098faff37b7e221c
