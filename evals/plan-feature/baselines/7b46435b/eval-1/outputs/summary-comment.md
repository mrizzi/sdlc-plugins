# Plan Summary: TC-9001 -- Add advisory severity aggregation endpoint

## Tasks Created

| # | Task | Type |
|---|---|---|
| 1 | Create advisory severity summary model and aggregation service | Implementation |
| 2 | Implement advisory-summary REST endpoint with caching | Implementation |
| 3 | Add cache invalidation to advisory ingestion pipeline | Implementation |
| 4 | Write integration tests for advisory-summary endpoint | Implementation |
| 5 | Update REST API reference documentation | Documentation |
| 6 | Smoke Tests -- advisory severity aggregation | Testing |
| 7 | Performance Benchmarks -- advisory severity aggregation | Testing |

**Total**: 7 tasks (4 implementation, 1 documentation, 2 testing)

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Primary -- model, service, endpoint, ingestion pipeline, tests, and documentation |

## Architecture Summary

The feature adds a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the existing SBOM module following the established `model/ + service/ + endpoints/` pattern. The implementation layers are:

1. **Model** (`AdvisorySeveritySummary` struct) -- defines the response shape with severity counts
2. **Service** (`SbomService::advisory_severity_summary`) -- executes a SeaORM aggregation query joining `sbom_advisory` and `advisory` entities, deduplicating by advisory ID, with optional severity threshold filtering
3. **Endpoint** -- Axum handler with 5-minute tower-http cache, 404 for missing SBOMs, optional `?threshold` query param
4. **Cache invalidation** -- advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) invalidates cached summaries when new SBOM-advisory links are created

No new database tables are required; the feature uses the existing `sbom_advisory` join table and `advisory` entity.

## Inherited Fields

- **Priority**: Major (inherited from TC-9001)
- **Fix Versions**: RHTPA 1.5.0 (inherited from TC-9001)

Both values are set on the feature and propagated to all task `additional_fields`.
