# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add severity aggregation query method to SbomService that counts advisories by severity from the sbom_advisory join table, deduplicating by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler returning severity counts with 404 for missing SBOMs
    - Register the new advisory-summary route in the SBOM endpoints module
    - Configure 5-minute tower-http cache for the advisory-summary endpoint
    - Add cache invalidation in the advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add optional ?threshold query parameter to filter severity counts above a given level (non-MVP)
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
    - Update API documentation (README.md) to document the new endpoint

## Workflow Mode

**Mode:** direct-to-main

**Rationale:** No atomicity indicators are present. All changes are in a single repository (trustify-backend). The new endpoint is purely additive — it does not modify existing API contracts, does not require coordinated schema migrations (no new tables), and does not break any existing functionality if landed incrementally. Each task's PR can merge to main independently.
