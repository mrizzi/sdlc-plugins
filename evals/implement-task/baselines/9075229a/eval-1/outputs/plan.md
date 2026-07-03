# Implementation Plan: TC-9201

## Task Summary
Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM.

## Repository
trustify-backend

## Target Branch
main

## Branch Name
TC-9201

## Files to Create

### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs`
New model struct `SeveritySummary` defining the response shape with fields for each severity level and a total count.

### File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
New GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the JSON response.

### File 3: `tests/api/advisory_summary.rs`
Integration tests covering: valid SBOM with known advisories, non-existent SBOM returns 404, SBOM with no advisories returns all zeros, and duplicate advisory deduplication.

## Files to Modify

### File 4: `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module.

### File 5: `modules/fundamental/src/advisory/service/advisory.rs`
Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table for a given SBOM ID, joins with advisory data to get severity levels, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

### File 6: `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))` following the existing pattern.

## Files Unchanged (confirmed)
- `server/src/main.rs` -- no changes needed (routes auto-mount via module registration).

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint returning `{ critical: N, high: N, medium: N, low: N, total: N }`.

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low) and total for all
advisories linked to the given SBOM. Deduplicates advisories by ID
and defaults missing severity levels to zero.

Implements TC-9201
```

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` request
  -> Axum extracts `id` from path via `Path<Id>`
  -> Handler calls `AdvisoryService::severity_summary(sbom_id, tx)`
  -> Service queries `sbom_advisory` join table filtered by `sbom_id`
  -> Service joins with `advisory` table to get severity field
  -> Service deduplicates by advisory ID (using `DISTINCT` or `HashSet`)
  -> Service counts by severity level, builds `SeveritySummary`
  -> Handler wraps result in `Json` and returns 200 OK
  -> On missing SBOM: returns 404 via `AppError` with `.context()`

**Status: COMPLETE** -- all stages connected from input to output.

## Cross-Section Reference Consistency
- Entity `AdvisoryService` -- consistent: both Files to Modify and Implementation Notes reference `modules/fundamental/src/advisory/service/advisory.rs`.
- Entity `SeveritySummary` -- consistent: Files to Create and Implementation Notes both reference the model module.
- Entity `sbom_advisory` join table -- consistent: Implementation Notes and entity directory both reference `entity/src/sbom_advisory.rs`.

## Acceptance Criteria Verification Plan
1. GET /api/v2/sbom/{id}/advisory-summary returns correct shape -- verified by integration test with known data.
2. Returns 404 for non-existent SBOM -- verified by dedicated 404 test.
3. Deduplicates by advisory ID -- verified by test inserting duplicate links.
4. Defaults to 0 for missing severity levels -- verified by empty SBOM test.
5. Response time under 200ms for up to 500 advisories -- ensured by single SQL query with GROUP BY (no N+1).
