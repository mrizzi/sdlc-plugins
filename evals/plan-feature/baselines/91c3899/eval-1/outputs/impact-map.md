# Repository Impact Map

## TC-9001: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields for critical, high, medium, low, and total counts
    - Add service method to aggregate advisory severity counts for a given SBOM, deduplicating by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling for missing SBOMs
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Configure 5-minute tower-http caching on the advisory-summary endpoint
    - Add cache invalidation logic in advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, deduplication, caching, and threshold filtering
    - Update API documentation to include the new endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. This feature adds a new endpoint to a single repository (trustify-backend) without breaking existing API contracts, requiring no coordinated schema migrations (no new database tables), no cross-repo dependencies (backend-only), and no cross-cutting refactors. Each task can be merged independently to main without leaving the codebase in an inconsistent state.
