## Repository
trustify-backend

## Target Branch
main

## Description
Update the advisory ingestion pipeline to invalidate cached advisory-summary responses when new advisories are linked to an SBOM. This ensures the aggregation endpoint returns fresh severity counts after new advisory correlations are processed, preventing stale data from being served to dashboard consumers.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after the advisory-to-SBOM correlation step where `sbom_advisory` records are inserted

## Implementation Notes
- Identify the point in `modules/ingestor/src/graph/advisory/mod.rs` where advisories are correlated to SBOMs (i.e., where `entity::sbom_advisory` join records are created). Add cache invalidation logic immediately after this correlation step.
- Use the tower-http cache invalidation mechanism consistent with the existing caching infrastructure. If the caching layer uses an in-memory store, inject a cache handle and evict the key for `/api/v2/sbom/{id}/advisory-summary` for each affected SBOM ID.
- If no programmatic cache invalidation API is available from the tower-http layer, implement a cache version key pattern: maintain a version counter per SBOM (in the database or in-memory), increment it during ingestion, and include it in the cache key used by the endpoint. This ensures the next request generates a cache miss.
- Reference `modules/ingestor/src/service/mod.rs` (`IngestorService`) for understanding the ingestion pipeline flow and how services are passed to graph operations.
- Scope invalidation to only the affected SBOM IDs extracted from the newly created `sbom_advisory` records. Do not flush the entire cache.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust language scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion and correlation logic to extend
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service layer that orchestrates ingestion and may coordinate cache handles

## Acceptance Criteria
- [ ] Advisory ingestion invalidates cached advisory-summary for all affected SBOM IDs
- [ ] Cache invalidation occurs after successful advisory-to-SBOM correlation
- [ ] Fresh data is served on the next `GET /api/v2/sbom/{id}/advisory-summary` request after ingestion
- [ ] Invalidation is scoped to affected SBOM IDs only, not a global cache flush

## Test Requirements
- [ ] Integration test: ingest a new advisory linked to an SBOM, verify the cached summary is invalidated and the next request returns updated counts
- [ ] Verify that unrelated SBOM caches are not affected by the invalidation

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
