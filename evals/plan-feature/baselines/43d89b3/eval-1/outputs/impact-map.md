# Repository Impact Map

## Feature: TC-9001 — Add advisory severity aggregation endpoint

### Workflow Mode

**direct-to-main** — No atomicity indicators identified. Each task can be merged independently without leaving `main` in a broken state. The model and service layers are additive (new struct, new method), the endpoint is a new route that does not modify existing endpoints, cache invalidation is an additive hook in the ingestion pipeline, and tests are self-contained.

---

### Impact Map

```
trustify-backend:
  changes:
    - Add SeveritySummary model struct to the SBOM model module
    - Add severity aggregation query method to SbomService using existing sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache TTL
    - Add cache invalidation for advisory summaries in the advisory ingestion pipeline
    - Add integration tests for the advisory-summary endpoint covering success, 404, deduplication, and threshold filter scenarios
```
