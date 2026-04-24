# Impact Map: TC-9001 — Add advisory severity aggregation endpoint

## Repository: trustify-backend

### Entity Layer (`entity/`)
- `entity/src/sbom_advisory.rs` — Existing SBOM-Advisory join table entity used for the aggregation query; no changes needed but is a key dependency for the query logic
- No new entities or migrations required (requirement: no new database tables)

### Common Module (`common/`)
- `common/src/model/mod.rs` — Add `AdvisorySeveritySummary` response struct with fields `critical`, `high`, `medium`, `low`, `total` (and re-export from `mod.rs`)

### Fundamental Module — SBOM (`modules/fundamental/src/sbom/`)
- `modules/fundamental/src/sbom/model/` — Add `advisory_summary.rs` containing the `AdvisorySeveritySummary` struct (alternatively place in the sbom model namespace)
- `modules/fundamental/src/sbom/model/mod.rs` — Re-export the new advisory summary model
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_severity_summary(&self, sbom_id: Uuid)` method to `SbomService` that queries the `sbom_advisory` join table joined with `advisory` to aggregate severity counts, deduplicating by advisory ID
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `GET /api/v2/sbom/{id}/advisory-summary` route with 5-minute cache-control header
- `modules/fundamental/src/sbom/endpoints/` — Add `advisory_summary.rs` handler that extracts the SBOM ID path parameter, calls the service method, and returns JSON or 404

### Ingestor Module (`modules/ingestor/`)
- `modules/ingestor/src/graph/advisory/mod.rs` — After advisory ingestion and SBOM correlation, invalidate cached advisory summary for affected SBOM IDs

### Integration Tests (`tests/`)
- `tests/api/sbom.rs` — Add integration tests for the new endpoint covering: success with counts, 404 for unknown SBOM, threshold query parameter filtering, deduplication of advisories

### Server (`server/`)
- `server/src/main.rs` — No changes expected if route registration is handled within `modules/fundamental/src/sbom/endpoints/mod.rs` (verify mounting pattern)

### Summary of Changes
| Area | Files Modified | Files Created |
|------|---------------|---------------|
| Model | 1 | 1 |
| Service | 1 | 0 |
| Endpoints | 1 | 1 |
| Ingestor | 1 | 0 |
| Tests | 1 | 0 |
| **Total** | **5** | **2** |
