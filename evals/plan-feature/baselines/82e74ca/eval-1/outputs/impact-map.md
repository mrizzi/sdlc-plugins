# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## trustify-backend

### changes

- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the SBOM model module
- Add service method on `SbomService` to query and aggregate advisory severity counts for a given SBOM ID, deduplicating by advisory ID, using the existing `sbom_advisory` join table and `advisory` entity
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the new service method, returns 404 if the SBOM ID does not exist, and supports an optional `?threshold` query parameter for severity filtering
- Register the new endpoint route in the SBOM endpoints module with 5-minute `tower-http` cache configuration
- Add cache invalidation logic in the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: successful aggregation, 404 for non-existent SBOM, deduplication, threshold filtering, and cache behavior
- Update API documentation to include the new endpoint path, parameters, and response shape
