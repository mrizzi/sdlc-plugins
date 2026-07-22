# Impact Map: TC-9001 -- Add advisory severity aggregation endpoint

## Feature Summary

Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts (critical, high, medium, low, total) for a given SBOM, with 5-minute caching and optional severity threshold filtering.

## Inherited Fields

- **Priority**: Major (propagated from feature TC-9001 to all tasks)
- **Fix Versions**: RHTPA 1.5.0 (propagated from feature TC-9001 to all tasks)

## Repository Impact

| Repository | Impact |
|---|---|
| trustify-backend | Primary -- all implementation, testing, and documentation tasks target this repository |

## File Impact Summary

### New Files

| File | Task | Purpose |
|---|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | Task 1 | `AdvisorySeveritySummary` response struct and `SeverityThreshold` enum |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Task 3 | HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary` |
| `tests/api/sbom_advisory_summary.rs` | Task 5 | Integration tests for the advisory-summary endpoint |

### Modified Files

| File | Task | Change |
|---|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Task 1 | Add `pub mod advisory_summary` declaration and re-exports |
| `modules/fundamental/src/sbom/service/sbom.rs` | Task 2 | Add `get_advisory_summary` method to `SbomService` with aggregation query |
| `modules/fundamental/src/sbom/service/mod.rs` | Task 2 | Import advisory summary model types |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 3 | Register `/api/v2/sbom/{id}/advisory-summary` route |
| `modules/ingestor/src/graph/advisory/mod.rs` | Task 4 | Add cache invalidation call after advisory-SBOM linkage |

### Referenced Entities (Read-Only)

| File | Purpose |
|---|---|
| `entity/src/sbom.rs` | SBOM entity for existence check |
| `entity/src/advisory.rs` | Advisory entity with severity field for aggregation |
| `entity/src/sbom_advisory.rs` | Join table entity for SBOM-advisory relationships |
| `common/src/error.rs` | `AppError` enum for error handling |
| `common/src/db/query.rs` | Query builder helpers for SeaORM queries |

## API Changes

| Method | Path | Action |
|---|---|---|
| GET | `/api/v2/sbom/{id}/advisory-summary` | New endpoint -- returns severity counts |

## Task Dependency Graph

```
Task 1 (model)
  └── Task 2 (service)
        └── Task 3 (endpoint)
              ├── Task 4 (cache invalidation)
              ├── Task 5 (integration tests)
              └── Task 6 (documentation)

Tasks 1-5 (all implementation)
  ├── Task 7 (smoke tests)
  └── Task 8 (performance benchmarks)
```

## Task Summary

| Task | Title | Type | Dependencies |
|---|---|---|---|
| Task 1 | Add advisory severity summary response model | Implementation | None |
| Task 2 | Add advisory severity aggregation service method | Implementation | Task 1 |
| Task 3 | Add advisory-summary endpoint with caching | Implementation | Task 2 |
| Task 4 | Add cache invalidation for advisory summaries on ingestion | Implementation | Task 3 |
| Task 5 | Add integration tests for advisory-summary endpoint | Implementation | Task 3, Task 4 |
| Task 6 | Update REST API reference documentation | Documentation | Task 3 |
| Task 7 | Smoke tests | Testing | Tasks 1-5 |
| Task 8 | Performance benchmarks | Testing | Tasks 1-5 |

## Non-Functional Considerations

- **Performance**: p95 < 200ms for SBOMs with up to 500 advisories
- **Caching**: 5-minute TTL via `Cache-Control: max-age=300`; invalidated on advisory ingestion
- **Database**: No new tables; uses existing `sbom_advisory` join table with `advisory` severity field
- **Deduplication**: Advisories are counted uniquely by advisory ID to prevent double-counting
