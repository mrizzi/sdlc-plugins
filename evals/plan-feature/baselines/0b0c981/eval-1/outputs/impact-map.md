# Repository Impact Map

## Feature: TC-9001 — Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct to the SBOM model module
    - Add severity aggregation query method to `SbomService` that counts advisories by severity using the `sbom_advisory` join table
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 404 handling for missing SBOMs
    - Register the new endpoint route in the SBOM endpoints module
    - Add 5-minute cache configuration to the new endpoint route
    - Add cache invalidation call in the advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add optional `?threshold` query parameter support to filter severity counts
    - Add integration tests for the new endpoint covering success, 404, caching, and threshold filtering scenarios

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes are additive — a new endpoint, a new model struct, a new service method, and new tests. No existing API contracts are modified, no database schema changes are required (the endpoint uses existing `sbom_advisory` join table), and no cross-cutting refactors are needed. Each task can land on `main` independently without leaving the codebase in a broken state.
