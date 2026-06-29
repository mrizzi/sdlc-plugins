# Repository Impact Map — TC-9001: Add Advisory Severity Aggregation Endpoint

## Repository: trustify-backend

### New Files

| Path | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total |
| `modules/fundamental/src/sbom/service/advisory_summary.rs` | Service method to query and aggregate advisory severity counts for an SBOM |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | `GET /api/v2/sbom/{id}/advisory-summary` handler with optional `?threshold` query param and 5-minute cache |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the new endpoint |

### Modified Files

| Path | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_summary;` to expose the new model |
| `modules/fundamental/src/sbom/service/mod.rs` | Add `pub mod advisory_summary;` to expose the new service module |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Add `pub mod advisory_summary;` and register the new route in the router |
| `modules/fundamental/Cargo.toml` | No changes expected — existing dependencies should suffice |
| `modules/ingestor/src/graph/advisory/mod.rs` | Add cache invalidation call when new advisories are linked to an SBOM |
| `tests/Cargo.toml` | Add new test file to the test suite if needed |

### Entities Referenced (Read-Only)

| Path | Usage |
|---|---|
| `entity/src/sbom.rs` | SBOM entity for existence check (404 if not found) |
| `entity/src/advisory.rs` | Advisory entity — severity field used in aggregation |
| `entity/src/sbom_advisory.rs` | Join table linking SBOMs to advisories — primary query target |
| `common/src/error.rs` | `AppError` enum for error handling in the new handler |
| `common/src/db/query.rs` | Query builder helpers potentially reusable for the aggregation query |
| `common/src/model/paginated.rs` | Reference for response wrapper patterns (this endpoint uses a custom struct, not pagination) |

### Architecture Notes

- The new endpoint lives within the existing `sbom` module, following the established `model/ + service/ + endpoints/` module pattern.
- The aggregation query joins `sbom_advisory` with `advisory` to count distinct advisory IDs grouped by severity level.
- Caching uses the existing `tower-http` middleware pattern already established in route builders.
- Cache invalidation is triggered in the advisory ingestion pipeline when new SBOM-advisory links are created.
- The `?threshold` query parameter filters returned severity counts to only levels at or above the specified threshold.
