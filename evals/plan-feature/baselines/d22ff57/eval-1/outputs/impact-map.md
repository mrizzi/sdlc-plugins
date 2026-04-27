# Repository Impact Map — TC-9001

## Feature: Add advisory severity aggregation endpoint

---

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model struct to represent aggregated severity counts (critical, high, medium, low, total)
    - Add service method to SbomService that queries the sbom_advisory join table, deduplicates by advisory ID, and aggregates counts by severity level
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache, 404 handling for missing SBOMs, and optional ?threshold query parameter
    - Add cache invalidation for advisory-summary when new advisories are linked to an SBOM during advisory ingestion
    - Add integration tests for the new advisory-summary endpoint covering success, 404, deduplication, caching, and threshold filtering
```
