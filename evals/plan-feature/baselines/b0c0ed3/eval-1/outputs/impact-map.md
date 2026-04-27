# Repository Impact Map — TC-9001

## trustify-backend

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct with fields: critical, high, medium, low, total
    - Add advisory_summary method to SbomService that queries sbom_advisory join table, groups by severity, and returns aggregated counts with deduplication by advisory ID
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache configuration
    - Register the new advisory-summary route in the SBOM endpoints module
    - Add optional ?threshold query parameter support to filter severity counts (non-MVP)
    - Add cache invalidation hook in advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint covering: success with counts, 404 for missing SBOM, deduplication, threshold filtering, and cache behavior
    - Update API documentation to include the new endpoint
```
