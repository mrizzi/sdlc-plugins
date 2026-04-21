# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that invokes the LicenseReportService to generate a compliance report for the specified SBOM and returns the result as JSON. Register the route in the license endpoint module and mount it in the server's route configuration.

## Files to Create
- `modules/fundamental/src/license/endpoints/mod.rs` — Route registration for the license report endpoint; exports a router/configure function
- `modules/fundamental/src/license/endpoints/report.rs` — GET handler for `/api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the endpoints submodule
- `server/src/main.rs` — Mount the license report routes in the Axum server route tree

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseComplianceReport` JSON object with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` -- it shows how to extract a path parameter (SBOM ID), call a service method, and return a JSON response.
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` -- each endpoint module has a router or `configure` function that registers routes with Axum.
- The handler should: (1) extract the SBOM ID from the URL path, (2) call `LicenseReportService::generate_report(db, sbom_id)`, (3) return the result serialized as JSON with `axum::Json`.
- Error handling: return `AppError` variants for not-found (404) and internal errors (500), matching the pattern in `common/src/error.rs`. The `AppError` type already implements `IntoResponse`.
- Per CONVENTIONS.md Key Conventions: endpoint registration goes in `endpoints/mod.rs`; final server mounting goes in `server/src/main.rs`.
- Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — canonical example of a GET endpoint with path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for reference
- `common/src/error.rs::AppError` — error type for handler error responses, implements IntoResponse

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseComplianceReport JSON body for an existing SBOM
- [ ] Response JSON structure matches `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Returns 404 with appropriate error message for non-existent SBOM ID
- [ ] Endpoint is accessible through the mounted server route configuration

## Test Requirements
- [ ] Integration test: GET request returns 200 with correct report structure for an SBOM with known packages and licenses
- [ ] Integration test: GET request returns 404 for non-existent SBOM ID
- [ ] Integration test: report correctly flags non-compliant licenses based on the configured policy

## Verification Commands
- `cargo test --package fundamental -- license::endpoints` — endpoint unit/integration tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — returns valid JSON response (manual verification against running server)

## Documentation Updates
- `README.md` — Document the new endpoint: path, HTTP method, path parameters, response schema, and example response

## Dependencies
- Depends on: Task 2 — Add license compliance report service with transitive dependency resolution
