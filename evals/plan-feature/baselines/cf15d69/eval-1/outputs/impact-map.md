# Impact Map — TC-9001: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response struct in `modules/fundamental/src/sbom/model/` to represent `{ critical, high, medium, low, total }` counts
    - Add `advisory_summary` aggregation method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that queries `entity/src/sbom_advisory.rs` join table and groups by advisory severity
    - Add `advisory_summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/` implementing `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query param
    - Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` with `tower-http` caching middleware (5-minute TTL)
    - Mount the updated sbom routes in `server/src/main.rs` (verify existing mount covers new sub-route)
    - Add cache invalidation hook in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate advisory-summary cache when new advisories are linked to an SBOM
    - Add integration tests in `tests/api/sbom.rs` covering the new endpoint: success case, 404 for missing SBOM, threshold filtering, deduplication of advisory IDs
    - Extend error handling in `common/src/error.rs` if any new error variants are needed (e.g., invalid threshold parameter)
