# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add severity aggregation query method to SbomService that joins sbom_advisory and advisory tables, groups by severity, and returns deduplicated counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with optional ?threshold query parameter
    - Add 5-minute cache layer to the advisory-summary endpoint using tower-http caching middleware
    - Add cache invalidation hook in advisory ingestion pipeline to clear cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering: success response, 404 for missing SBOM, severity deduplication, threshold filtering, cache behavior
    - Update API documentation to include the new endpoint path, parameters, and response shape
```
