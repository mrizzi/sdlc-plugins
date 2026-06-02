## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that exposes the license compliance report for a given SBOM. The endpoint calls the LicenseReportService (from Task 2) and returns the structured LicenseReport response. This is the user-facing API that compliance teams and CI/CD pipelines will call to retrieve license compliance data.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license-report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the sbom module routes (which now include the license-report sub-route) are mounted (likely already handled by existing route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure. That file demonstrates:
- Extracting path parameters (SBOM ID)
- Calling the service layer
- Returning `Result<Json<T>, AppError>`

The handler should:
1. Extract the SBOM ID from the path parameter
2. Call `LicenseReportService::generate_report(sbom_id)` 
3. Return `Json(report)` on success, or propagate `AppError` on failure
4. Return 404 if the SBOM ID does not exist

Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for the existing `get` and `list` routes. The route should be nested under the existing `/api/v2/sbom` prefix.

Per CONVENTIONS.md §Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Key Conventions: register routes in the module's `endpoints/mod.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow this handler's pattern for path parameter extraction, service invocation, and response construction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for route registration pattern
- `common/src/error.rs::AppError` — Error type implementing IntoResponse for automatic HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing `groups` array
- [ ] Each group in the response contains `license` (string), `packages` (array), and `compliant` (boolean) fields
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error response for invalid SBOM ID format
- [ ] Response content type is application/json

## Test Requirements
- [ ] Integration test: GET license-report for an SBOM with known packages and licenses — verify response structure and compliance flags
- [ ] Integration test: GET license-report for a non-existent SBOM ID — verify 404 response
- [ ] Integration test: GET license-report for an SBOM with no packages — verify empty groups array
- [ ] Integration test: verify response matches expected JSON schema (groups array with license, packages, compliant fields)

## Verification Commands
- `cargo test --test api` — Run integration tests and verify all license-report tests pass

## Dependencies
- Depends on: Task 2 — Add LicenseReport model and service
