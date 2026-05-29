# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. Each task can be merged independently without leaving `main` in a broken state:
- The new model struct is additive and does not break existing code.
- The new service method is additive and does not modify existing service interfaces.
- The new endpoint is a new route; existing endpoints are unaffected.
- Cache invalidation in the ingestor is a standalone change to an existing pipeline step.
- No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components exist across tasks.

### Impact Map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct in the SBOM model module
    - Add service method on SbomService to aggregate advisory severity counts for a given SBOM using the sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and route registration
    - Add optional ?threshold query parameter to filter severity counts above a given level
    - Add cache invalidation for advisory-summary in the advisory ingestion pipeline
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, threshold filtering, and deduplication
    - Update API documentation (README) to include the new endpoint
```
