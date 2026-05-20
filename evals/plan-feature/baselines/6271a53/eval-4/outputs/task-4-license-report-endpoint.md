# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint loads the license policy, invokes the LicenseReportService, and returns the structured report as JSON. This is the user-facing API that compliance officers and CI/CD pipelines will call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [{ package_name: "...", version: "...", transitive: false }], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `get.rs` for the single-resource GET handler pattern (path parameter extraction, service call, JSON response)
- Use Axum's `Path` extractor for the SBOM ID parameter
- The handler should:
  1. Extract the SBOM ID from the path
  2. Load the LicensePolicy (from Task 1) — either from a configured path or embedded default
  3. Call `LicenseReportService::generate()` (from Task 3) with the database connection, SBOM ID, and policy
  4. Return the `LicenseReport` as JSON with `StatusCode::OK`
- Error handling: return `Result<Json<LicenseReport>, AppError>` consistent with all other handlers in the codebase
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (see how `list.rs` and `get.rs` routes are registered)
- The route should be mounted under the existing SBOM router so it appears as `/api/v2/sbom/{id}/license-report`
- Per constraints (docs/constraints.md) section 3: PR branch must be named after the Jira issue ID
- Per constraints (docs/constraints.md) section 2: commit must reference the Jira issue ID and follow Conventional Commits

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET /api/v2/sbom/{id} handler demonstrates path parameter extraction, service invocation, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration shows how to wire new handlers into the Axum router
- `common/src/error.rs` — AppError for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body matching the LicenseReport schema
- [ ] Invalid or non-existent SBOM ID returns an appropriate error status (404)
- [ ] Response Content-Type is application/json
- [ ] Route is properly registered and accessible alongside existing SBOM endpoints

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 response with correct JSON shape
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify error response
- [ ] Integration test: verify the response contains packages grouped by license with compliance flags

## Verification Commands
- `cargo build` — verifies the code compiles without errors
- `cargo test` — verifies all tests pass including the new integration tests

## Documentation Updates
- `README.md` — Add the new license report endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 3 — Add LicenseReportService for license aggregation and compliance checking
