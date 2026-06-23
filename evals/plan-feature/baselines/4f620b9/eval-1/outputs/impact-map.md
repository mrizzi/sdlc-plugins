# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct for severity count aggregation
    - Add service method to `SbomService` that queries the `sbom_advisory` join table and aggregates advisory counts by severity
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache and optional `?threshold` query parameter
    - Register the new endpoint route in the SBOM endpoints module
    - Add cache invalidation logic in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the new endpoint covering: success response, 404 for missing SBOM, severity counting correctness, deduplication by advisory ID, cache behavior, and threshold query parameter
    - Update API documentation to include the new endpoint

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes target a single repository (`trustify-backend`). There are no coordinated schema migrations (no new tables), no breaking API changes (this is a new additive endpoint), no cross-cutting refactors, and no tightly coupled cross-repo components. Each task can be merged independently without leaving `main` in a broken state.
