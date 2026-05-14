# Implementation Plan for TC-9201

## Task Summary

Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## New Endpoint

`GET /api/v2/sbom/{id}/advisory-summary` -- returns `{ critical: N, high: N, medium: N, low: N, total: N }`

## Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New `SeveritySummary` response struct with fields for each severity level and total.

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`. Extracts path param, calls service, returns JSON.

3. **`tests/api/advisory_summary.rs`** -- Integration tests covering: valid SBOM with known advisories, non-existent SBOM (404), SBOM with no advisories (all zeros), and deduplication of advisory links.

## Files to Modify

4. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module and re-export the struct.

5. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table for a given SBOM ID, joins to fetch advisory severity, deduplicates by advisory ID, counts per severity level, and returns a `SeveritySummary`.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`.

## Files Not Modified

- **`server/src/main.rs`** -- No changes needed; routes auto-mount via module registration.

## Cross-Section Reference Consistency

- Entity `AdvisoryService`: referenced in both "Files to Modify" (`modules/fundamental/src/advisory/service/advisory.rs`) and "Implementation Notes" (`modules/fundamental/src/advisory/service/advisory.rs`) -- paths are consistent.
- Entity `AdvisorySummary`: referenced in "Implementation Notes" (`modules/fundamental/src/advisory/model/summary.rs`) -- this is a read-only reference to extract the `severity` field pattern; the new struct is in a separate file (`severity_summary.rs`).
- Entity `sbom_advisory`: referenced in "Implementation Notes" (`entity/src/sbom_advisory.rs`) -- consistent with repo structure.

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `id` from path (Axum `Path<Id>`) -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table filtered by SBOM ID -> join with advisory table to get severity -> deduplicate by advisory ID -> count per severity level -> construct `SeveritySummary` -> return as JSON -- **COMPLETE**

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

## Implementation Order

1. Create `SeveritySummary` model struct (file-1)
2. Register model module in `model/mod.rs` (file-4)
3. Add `severity_summary` service method to `AdvisoryService` (file-5)
4. Create endpoint handler (file-2)
5. Register route in `endpoints/mod.rs` (file-6)
6. Write integration tests (file-3)
7. Run `cargo test` and fix any failures
8. Verify acceptance criteria
9. Self-verification checks (scope, secrets, duplication)
10. Commit and push
