# Repository Impact Map

**Feature:** TC-9001 — Add advisory severity aggregation endpoint

## trustify-backend

changes:
  - Add `AdvisorySeveritySummary` response model struct for the aggregation endpoint
  - Add service method to `SbomService` that queries advisory-SBOM relationships, deduplicates by advisory ID, and aggregates severity counts
  - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache configuration
  - Register the new endpoint route in the SBOM endpoints module
  - Support optional `?threshold=critical` query parameter to filter severity counts (non-MVP)
  - Invalidate cached advisory summaries when advisory ingestion links new advisories to an SBOM
  - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature is entirely additive within a single repository — it introduces a new endpoint without modifying existing API contracts, database schema, or cross-repository dependencies. Each task can be merged independently without leaving `main` in a broken state.
