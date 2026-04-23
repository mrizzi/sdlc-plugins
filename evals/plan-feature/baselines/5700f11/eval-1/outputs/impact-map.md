# Repository Impact Map

**Feature**: TC-9001 — Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct with fields for critical, high, medium, low, and total counts
    - Extend `SbomService` with an aggregation method that queries the `sbom_advisory` join table grouped by severity
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with 5-minute cache configuration
    - Add optional `?threshold` query parameter to filter severity counts above a given level
    - Update advisory ingestion in the ingestor module to invalidate cached advisory summaries when new advisories are linked to an SBOM
    - Add integration tests for the new endpoint covering success, 404, caching, and threshold filtering
