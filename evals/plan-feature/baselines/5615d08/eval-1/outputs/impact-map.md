trustify-backend:
  changes:
    - Add `AdvisorySeveritySummary` response model struct with severity count fields to `modules/fundamental/src/sbom/model/advisory_summary.rs`
    - Add `SeverityThreshold` enum for query parameter parsing to `modules/fundamental/src/sbom/model/advisory_summary.rs`
    - Export new model module from `modules/fundamental/src/sbom/model/mod.rs`
    - Add `advisory_summary` aggregation method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that queries `sbom_advisory` + `advisory` entities, deduplicates by advisory ID, and groups by severity
    - Add `invalidate_advisory_summary_cache` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`
    - Create `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`
    - Register the advisory-summary route in `modules/fundamental/src/sbom/endpoints/mod.rs`
    - Add 5-minute cache (`Cache-Control: max-age=300`) to the advisory-summary route via `tower-http` caching middleware
    - Add optional `?threshold=critical|high|medium|low` query parameter to filter severity counts at or above the specified level
    - Hook cache invalidation into advisory ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` to evict cached summaries when new advisories are linked to an SBOM
    - Add integration test module `tests/api/advisory_summary.rs` covering happy path, 404, deduplication, threshold filtering, cache headers, and invalidation behavior
