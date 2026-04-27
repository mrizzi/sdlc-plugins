# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## trustify-backend

### changes

- Add `AdvisorySeveritySummary` response model struct with fields `critical`, `high`, `medium`, `low`, `total` in `modules/fundamental/src/sbom/model/`
- Add `get_advisory_severity_summary` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that queries the `sbom_advisory` join table, joins with `advisory` to read severity, deduplicates by advisory ID, and aggregates counts by severity level
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/` with route registration in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Configure 5-minute response caching on the advisory-summary endpoint using `tower-http` caching middleware
- Add cache invalidation hook in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate cached advisory summaries when new advisories are linked to an SBOM during advisory ingestion
- Support optional `?threshold=critical` query parameter on the new endpoint to filter severity counts at or above the specified threshold (non-MVP)
- Add integration tests for the new endpoint in `tests/api/sbom.rs` covering: successful aggregation, 404 for nonexistent SBOM, deduplication of advisories, cache behavior, and threshold query parameter filtering
- Update `README.md` to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint path, parameters, and response shape
