# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

### Workflow Mode: `direct-to-main`

**Rationale:** No atomicity constraints identified. All changes are confined to a single repository (`trustify-backend`) and can be merged independently without leaving `main` in a broken state. There are no coordinated schema migrations, no breaking API changes, no cross-cutting refactors, and no tightly coupled cross-repo components.

---

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model for severity count aggregation
    - Add severity aggregation query method to SbomService using sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional ?threshold query param
    - Add cache invalidation in advisory ingestion pipeline when advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
```
