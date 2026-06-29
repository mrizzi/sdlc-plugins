## Repository
trustify-backend

## Target Branch
main

## Description
Add cache invalidation logic to the advisory ingestion pipeline so that cached advisory severity summaries are invalidated when new advisories are linked to an SBOM. This ensures that the `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns fresh data after advisory correlation updates.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation call after new SBOM-advisory relationships are created during advisory ingestion

## Implementation Notes
The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories with SBOMs. After the correlation step where new entries are inserted into the `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`), add a call to invalidate the cached advisory summary for the affected SBOM IDs.

The invalidation approach depends on the `tower-http` caching middleware configuration established in Task 3. Options include:
1. If using an in-memory cache layer, call the cache eviction API with the affected SBOM ID as the cache key.
2. If using HTTP cache headers only (no server-side cache store), no explicit invalidation is needed — the 5-minute TTL handles staleness. In this case, document this decision and verify the TTL is acceptable.
3. If a shared cache store exists (e.g., Redis), publish an invalidation message for the affected SBOM ID(s).

Identify the specific correlation function in `modules/ingestor/src/graph/advisory/mod.rs` that creates `sbom_advisory` records and add the invalidation call immediately after the insert succeeds. Collect all affected SBOM IDs from the newly created relationships.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and use `.context()` wrapping for any cache invalidation errors; do not let cache failures abort advisory ingestion.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Caching: follow the established `tower-http` caching patterns for invalidation.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory correlation logic where invalidation should be added
- `entity/src/sbom_advisory.rs` — join table entity to identify affected SBOM IDs

## Acceptance Criteria
- [ ] Cache invalidation is triggered after new SBOM-advisory relationships are created
- [ ] All affected SBOM IDs are collected from newly created relationships
- [ ] Cache invalidation failures are logged but do not abort advisory ingestion
- [ ] Invalidation approach is consistent with the caching mechanism used in Task 3

## Test Requirements
- [ ] Integration test verifying that after ingesting a new advisory linked to an SBOM, the advisory summary endpoint returns updated counts
- [ ] Test verifying that cache invalidation failure does not cause advisory ingestion to fail

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (establishes the caching mechanism to invalidate)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:1c1fa83e87a4110eb6136e915446f7edd4bde95c649e63d7b6240b0a82a18d3e
