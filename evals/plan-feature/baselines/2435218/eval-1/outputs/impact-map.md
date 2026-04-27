# Repository Impact Map — TC-9001: Add Advisory Severity Aggregation Endpoint

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model struct with severity count fields (critical, high, medium, low, total)
    - Add advisory severity aggregation query method to SbomService that counts unique advisories by severity using the sbom_advisory join table
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache and optional threshold query parameter
    - Add cache invalidation for advisory-summary when new advisories are linked to an SBOM during advisory ingestion
    - Add integration tests for the advisory-summary endpoint covering success, 404, caching, and threshold filtering
    - Update API documentation to include the new advisory-summary endpoint
```

## Affected Modules

| Module | Files | Change Type |
|---|---|---|
| `modules/fundamental/src/sbom/model/` | New `advisory_summary.rs`, modify `mod.rs` | New model struct |
| `modules/fundamental/src/sbom/service/` | Modify `sbom.rs`, modify `mod.rs` | New service method |
| `modules/fundamental/src/sbom/endpoints/` | New `advisory_summary.rs`, modify `mod.rs` | New endpoint + route registration |
| `modules/ingestor/src/graph/advisory/` | Modify `mod.rs` | Cache invalidation on ingest |
| `tests/api/` | New `sbom_advisory_summary.rs`, modify `Cargo.toml` if needed | Integration tests |

## Reuse Candidates

- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field for grouping
- `common/src/error.rs` — `AppError` enum for 404 handling (consistent with existing SBOM endpoints)
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct includes severity field; reference for severity enum/type
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET endpoint as pattern reference for 404 handling and route structure
- `common/src/db/query.rs` — shared query builder helpers for building the aggregation query
