## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for the specified SBOM. The endpoint calls the license report service to aggregate packages by license, evaluate policy compliance, and return the grouped report.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for the new license-report endpoint
- `server/src/main.rs` — verify the SBOM module routes are already mounted (no change expected, but confirm)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the GET handler for `/api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with packages grouped by license and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — handlers are async functions that extract path parameters, call the service, and return a JSON response or `AppError`.
- Route registration pattern: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing SBOM routes (`GET /api/v2/sbom` for list, `GET /api/v2/sbom/{id}` for details).
- The handler should:
  1. Extract the SBOM `{id}` from the path
  2. Call `LicenseReportService::generate_report(id)` 
  3. Return the `LicenseReport` as JSON with `StatusCode::OK`
  4. Return `AppError` with appropriate status code if SBOM not found (404) or other errors
- Error handling: use `Result<Json<LicenseReport>, AppError>` return type with `.context()` wrapping per the established convention.
- Per CONVENTIONS.md: follow the existing endpoint module pattern. Register the route in `endpoints/mod.rs` using the same router builder pattern as existing endpoints.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler for SBOM details; follow the same pattern for path extraction and response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration showing how to add new routes to the SBOM router
- `common/src/error.rs::AppError` — error type with IntoResponse implementation for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON response
- [ ] Response body contains `groups` array with `license`, `packages`, and `compliant` fields per group
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Endpoint is properly registered in the SBOM route module

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/license-report` for a valid SBOM returns 200 with correct groupings
- [ ] Integration test: GET request for non-existent SBOM ID returns 404
- [ ] Integration test: response JSON structure matches the expected schema (`groups` array with `license`, `packages`, `compliant`)
- [ ] Integration test: transitive dependency licenses appear in the report

## Verification Commands
- `cargo build -p trustify-server` — compiles without errors
- `cargo test -- license_report` — all license report integration tests pass

## Documentation Updates
- `README.md` — add the new license report endpoint to the API summary if one exists

## Dependencies
- Depends on: Task 2 — Implement license compliance report service logic
