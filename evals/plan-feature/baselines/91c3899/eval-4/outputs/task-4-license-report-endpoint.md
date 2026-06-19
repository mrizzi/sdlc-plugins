## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for a given SBOM. The endpoint calls the license report service (Task 3) and returns the result as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the new `/api/v2/sbom/{id}/license-report` route

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a `LicenseReport` JSON response with packages grouped by license type and compliance flags. Returns 404 if the SBOM ID does not exist. Returns 200 with the report on success.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` -- see `get.rs` for the `GET /api/v2/sbom/{id}` handler as a direct reference for path parameter extraction, service invocation, and response serialization.
- The handler should:
  1. Extract the SBOM `id` path parameter
  2. Call `SbomService::generate_license_report(id)` (from Task 3)
  3. Return `Ok(Json(report))` on success or propagate the `AppError`
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes.
- All handlers return `Result<T, AppError>` with `.context()` wrapping, consistent with `common/src/error.rs`.
- The route must be mounted under the existing SBOM route group so it shares the same middleware (auth, caching, etc.).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Existing GET handler for SBOM details; follow its exact pattern for path extraction and response
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Existing route registration; add the new route here
- `common/src/error.rs::AppError` -- Use existing error type; it implements `IntoResponse` for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseReport` for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 404 for a nonexistent SBOM ID
- [ ] Response content type is `application/json`
- [ ] Route is registered under the existing SBOM endpoint group

## Test Requirements
- [ ] Handler unit test: verify 200 response with expected JSON structure for a valid SBOM
- [ ] Handler unit test: verify 404 response for a nonexistent SBOM

## Verification Commands
- `cargo test -p fundamental` -- all tests pass including new endpoint tests
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` -- returns JSON license report (manual verification against running server)

## Documentation Updates
- `README.md` -- Add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 3 -- Add license report service
