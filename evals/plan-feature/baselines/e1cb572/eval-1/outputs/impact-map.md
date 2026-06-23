# Repository Impact Map: TC-9001

## Feature

**TC-9001**: Add advisory severity aggregation endpoint

## Repository

trustify-backend

## Workflow Mode

direct-to-main -- The feature is purely additive (new endpoint, model, service logic, tests). No existing behavior is modified in a breaking way. Each task can land on `main` independently.

## Impact Summary

### New Files

| File Path | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | New `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `?threshold` query param |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the new endpoint |

### Modified Files

| File Path | Change Description |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_summary;` to export the new model |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `advisory_severity_summary` method to `SbomService` that queries `sbom_advisory` join table, joins to `advisory` for severity, groups and counts by severity level |
| `modules/fundamental/src/sbom/service/mod.rs` | Re-export the new service method if needed by module structure |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration |
| `modules/fundamental/src/sbom/mod.rs` | Ensure submodule exports are complete for new files |
| `modules/ingestor/src/graph/advisory/mod.rs` | Add cache invalidation call when new advisories are linked to an SBOM during advisory ingestion |
| `entity/src/sbom_advisory.rs` | Verify the entity has the necessary relations for severity aggregation queries (may need minor adjustments for the aggregation query) |
| `server/src/main.rs` | No change expected -- route auto-mounted via `endpoints/mod.rs` registration pattern |

### Entities Used (Read-Only)

| Entity File | Usage |
|---|---|
| `entity/src/sbom.rs` | SBOM entity lookup for 404 validation |
| `entity/src/advisory.rs` | Advisory entity for severity field access |
| `entity/src/sbom_advisory.rs` | Join table for SBOM-to-Advisory relationship |

### Shared Infrastructure Reused

| File Path | What Is Reused |
|---|---|
| `common/src/error.rs` | `AppError` enum for 404 and error responses |
| `common/src/db/query.rs` | Query builder helpers if needed for filtering |
| `common/src/model/paginated.rs` | Reference for response wrapper patterns (not used directly -- summary is not paginated) |

### Cache Infrastructure

| Aspect | Detail |
|---|---|
| Cache mechanism | `tower-http` caching middleware, configured in endpoint route builder |
| Cache duration | 5 minutes (300 seconds) |
| Cache invalidation | Advisory ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`) must invalidate cached summaries when new advisories are linked to an SBOM |

### API Surface Changes

| Method | Path | Change |
|---|---|---|
| `GET` | `/api/v2/sbom/{id}/advisory-summary` | NEW -- returns `{ critical, high, medium, low, total }` |
| `GET` | `/api/v2/sbom/{id}/advisory-summary?threshold={level}` | NEW -- filters counts to only include severities at or above the specified threshold |
