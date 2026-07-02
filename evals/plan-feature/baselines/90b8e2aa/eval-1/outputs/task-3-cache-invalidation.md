## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory-summary responses are invalidated when new advisories are linked to an SBOM. Without this, the `GET /api/v2/sbom/{id}/advisory-summary` endpoint would serve stale severity counts for up to 5 minutes after new advisories are correlated, which could mislead alerting integrations that poll for critical advisories.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after the advisory correlation step (where advisories are linked to SBOMs), add cache invalidation logic that clears or marks stale the cached advisory-summary response for the affected SBOM IDs

## Implementation Notes
- Identify the point in the advisory ingestion flow where advisories are linked to SBOMs. This is in `modules/ingestor/src/graph/advisory/mod.rs`, in the correlation step that creates entries in the `sbom_advisory` join table.
- The cache invalidation approach depends on the existing caching infrastructure. Since the codebase uses tower-http caching middleware (HTTP-level caching), the most appropriate strategy is likely one of:
  1. **Cache-busting via ETag or Last-Modified headers** — track the last advisory ingestion timestamp per SBOM and include it in the response headers, so that tower-http's conditional request handling serves fresh data after ingestion.
  2. **In-memory cache store invalidation** — if the caching layer uses an in-memory store (e.g., `tower-http::services::SetResponseHeader` wrapping a moka or similar cache), invalidate the specific SBOM's entry by key.
  3. **Cache TTL is sufficient** — if the 5-minute TTL is acceptable for the use case, document this as a known limitation rather than implementing active invalidation.
- Inspect the existing caching setup in the endpoint handlers and `server/src/main.rs` to determine which approach fits. The non-functional requirements state "cache invalidation: advisory ingestion pipeline must invalidate cached summaries when new advisories are linked to an SBOM," so active invalidation is required.
- After correlation, collect the list of affected SBOM IDs and invalidate their cache entries. Avoid invalidating all cached summaries — only the SBOMs that received new advisory links.
- Per CONVENTIONS.md §Error Handling: wrap cache invalidation operations with `.context()` so failures produce descriptive error messages without crashing the ingestion pipeline. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's .rs file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion and correlation logic; the cache invalidation hook must be inserted after the correlation step
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; used during correlation to determine which SBOMs are affected

## Acceptance Criteria
- [ ] When new advisories are linked to an SBOM via the ingestion pipeline, the cached advisory-summary for that SBOM is invalidated
- [ ] Cache invalidation is scoped to the affected SBOM IDs only — other cached summaries are not impacted
- [ ] Cache invalidation failures are logged but do not crash the advisory ingestion pipeline
- [ ] After ingestion of a new advisory, a subsequent call to `GET /api/v2/sbom/{id}/advisory-summary` returns updated counts

## Test Requirements
- [ ] Integration test: ingest a new advisory for an SBOM, then verify that the advisory-summary endpoint returns updated counts (not stale cached data)
- [ ] Test: cache invalidation failure is handled gracefully without blocking advisory ingestion

## Verification Commands
- `cargo build -p ingestor` — compiles without errors
- `cargo test -p ingestor` — all existing and new tests pass

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint (the cache must exist before invalidation can be tested)

---
[sdlc-workflow] Description digest: sha256-md:a0883631d9deb7cf911388f601132d3eec6bb0334bbb1637c02c3d29326df901
