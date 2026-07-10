# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## trustify-backend

### Changes
- Add `AdvisorySeveritySummary` model struct in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: critical, high, medium, low, total
- Add `pub mod advisory_summary` and re-export in `modules/fundamental/src/sbom/model/mod.rs`
- Add `get_advisory_summary` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` that aggregates severity counts from `sbom_advisory` join table with deduplication by advisory ID
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` with optional `?threshold` query parameter
- Register the new route with 5-minute tower-http cache in `modules/fundamental/src/sbom/endpoints/mod.rs`
- Add cache invalidation in `modules/ingestor/src/graph/advisory/mod.rs` to invalidate advisory-summary cache when new advisories are correlated to an SBOM
- Add integration tests in `tests/api/sbom_advisory_summary.rs` covering success, 404, threshold filtering, deduplication, and zero-advisory scenarios

## Workflow Mode

**direct-to-main** — No atomicity indicators identified. Each task can be merged independently:
- The model and service method (Task 1) are new additions with no breaking impact on existing code
- The endpoint (Task 2) depends on Task 1 but can be merged after Task 1 without breaking main
- Cache invalidation (Task 3) is an additive change to the ingestion pipeline
- Integration tests (Task 4) validate the new endpoint after it exists

## Inherited Fields

- **Priority**: Major (propagated to all created tasks)
- **fixVersions**: RHTPA 1.5.0 (propagated to all created tasks — fixVersion scope defaults to "both" since no `### Jira Field Defaults` section exists in CLAUDE.md)

### Task Creation Fields

All tasks are created with the following `additional_fields`:

```
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
