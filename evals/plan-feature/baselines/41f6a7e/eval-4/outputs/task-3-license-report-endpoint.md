# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint that exposes the license compliance report for a given SBOM. This endpoint calls the LicenseReportService, serializes the result, and returns it as a JSON response. The endpoint follows the existing Axum routing and error handling patterns established by the SBOM module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license-report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (which now include the license report) are mounted (likely already handled by existing SBOM route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report grouped by license type with policy compliance flags. Response shape: `{ sbom_id: string, groups: [{ license: string, packages: [...], compliant: bool, policy_action: string }], total_packages: number, compliant_count: number, non_compliant_count: number }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it shows how to:
  - Extract path parameters (SBOM ID) using Axum extractors
  - Call the service layer
  - Return `Result<Json<T>, AppError>` for consistent error handling
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used by `list.rs` and `get.rs` route registration
- The handler should:
  1. Extract the SBOM ID from the path
  2. Load the license policy (from the config file path, possibly injected via Axum state/extension)
  3. Call `LicenseReportService::generate(sbom_id, &policy)`
  4. Return `Json(report)` on success
- For the license policy loading, consider adding it to the Axum application state so it is loaded once at startup rather than on every request — inspect `server/src/main.rs` for how other shared state is configured
- Per docs/constraints.md section 2.1: commits must reference TC-9004
- Per docs/constraints.md section 3.1: feature branch named after the Jira issue ID
- Per docs/constraints.md section 5.3: follow the patterns referenced in these Implementation Notes

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint showing Axum handler pattern with path parameter extraction and service call
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for adding new routes to the SBOM module
- `common/src/error.rs::AppError` — implements `IntoResponse` for automatic HTTP error response conversion

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/license-report returns 200 with a JSON license compliance report
- [ ] Response body matches the specified schema: groups array with license, packages, compliant flag, and policy_action
- [ ] Requesting a report for a non-existent SBOM returns an appropriate error status (404)
- [ ] The endpoint is registered and accessible through the standard server route tree

## Test Requirements
- [ ] Integration test: call GET /api/v2/sbom/{id}/license-report for an SBOM with known package-license data and verify the response structure and compliance flags
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify a 404 response
- [ ] Integration test: call the endpoint for an SBOM containing packages with denied licenses and verify non-compliant flags appear in the response

## Verification Commands
- `cargo test --test api license_report` — run license report integration tests, expect all tests to pass
- `cargo build` — verify the project compiles cleanly with the new endpoint

## Dependencies
- Depends on: Task 2 — Add LicenseReportService for compliance aggregation
