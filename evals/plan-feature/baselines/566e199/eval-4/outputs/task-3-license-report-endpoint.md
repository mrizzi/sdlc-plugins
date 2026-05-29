# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint that exposes the license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` to generate the report and returns the structured JSON response. This completes the user-facing API for the license compliance feature.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `license-report` route under the existing `/api/v2/sbom` router
- `server/src/main.rs` — no changes expected if the sbom module router is already mounted; verify route mounting

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "..." }], compliant: true }] }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract the SBOM ID from the path using Axum's `Path` extractor, inject database connection and service dependencies.
- The handler should:
  1. Extract the SBOM `id` from the URL path
  2. Load the `LicensePolicy` from the configured policy file
  3. Call `LicenseReportService::generate_report(id, &db, &policy)`
  4. Return the `LicenseReport` as JSON with `StatusCode::OK`
  5. Return `StatusCode::NOT_FOUND` if the SBOM does not exist
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes (`list.rs`, `get.rs`). Add `.route("/{id}/license-report", get(license_report::handler))`.
- Use `Result<Json<LicenseReport>, AppError>` as the handler return type, consistent with other endpoints.
- Error handling: use `.context("generating license report")` on the service call, following the pattern in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the same handler pattern for path extraction, error handling, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing `groups` array
- [ ] Each group contains `license` (string), `packages` (array), and `compliant` (boolean)
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] The endpoint is registered and accessible through the Axum router

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID that has packages with licenses, verify 200 response with correct grouping structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID, verify 404 response
- [ ] Integration test: call the endpoint for an SBOM where some packages have policy-violating licenses, verify `compliant: false` on those groups
- [ ] Integration test: verify the response includes transitive dependency licenses

## Verification Commands
- `cargo test --test api` — integration tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — returns valid JSON response

## Documentation Updates
- `README.md` — document the new `GET /api/v2/sbom/{id}/license-report` endpoint, its request parameters, response schema, and the license policy configuration file format

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
