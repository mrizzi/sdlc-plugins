## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the `LicenseReportService` and returns the license compliance report as a JSON response. Register the route in the SBOM endpoint module and mount it in the server.

## Files to Create
- `modules/fundamental/src/sbom/license_report/endpoints.rs` -- defines the Axum handler function `get_license_report` that extracts the SBOM ID from the path, calls `LicenseReportService::generate_report`, and returns `Json<LicenseReport>`

## Files to Modify
- `modules/fundamental/src/sbom/license_report/mod.rs` -- add `pub mod endpoints;` declaration
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the `/api/v2/sbom/{id}/license-report` route by nesting the license_report endpoint router
- `server/src/main.rs` -- if needed, ensure the SBOM module routes include the new license-report subroute (may already be covered by existing SBOM route mounting)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a JSON license compliance report for the specified SBOM. Response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "compliant": true }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` -- extract the SBOM ID using `Path<Uuid>`, obtain the database connection from Axum state, and return `Result<Json<LicenseReport>, AppError>`.
- Route registration should follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which uses Axum's `Router::new().route(...)` builder.
- Load the `LicensePolicy` at application startup or lazily on first request. Consider adding policy path to the application configuration/state. For simplicity in the MVP, loading from a well-known path on each request (with caching via `once_cell` or similar) is acceptable.
- The endpoint must respect existing authentication/authorization middleware already applied at the server level in `server/src/main.rs`. No special auth handling is needed in this handler.
- Return HTTP 404 (`AppError::NotFound`) if the SBOM ID does not exist, following the pattern in the existing `get.rs` endpoint.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- pattern for Path extraction and error handling in SBOM endpoints
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- pattern for route registration
- `common/src/error.rs::AppError` -- standard error responses (NotFound, InternalServerError)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON `LicenseReport` for a valid SBOM
- [ ] Returns HTTP 404 for a nonexistent SBOM ID
- [ ] Response JSON matches the documented shape: `{ groups: [...], compliant: bool }`
- [ ] Route is registered and reachable through the existing SBOM route hierarchy
- [ ] Endpoint follows existing authentication middleware (no bypass, no special auth)

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` with a seeded SBOM returns HTTP 200 and valid JSON
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent-id}/license-report` returns HTTP 404
- [ ] Integration test: response contains expected license groups matching seeded package data
- [ ] Integration test: response `compliant` flag is `false` when seeded data includes a denied license

## Verification Commands
- `cargo test --test api license_report` -- run integration tests for the license-report endpoint, expect all tests to pass

## Dependencies
- Depends on: Task 2 -- License report service (provides `LicenseReportService::generate_report`)
