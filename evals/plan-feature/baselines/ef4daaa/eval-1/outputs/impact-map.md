# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add service method to SbomService that queries sbom_advisory join table, joins advisory table, groups by severity, and returns deduplicated counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling for missing SBOM IDs
    - Register the new endpoint route in the SBOM endpoints module
    - Add 5-minute cache configuration to the advisory-summary endpoint using tower-http caching middleware
    - Add cache invalidation logic in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add optional ?threshold query parameter to filter severity counts (non-MVP)
    - Add integration tests for the advisory-summary endpoint covering: success response, 404 for missing SBOM, severity count correctness, deduplication, and cache behavior
    - Update API documentation to include the new endpoint
```
