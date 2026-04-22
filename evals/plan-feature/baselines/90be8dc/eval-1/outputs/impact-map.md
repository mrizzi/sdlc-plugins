# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Feature Summary

Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM. Includes 5-minute caching and an optional `?threshold` query parameter for severity filtering.

## Impacted Areas

### New Files

| File | Change | Reason |
|---|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | CREATE | New `AdvisorySeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | CREATE | New Axum handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `?threshold` query param |
| `modules/fundamental/src/sbom/service/advisory_summary.rs` | CREATE | Service method to query `sbom_advisory` join table, join to `advisory` for severity, aggregate counts with deduplication by advisory ID |
| `tests/api/sbom_advisory_summary.rs` | CREATE | Integration tests for the new endpoint: happy path, 404 for missing SBOM, threshold filtering, caching behavior |

### Modified Files

| File | Change | Reason |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | MODIFY | Add `pub mod advisory_summary;` to expose the new model |
| `modules/fundamental/src/sbom/service/mod.rs` | MODIFY | Add `pub mod advisory_summary;` to expose the new service module |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | MODIFY | Register the `/api/v2/sbom/{id}/advisory-summary` route in the SBOM router |
| `modules/ingestor/src/graph/advisory/mod.rs` | MODIFY | Add cache invalidation call when new advisories are linked to an SBOM during ingestion |

### Referenced Files (read-only, patterns to follow)

| File | Relevance |
|---|---|
| `modules/fundamental/src/sbom/endpoints/get.rs` | Pattern for single-SBOM endpoint handler with path parameter extraction and 404 handling |
| `modules/fundamental/src/advisory/model/summary.rs` | `AdvisorySummary` struct contains the `severity` field to reference in aggregation |
| `entity/src/sbom_advisory.rs` | SeaORM entity for the SBOM-Advisory join table used in the aggregation query |
| `entity/src/advisory.rs` | Advisory entity with severity column |
| `common/src/error.rs` | `AppError` enum for consistent error responses (404 on missing SBOM) |
| `common/src/db/query.rs` | Query builder helpers for constructing the aggregation query |
| `tests/api/sbom.rs` | Pattern for SBOM integration tests to follow |

## Dependency Graph

```
Task 1: AdvisorySeveritySummary model
   |
   v
Task 2: Advisory summary service (aggregation query)
   |
   v
Task 3: Advisory summary endpoint + route registration
   |
   v
Task 4: Threshold query parameter support
   |
   v
Task 5: Cache integration and ingestion-time invalidation
   |
   v
Task 6: Integration tests
```

## Tasks

| # | Title | Dependencies |
|---|---|---|
| 1 | Define AdvisorySeveritySummary response model | None |
| 2 | Implement advisory severity aggregation service | Task 1 |
| 3 | Add advisory-summary endpoint and register route | Task 2 |
| 4 | Add threshold query parameter filtering | Task 3 |
| 5 | Add caching and cache invalidation on advisory ingestion | Task 3 |
| 6 | Add integration tests for advisory-summary endpoint | Task 3, Task 4, Task 5 |
