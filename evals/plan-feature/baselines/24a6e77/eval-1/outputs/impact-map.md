# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## trustify-backend

### changes:
- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the SBOM model module
- Add aggregation query in `SbomService` that joins `sbom_advisory` with `advisory` table, groups by severity, deduplicates by advisory ID, and returns counts
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache configuration via `tower-http` caching middleware
- Support optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above a given severity level
- Return 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints
- Add cache invalidation hook in the advisory ingestion pipeline to invalidate cached summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: success with counts, 404 for missing SBOM, threshold filtering, deduplication of advisories, and cache behavior
- Update API documentation to include the new endpoint path, parameters, and response shape
