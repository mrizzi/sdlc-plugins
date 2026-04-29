# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Description
Expose the license compliance report as a REST endpoint nested under the existing SBOM routes. The endpoint calls the LicenseReportService from Task 2 and returns a JSON response with packages grouped by license and compliance flags.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/license-report` route in the existing SBOM router
- `modules/fundamental/src/license_report/mod.rs` — re-export the endpoint module

## Files to Create
- `modules/fundamental/src/license_report/endpoints/mod.rs` — route handler for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report for the specified SBOM. Response shape: `{ sbom_id: string, groups: [{ license: string, packages: [{ name: string, version: string, purl: string | null }], compliant: bool }], generated_at: string }`

## Implementation Notes
- Follow the endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs`:
  - Extract the SBOM `{id}` path parameter using Axum extractors
  - Obtain a database connection from the application state
  - Call `LicenseReportService::generate_report(id, &db)` 
  - Return the `LicenseReport` as JSON with `StatusCode::OK`
  - Return `AppError::NotFound` if the SBOM ID does not exist (check by attempting to fetch the SBOM first, or handle the service error)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as existing routes (e.g., `get.rs`, `list.rs`)
- Error handling: all handlers return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping, following the pattern in `common/src/error.rs`
- The endpoint does not require pagination since it returns a single report per SBOM. Do not use `PaginatedResults<T>` here

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow this handler pattern for path parameter extraction and response formatting
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — existing error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON license report
- [ ] Response body matches the documented shape: `{ sbom_id, groups: [{ license, packages, compliant }], generated_at }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Route is properly registered and accessible through the Axum router

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct report structure
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with packages having non-compliant licenses shows `compliant: false` in the response

## Dependencies
- Depends on: Task 2 — Add license report model and service
