# Task 3 — Add License Report Endpoint

## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that invokes the `LicenseReportService` and returns the structured license compliance report. Register the new route in the SBOM endpoint module and mount it in the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (which now include the license report) are mounted (likely already handled by existing SBOM module mounting, but verify)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response containing packages grouped by license with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`):
  - Extract the SBOM ID from the path using Axum's `Path` extractor
  - Call the service method and return the result as JSON
  - Return `Result<Json<LicenseReport>, AppError>` — use the same error handling pattern with `.context()` wrapping
- Route registration: in `modules/fundamental/src/sbom/endpoints/mod.rs`, add the new route using the same pattern as the existing `get` and `list` routes. The route should be nested under the existing `/api/v2/sbom` prefix as `/api/v2/sbom/{id}/license-report`.
- The endpoint should return HTTP 404 if the SBOM ID does not exist, consistent with the existing `get.rs` handler behavior.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format and reference TC-9004 in the footer.
- Per constraints doc section 3 (PR Rules): name the feature branch after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow the same pattern for path extraction, service invocation, and error responses
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new endpoint
- `common/src/error.rs::AppError` — standard error type for endpoint error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON body for an SBOM with license data
- [ ] The endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] The response JSON matches the specified shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] The route is properly registered and accessible through the server

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` for an SBOM with known packages and licenses, verify the response shape and compliance flags
- [ ] Integration test: call the endpoint with a non-existent SBOM ID, verify HTTP 404 response
- [ ] Integration test: call the endpoint for an SBOM with no packages, verify empty groups array

## Documentation Updates
- `README.md` — Add the new license report endpoint to any API endpoint listing or feature overview

## Dependencies
- Depends on: Task 2 — Implement License Report Service
