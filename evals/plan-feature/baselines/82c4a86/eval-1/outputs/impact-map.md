# Repository Impact Map — TC-9001

## trustify-backend

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct to represent aggregated severity counts
    - Add severity aggregation query method to AdvisoryService that counts unique advisories per severity for a given SBOM
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional threshold query param
    - Add cache invalidation hook in advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
    - Update REST API documentation (README.md) to document the new endpoint
```
