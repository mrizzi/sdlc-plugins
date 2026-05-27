# Repository Impact Map — TC-9001

## trustify-backend

Changes:
- Add `AdvisorySeveritySummary` response model struct with fields: critical, high, medium, low, total
- Add aggregation query method to `SbomService` that counts unique advisories by severity for a given SBOM ID using the `sbom_advisory` join table
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 404 handling for missing SBOMs
- Add 5-minute cache configuration on the new endpoint route using `tower-http` caching middleware
- Add optional `?threshold=critical` query parameter to filter severity counts above a given threshold
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Register the new endpoint route in the SBOM endpoint module
- Add integration tests for the new endpoint covering: successful aggregation, 404 for missing SBOM, cache behavior, and threshold filtering

## Workflow Mode Decision

**Selected mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. All changes are confined to a single repository (`trustify-backend`). There are no coordinated schema migrations (no new database tables required per non-functional requirements). There are no breaking API changes — this is a purely additive new endpoint. There are no cross-cutting refactors. The frontend is not in scope for this feature. Each task can be merged independently without leaving `main` in a broken state.
