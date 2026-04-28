# Task 4 -- License Report Endpoint

## Repository
trustify-backend

## Description
Register the `GET /api/v2/sbom/{id}/license-report` endpoint in the SBOM endpoints module. This endpoint invokes the `LicenseReportService` to generate a license compliance report for the specified SBOM and returns it as a JSON response. It serves both human consumers (compliance officers) and automated CI/CD pipeline compliance gates.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Add the new route to the SBOM route registration and add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a structured license compliance report grouped by license type with compliance flags. Response shape: `{ sbom_id: string, groups: [{ license: string, packages: [{ name: string, version: string }], compliant: bool }], compliant: bool }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure:
  - Extract path parameters using Axum extractors
  - Call the service layer
  - Return `Result<Json<LicenseReport>, AppError>`
- Route registration: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs` (see existing `.route()` calls in that file)
- The handler should:
  1. Extract the SBOM `id` from the URL path
  2. Load the `LicensePolicy` from configuration
  3. Call `LicenseReportService::generate_report()`
  4. Return the `LicenseReport` as JSON
- Return HTTP 404 with a descriptive error if the SBOM ID does not exist (handled by the service returning `AppError`)
- Per constraints doc section 5.3: follow the exact patterns referenced in the task's Implementation Notes
- Per constraints doc section 2.1: commit must reference TC-9004 in the footer
- Per constraints doc section 3.1: feature branch must be named after the Jira issue ID

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference pattern for SBOM endpoint handler with path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- existing route registration to follow for adding the new route
- `modules/fundamental/src/advisory/endpoints/get.rs` -- additional reference for endpoint handler patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON body
- [ ] Response includes packages grouped by license with compliance flags
- [ ] Request for a non-existent SBOM returns HTTP 404
- [ ] Endpoint is registered and reachable via the Axum router
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 response with correct JSON structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify the response includes transitive dependency licenses

## Documentation Updates
- `README.md` -- Add the new license report endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 3 -- License Report Service (for `LicenseReportService::generate_report`)
