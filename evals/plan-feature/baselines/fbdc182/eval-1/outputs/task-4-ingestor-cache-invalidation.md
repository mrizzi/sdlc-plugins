## Repository
trustify-backend

## Description
When the advisory ingestion pipeline correlates a new advisory to an SBOM (i.e., writes a new row to the `sbom_advisory` join table), any cached `advisory-summary` response for that SBOM becomes stale. This task adds cache invalidation logic to the advisory ingestor so that the cached summary is evicted immediately after a new advisory-SBOM link is created, ensuring consumers receive up-to-date counts within one request cycle rather than waiting up to 5 minutes.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — after inserting into `sbom_advisory`, call the cache invalidation helper for the affected SBOM IDs

## Implementation Notes
The advisory ingestion entry point is in `modules/ingestor/src/graph/advisory/mod.rs`. The correlation step (linking an advisory to one or more SBOMs) results in inserts to the `entity::sbom_advisory` table. Locate the section that performs these inserts and add invalidation after the insert succeeds.

Cache invalidation approach — choose based on what `tower-http` cache infrastructure is already in place:

**Option A — Shared in-memory cache (most likely):** If the cache is an in-memory store (e.g., `dashmap::DashMap` or similar) held in `AppState`, inject it into `IngestorService` (via the same `State`/`Extension` pattern used elsewhere) and call `.remove(&cache_key)` where the cache key is derived from the SBOM ID (e.g., `format!("advisory-summary:{sbom_id}")`). Confirm the cache key format by inspecting how the endpoint in Task 3 stores values.

**Option B — HTTP-layer cache with surrogate keys:** If the cache is a reverse-proxy or HTTP-layer cache that supports surrogate key purging (e.g., a custom `SurrogateKey` header), emit a purge request after the insert.

Regardless of option, the invalidation must cover every SBOM ID that was correlated in the current ingestion batch, not just the first. Collect all affected SBOM IDs from the insert loop and invalidate each.

Error handling: cache invalidation failure must not abort the ingestion transaction. Wrap the invalidation call in a `if let Err(e) = ... { tracing::warn!("failed to invalidate cache: {e}"); }` block so ingestion remains resilient.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing insert logic for `sbom_advisory` rows; add invalidation immediately after the successful insert
- `modules/ingestor/src/service/mod.rs::IngestorService` — service struct; extend its fields if a cache handle needs to be threaded through
- `entity/src/sbom_advisory.rs` — join entity; confirms the column names for the insert being instrumented

## Acceptance Criteria
- [ ] After ingesting an advisory correlated to SBOM `X`, a subsequent call to `GET /api/v2/sbom/X/advisory-summary` returns updated counts (not a cached stale response)
- [ ] Ingestion does not fail or roll back if cache invalidation encounters an error
- [ ] Invalidation is applied to all SBOM IDs affected in a single ingestion run, not just the first
- [ ] `cargo check -p ingestor` passes with no warnings

## Test Requirements
- [ ] Integration test: ingest an SBOM, then ingest an advisory correlated to it, then call the summary endpoint — assert the count reflects the newly ingested advisory
- [ ] Integration test: simulate a cache invalidation error (e.g., poisoned mutex / dropped channel) — assert ingestion still returns success

## Dependencies
- Depends on: Task 3 — Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with caching
