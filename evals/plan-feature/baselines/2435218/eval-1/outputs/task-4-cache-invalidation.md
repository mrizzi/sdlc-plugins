# Task 4 — Add Cache Invalidation for Advisory-Summary on Advisory Ingestion

## Repository
trustify-backend

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that when new advisories are linked to an SBOM, the cached advisory-summary response for that SBOM is invalidated. This ensures that the 5-minute cache does not serve stale severity counts after new advisories are correlated with an SBOM.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — add cache invalidation call when advisories are linked to SBOMs during ingestion (in the advisory correlation step)

## Implementation Notes
- The advisory ingestion module in `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. The cache invalidation hook should be added at the point where an advisory is linked to an SBOM (i.e., after an `sbom_advisory` relationship is created or updated).
- Reference the caching infrastructure used by the endpoint (Task 3) to determine the appropriate invalidation mechanism. If `tower-http` cache is key-based, invalidate by constructing the cache key for `/api/v2/sbom/{sbom_id}/advisory-summary`.
- If the caching layer does not support targeted invalidation (e.g., it is a simple TTL-based HTTP cache), consider alternative approaches:
  1. Use a shared cache store (e.g., an in-memory cache or Redis) that the endpoint reads and the ingestor can clear by key.
  2. Add a version/generation counter to the SBOM entity that the endpoint checks against the cached version.
- Inspect the existing `IngestorService` in `modules/ingestor/src/service/mod.rs` for service injection patterns and how cross-module interactions are handled.
- Per constraints doc section 5.1: changes must be scoped to cache invalidation — do not modify the ingestion logic itself.
- Per constraints doc section 5.2: inspect ingestion code before modifying to understand the exact correlation step.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation logic; the hook point for invalidation
- `modules/ingestor/src/service/mod.rs::IngestorService` — service injection patterns for cross-module access

## Acceptance Criteria
- [ ] When a new advisory is linked to an SBOM during ingestion, the cached advisory-summary for that SBOM is invalidated
- [ ] Subsequent calls to `GET /api/v2/sbom/{id}/advisory-summary` after invalidation return fresh data
- [ ] Cache invalidation does not impact advisory ingestion performance (no blocking external calls)
- [ ] Ingestion of advisories not linked to any SBOM does not trigger unnecessary invalidation

## Test Requirements
- [ ] Integration test: ingest an advisory linked to an SBOM, verify that a subsequent advisory-summary request reflects the new advisory (not stale cached data)
- [ ] Integration test: ingest an advisory not linked to any SBOM, verify no cache invalidation occurs

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary Endpoint
