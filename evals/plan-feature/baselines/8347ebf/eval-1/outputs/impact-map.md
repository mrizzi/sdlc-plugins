# Repository Impact Map — TC-9001: Add Advisory Severity Aggregation Endpoint

## trustify-backend

### changes:
- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in the SBOM model module
- Add `advisory_summary` service method to `SbomService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, groups by severity, and returns counts
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache TTL using `tower-http` caching middleware
- Register the new endpoint route in the SBOM endpoints module
- Add cache invalidation logic in the advisory ingestion pipeline to invalidate cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests for the new endpoint covering: successful aggregation, 404 for nonexistent SBOM, correct deduplication, and cache behavior
- Add optional `threshold` query parameter support for filtering severity counts (non-MVP)
