# Impact Map: TC-9001 -- Add advisory severity aggregation endpoint

## Repository: trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` | `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Handler for `GET /api/v2/sbom/{id}/advisory-summary` with caching and threshold filtering |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_severity_summary` and re-export `AdvisorySeveritySummary` |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `advisory_severity_summary()` method: query `sbom_advisory` joined with `advisory`, group by severity, count distinct advisory IDs, return `AdvisorySeveritySummary` |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register `GET /api/v2/sbom/{id}/advisory-summary` route with 5-minute cache-control |
| `modules/ingestor/src/graph/advisory/mod.rs` | Add cache invalidation call after advisory-to-SBOM correlation commits |
| `tests/api/sbom.rs` | Add 8 integration tests: severity counting, deduplication, 404 handling, threshold filtering, cache headers |

### Entity References (read-only, not modified)

| File | Relevance |
|---|---|
| `entity/src/sbom_advisory.rs` | Join table queried for advisory-SBOM relationships |
| `entity/src/advisory.rs` | Advisory entity with severity column used in aggregation |
| `entity/src/sbom.rs` | SBOM entity used for existence check (404 handling) |
| `common/src/error.rs` | `AppError` enum used for error responses |
| `common/src/db/query.rs` | Shared query helpers potentially reused for aggregation query |

### API Surface Changes

- **New endpoint**: `GET /api/v2/sbom/{id}/advisory-summary`
  - Response: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - Optional query param: `?threshold=critical|high|medium|low`
  - Cache: `Cache-Control: max-age=300`
  - Errors: 404 (SBOM not found), 400 (invalid threshold value)

### Task Dependency Graph

```
Task 1 (model)
  |
  v
Task 2 (service query)
  |
  v
Task 3 (endpoint + caching)
  |         |
  v         v
Task 4    Task 5
(threshold) (cache invalidation)
  |         |
  +----+----+
       |
       v
  Task 6 (integration tests)
```
