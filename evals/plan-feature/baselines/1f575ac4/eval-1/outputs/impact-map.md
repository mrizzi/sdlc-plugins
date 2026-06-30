# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### trustify-backend

**Changes:**

- Add `AdvisorySeveritySummary` response model struct with fields: `critical`, `high`, `medium`, `low`, `total` (in `modules/fundamental/src/sbom/model/`)
- Add service method to `SbomService` that queries the `sbom_advisory` join table, joins to `advisory` to get severity, deduplicates by advisory ID, and aggregates counts by severity level (in `modules/fundamental/src/sbom/service/`)
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the service method, returns the summary or 404 if SBOM not found (in `modules/fundamental/src/sbom/endpoints/`)
- Register the new endpoint route in the SBOM endpoint module's route configuration (in `modules/fundamental/src/sbom/endpoints/mod.rs`)
- Add 5-minute `tower-http` cache configuration for the new endpoint
- Add cache invalidation hook in advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM (in `modules/ingestor/src/graph/advisory/mod.rs`)
- Add optional `?threshold` query parameter support to filter severity counts above a given threshold
- Add integration tests for the new endpoint covering: successful summary response, 404 for non-existent SBOM, deduplication of advisories, threshold filtering, and cache behavior (in `tests/api/`)

### Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This is a single-repository, additive feature — a new endpoint with no breaking API changes, no coordinated schema migrations, and no cross-cutting refactors. Each task can land on `main` independently without leaving the codebase in a broken state.
