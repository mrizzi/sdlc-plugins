# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with fields: critical, high, medium, low, total
    - Add advisory severity aggregation service method to SbomService that queries the sbom_advisory join table, deduplicates by advisory ID, groups by severity, and returns aggregated counts
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint handler with 5-minute cache-control header and 404 handling for missing SBOMs
    - Register the new advisory-summary route in the SBOM endpoints module
    - Add cache invalidation logic in the advisory ingestion pipeline when new advisories are linked to an SBOM
    - Add optional ?threshold query parameter to filter severity counts above a given severity level (non-MVP)
    - Add integration tests for the advisory-summary endpoint covering: happy path with correct counts, 404 for non-existent SBOM, deduplication of advisories, and threshold filtering

## New Files

- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary response struct with Serialize derive
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Service method to query and aggregate severity counts from sbom_advisory join table
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — GET /api/v2/sbom/{id}/advisory-summary endpoint handler
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Modified Files

- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service method
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the advisory-summary route alongside existing SBOM routes
- `modules/ingestor/src/graph/advisory/mod.rs` — Add cache invalidation logic after advisory-SBOM correlation step
- `tests/Cargo.toml` — Add new test file to the test suite if needed

## Referenced Files (pattern reference)

- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for single-SBOM endpoint handler with ID path parameter and 404 handling
- `modules/fundamental/src/sbom/service/sbom.rs` — Pattern for SbomService method structure and database query patterns
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct with severity field; reference for severity enum/type
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; used for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field
- `common/src/error.rs` — AppError enum for 404 and other error responses
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `common/src/model/paginated.rs` — PaginatedResults wrapper (not used here, but reference for response patterns)
- `server/src/main.rs` — Route mounting point for all modules
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests; pattern reference for test structure
- `tests/api/advisory.rs` — Advisory endpoint integration tests; pattern reference
