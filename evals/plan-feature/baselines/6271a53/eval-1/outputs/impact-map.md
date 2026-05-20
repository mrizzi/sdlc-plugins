# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend

**changes:**
- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the SBOM model module
- Add service method on `SbomService` to query the `sbom_advisory` join table, join with `advisory` to read severity, deduplicate by advisory ID, and aggregate counts per severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that validates SBOM existence (404 if missing), calls the service method, and returns the summary
- Register the new route in the SBOM endpoints module with 5-minute `tower-http` cache configuration
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Add optional `?threshold` query parameter support to filter severity counts (non-MVP)
- Add integration tests for the new endpoint covering: success case, 404 for missing SBOM, cached response, and threshold filtering
- Update API documentation to include the new endpoint path, parameters, and response shape

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The feature adds a single new endpoint to a single repository with no cross-repo dependencies, no breaking API changes to existing endpoints, no coordinated schema migrations, and no tightly coupled frontend-backend delivery requirement. Each task can be merged independently without leaving `main` in a broken state.
