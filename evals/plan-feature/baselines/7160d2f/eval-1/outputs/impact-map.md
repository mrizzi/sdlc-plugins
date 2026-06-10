# Repository Impact Map — TC-9001

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. This feature is contained within a single repository (trustify-backend) and introduces a new additive endpoint with no breaking API changes, no coordinated schema migrations, and no cross-repo dependencies. Each task can be merged independently to `main` without leaving the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct for severity count aggregation
    - Add service method on SbomService to query and aggregate advisory severity counts by SBOM ID, with deduplication by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and 404 handling for missing SBOMs
    - Add optional ?threshold query parameter to filter severity counts (non-MVP)
    - Add cache invalidation in advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
    - Update REST API documentation to include the new endpoint
```
