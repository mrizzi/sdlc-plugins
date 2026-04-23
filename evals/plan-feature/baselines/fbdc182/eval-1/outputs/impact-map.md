# Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Summary

Add `GET /api/v2/sbom/{id}/advisory-summary` to the `trustify-backend` service. The endpoint aggregates vulnerability advisory severity counts (Critical, High, Medium, Low) for a given SBOM server-side, returning a pre-computed summary. Results are cached for 5 minutes and the cache is invalidated when new advisories are linked to an SBOM via the ingestion pipeline.

## Repository: trustify-backend

### New Files

| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` | `AdvisorySeveritySummary` response struct with severity count fields |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Handler for `GET /api/v2/sbom/{id}/advisory-summary` |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the new endpoint |

### Modified Files

| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Re-export `AdvisorySeveritySummary` |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `advisory_severity_summary(sbom_id)` query method |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register `GET /api/v2/sbom/{id}/advisory-summary` route with 5-minute cache |
| `modules/ingestor/src/graph/advisory/mod.rs` | Invalidate cached advisory summary on advisory-SBOM correlation |
| `tests/Cargo.toml` | Add test module reference for `sbom_advisory_summary` |

### No Schema Changes

No new database tables or migrations are required. The aggregation query joins the existing `sbom_advisory` join table with the `advisory` entity using SeaORM.

## Task Breakdown

| Task | Title | Depends On |
|---|---|---|
| Task 1 | Add `AdvisorySeveritySummary` response model | — |
| Task 2 | Add `advisory_severity_summary` service method to `SbomService` | Task 1 |
| Task 3 | Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint with caching | Task 2 |
| Task 4 | Invalidate advisory summary cache in advisory ingestor | Task 3 |
| Task 5 | Add integration tests for the advisory summary endpoint | Task 3, Task 4 |
