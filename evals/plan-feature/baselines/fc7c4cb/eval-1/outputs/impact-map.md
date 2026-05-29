# Repository Impact Map — TC-9001

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. This feature adds a new endpoint to a single repository (trustify-backend) without breaking existing APIs, coordinated schema migrations, or cross-repository dependencies. Each task can be merged independently without leaving `main` in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct to represent aggregated severity counts
    - Add service method to SbomService that queries advisory-SBOM relationships and aggregates severity counts with deduplication
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache configuration
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Register the new endpoint route in SBOM endpoints module
    - Add cache invalidation hook in advisory ingestion pipeline for SBOM advisory summaries
    - Add integration tests for the new endpoint covering success, 404, caching, and threshold filtering
    - Update API documentation to include the new endpoint
```
