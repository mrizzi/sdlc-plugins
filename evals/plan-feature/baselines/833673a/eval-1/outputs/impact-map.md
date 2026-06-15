# Repository Impact Map — TC-9001

## trustify-backend

- Add `AdvisorySeveritySummary` response model struct to the SBOM model layer (`modules/fundamental/src/sbom/model/`)
- Add severity aggregation query method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that joins `sbom_advisory` with `advisory` and groups by severity
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/` with 5-minute cache-control header via `tower-http` caching middleware
- Add optional `?threshold` query parameter support to filter severity counts above a given level
- Add cache invalidation hook in advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) to invalidate cached advisory summaries when new advisories are linked to an SBOM
- Add integration tests for the advisory-summary endpoint in `tests/api/sbom.rs` covering: successful aggregation, 404 for unknown SBOM, deduplication by advisory ID, threshold filtering, and cache behavior
