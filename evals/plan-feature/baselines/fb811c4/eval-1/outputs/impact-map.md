# Impact Map — TC-9001: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary struct to modules/fundamental/src/sbom/model/ with fields for critical, high, medium, low, and total counts
    - Add advisory_summary service method to SbomService in modules/fundamental/src/sbom/service/sbom.rs that queries the sbom_advisory join table, groups by severity, and returns aggregated counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler in modules/fundamental/src/sbom/endpoints/ with optional threshold query parameter
    - Register the new advisory-summary route in modules/fundamental/src/sbom/endpoints/mod.rs
    - Add 5-minute cache configuration to the advisory-summary route using tower-http caching middleware
    - Add cache invalidation hook in modules/ingestor/src/graph/advisory/mod.rs to invalidate cached severity summaries when new advisories are linked to an SBOM
    - Add integration tests for the advisory-summary endpoint in tests/api/sbom.rs covering success, 404, caching, and threshold filtering scenarios
