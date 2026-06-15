## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for a given SBOM. The endpoint invokes the LicenseReportService and returns the grouped license data with compliance flags as a JSON response.

## Files to Create
- `modules/fundamental/src/license/endpoints/mod.rs` — Route registration for license report endpoint
- `modules/fundamental/src/license/endpoints/report.rs` — Handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the endpoints submodule
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Mount the license report route under the /api/v2/sbom/{id} prefix
- `server/src/main.rs` — Ensure the license module routes are mounted in the Axum router

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "...", transitive: false }], compliant: true }] }`

## Implementation Notes
Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` — the handler extracts the SBOM ID from the path, calls the service, and returns the result as JSON.

The route should be nested under the existing SBOM routes so the path is `/api/v2/sbom/{id}/license-report`. Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `get` and `list` routes. The endpoint registration pattern is visible in `modules/fundamental/src/sbom/endpoints/mod.rs`.

The handler must:
1. Extract the SBOM ID from the path parameter
2. Load the license policy configuration
3. Call `LicenseReportService` to generate the report
4. Return the report as a JSON response with `StatusCode::OK`

Error handling: return `Result<Json<LicenseReport>, AppError>` following the convention in `common/src/error.rs`. A 404 should be returned for non-existent SBOM IDs.

The route should be mounted in `server/src/main.rs` following the same pattern used for other module routes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow this handler's pattern for path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — follow route registration pattern for adding the new sub-route
- `common/src/error.rs::AppError` — reuse for error responses (404, 500)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON compliance report
- [ ] Response body matches the shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns 404 for non-existent SBOM IDs
- [ ] Endpoint is accessible at the correct path under the SBOM routes
- [ ] Route is registered and mounted in the server

## Test Requirements
- [ ] Integration test: GET returns 200 and valid report for an SBOM with known packages and licenses
- [ ] Integration test: GET returns 404 for a non-existent SBOM ID
- [ ] Integration test: response body contains expected license groups and compliance flags
- [ ] Integration test: transitive dependencies appear in the report with correct flag

## Dependencies
- Depends on: Task 2 — License report service

[sdlc-workflow] Description digest: sha256-md:99452fa7f38ee28ee3a94198dc78f0ccd4886886129034e257cfbd110fe72e35
