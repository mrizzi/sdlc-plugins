# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that invokes the `LicenseReportService` and returns the license compliance report as JSON. Register the route in the SBOM endpoints module and mount it in the server.

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON object containing packages grouped by license with compliance flags

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `server/src/main.rs` — ensure the SBOM module routes (which already include the new route via `endpoints/mod.rs`) are mounted (likely already mounted; verify)

## Implementation Notes
- Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler) — it demonstrates path parameter extraction, service invocation, and JSON response construction.
- The handler should:
  1. Extract `id` from the path using Axum's `Path` extractor
  2. Obtain the `LicenseReportService` from the application state (Axum's `State` extractor)
  3. Call `generate_report(id)` on the service
  4. Return `Json(report)` on success or `AppError` on failure
- Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the existing pattern — add `.route("/api/v2/sbom/:id/license-report", get(license_report))` alongside the existing SBOM routes.
- Return `Result<Json<LicenseReport>, AppError>` following the error handling convention from `common/src/error.rs`.
- Consider caching: if the SBOM data is static after ingestion, the report can be cached using the `tower-http` caching middleware pattern noted in the repo conventions.
- Per constraints doc section 5.1: changes must be scoped to the files listed above — no unrelated files.
- Per constraints doc section 5.3: follow the endpoint patterns referenced in these notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the exact pattern for path parameter extraction and JSON response for SBOM endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates list endpoint pattern with `PaginatedResults` (not needed here but useful reference for route registration)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — the route registration file to extend

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport` body for a valid SBOM ID
- [ ] The response JSON contains `groups` array with `license`, `packages`, and `compliant` fields
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 404 when the SBOM ID does not exist
- [ ] The route is registered and accessible when the server starts
- [ ] Code compiles without errors (`cargo build`)

## Test Requirements
- [ ] Handler unit test: valid SBOM ID returns 200 with correct response shape
- [ ] Handler unit test: non-existent SBOM ID returns 404

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint listing

## Dependencies
- Depends on: Task 3 — Add LicenseReportService for compliance report generation
