# Repository Impact Map — TC-9001

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature adds a new, purely additive
REST endpoint within a single repository. No coordinated schema migrations, no breaking API
changes, no cross-cutting refactors, and no tightly coupled multi-repo components. Each task
can be merged independently without leaving `main` in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add severity aggregation query to SbomService that joins sbom_advisory and advisory tables, groups by severity, and deduplicates by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache and optional ?threshold query param
    - Register the new advisory-summary route in the SBOM endpoints module
    - Add cache invalidation hook in advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
```
