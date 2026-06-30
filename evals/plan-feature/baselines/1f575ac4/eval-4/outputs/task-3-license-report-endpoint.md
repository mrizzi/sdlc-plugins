# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for a given SBOM. This endpoint calls the `LicenseReportService` from Task 2 and returns the grouped license data with compliance flags as a JSON response. The endpoint follows the existing Axum handler pattern in the sbom module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license report route alongside existing sbom routes (list, get)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a JSON license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "..." }], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it demonstrates extracting the SBOM ID path parameter, calling a service method, handling errors, and returning a JSON response.
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be nested under the existing `/api/v2/sbom` prefix.
- The handler should:
  1. Extract the SBOM ID from the path parameter (like `get.rs` does)
  2. Load the license policy (from the `LicensePolicy` config)
  3. Call `LicenseReportService::generate_report()`
  4. Return the `LicenseReport` as JSON
- Error handling: return `Result<Json<LicenseReport>, AppError>` consistent with other handlers. Use `.context()` for error wrapping per `common/src/error.rs` patterns.
- The endpoint should be registered in `server/src/main.rs` if the sbom module registration does not already pick up new routes automatically from `endpoints/mod.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Demonstrates the handler pattern for extracting SBOM ID from path parameters and returning JSON responses.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Shows how routes are registered for the sbom module; the new route should follow the same pattern.
- `modules/fundamental/src/sbom/endpoints/list.rs` — Another handler example showing the Axum response pattern.
- `common/src/error.rs::AppError` — The error type used by all handlers; implements `IntoResponse` for HTTP error responses.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body containing `groups` array
- [ ] Each group contains `license` (string), `packages` (array), and `compliant` (boolean) fields
- [ ] The endpoint returns HTTP 404 (or appropriate error) when the SBOM ID does not exist
- [ ] The route is registered and accessible through the Axum server
- [ ] Response content-type is `application/json`

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/license-report` for a valid SBOM returns 200 with correct grouped license data
- [ ] Integration test: GET request for a non-existent SBOM ID returns an appropriate error status

## Verification Commands
- `cargo build` — Compiles successfully with the new endpoint
- `cargo test` — All existing and new tests pass

## Documentation Updates
- `README.md` — Add the new license report endpoint to the API documentation section if one exists

## Dependencies
- Depends on: Task 2 — Implement license report aggregation service
