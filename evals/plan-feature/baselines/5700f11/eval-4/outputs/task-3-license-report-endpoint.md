## Repository
trustify-backend

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint delegates to the `LicenseReportService` from Task 2 and returns the `LicenseReport` as a JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/api/v2/sbom/{id}/license-report` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a `LicenseReport` JSON object containing packages grouped by license with compliance flags. Returns 200 on success, 404 if the SBOM ID does not exist.

## Implementation Notes
- Follow the handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting the SBOM ID path parameter and returning JSON responses.
- The handler should:
  1. Extract the SBOM `id` from the path using Axum's `Path` extractor
  2. Call `LicenseReportService::generate()` with the database connection and SBOM ID
  3. Return the `LicenseReport` as `Json<LicenseReport>` on success
  4. Return `AppError::NotFound` if the SBOM does not exist (check this before generating the report)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. Follow the route registration pattern used for `get.rs` and `list.rs` in that module.
- The handler function signature should return `Result<Json<LicenseReport>, AppError>` matching the error handling convention described in `common/src/error.rs`.
- Consider adding `tower-http` caching headers for the response since license reports for a given SBOM are relatively stable. Follow the caching middleware pattern noted in the repository conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Reference for SBOM ID path extraction, database connection access, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern to follow when adding the new route
- `common/src/error.rs::AppError` -- Error handling with `IntoResponse` implementation
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Pattern for checking SBOM existence before delegating to the report service

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body for an existing SBOM
- [ ] Returns 404 with an appropriate error message for a non-existent SBOM ID
- [ ] Response `Content-Type` is `application/json`
- [ ] Response body matches the structure: `{ "groups": [{ "license": "...", "packages": [...], "compliant": true/false }] }`

## Verification Commands
- `cargo build -p trustify-fundamental` -- Compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/license-report | jq .` -- Returns formatted license report JSON

## Dependencies
- Depends on: Task 2 -- License report model and service (provides `LicenseReportService` and `LicenseReport`)
