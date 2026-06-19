# Impact Map — TC-9001: Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: critical, high, medium, low, total
    - Register new model module in `modules/fundamental/src/sbom/model/mod.rs`
    - Add `advisory_summary` service method to `SbomService` in `modules/fundamental/src/sbom/service/advisory_summary.rs` performing COUNT(DISTINCT advisory_id) GROUP BY severity via SeaORM join on `sbom_advisory` and `advisory` entities
    - Register new service module in `modules/fundamental/src/sbom/service/mod.rs`
    - Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` with Cache-Control max-age=300 header
    - Register new endpoint route in `modules/fundamental/src/sbom/endpoints/mod.rs`
    - Add cache invalidation hook in `modules/ingestor/src/graph/advisory/mod.rs` to evict cached advisory summaries when new advisories are correlated to SBOMs
    - Wire cache handle dependency into `IngestorService` in `modules/ingestor/src/service/mod.rs`
    - Add integration test module `tests/api/sbom_advisory_summary.rs` covering happy path, 404, empty advisories, deduplication, and cache header scenarios
