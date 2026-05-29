# Repository Impact Map — TC-9001

## trustify-backend

**Changes:**

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total`
- Add service method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table, deduplicates by advisory ID, and aggregates counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that validates SBOM existence (404 if not found), calls the service method, and returns the summary
- Register the new endpoint route in the SBOM endpoints module with 5-minute `tower-http` cache configuration
- Add optional `?threshold` query parameter support to filter severity counts above a given level (non-MVP)
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: success response shape, 404 for unknown SBOM, deduplication of advisories, cache behavior, and threshold filtering

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes are confined to a single repository (`trustify-backend`). The feature adds a new endpoint without modifying existing API contracts (no breaking changes). No database schema migrations are required — the implementation uses the existing `sbom_advisory` join table and `advisory` entity. No cross-cutting refactors are needed. Each task can be merged independently into `main` without leaving the codebase in a broken state.
