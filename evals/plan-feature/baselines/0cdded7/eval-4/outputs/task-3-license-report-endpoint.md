# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that returns a structured license compliance report for a given SBOM. The endpoint calls the `LicenseReportService` from Task 2 to generate the report and returns the result as JSON. This is the primary user-facing entry point for the license compliance feature.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/license-report` route under the existing `/api/v2/sbom/{id}` path
- `server/src/main.rs` — Ensure the sbom module routes are mounted (likely already done; verify)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ sbom_id, generated_at, groups: [{ license, packages: [{ name, version }], compliant, policy_action }], summary: { total_packages, compliant_count, non_compliant_count } }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function structure, path parameter extraction, and error handling
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the license policy configuration (from the loader in Task 1)
  3. Call `LicenseReportService::generate_report(sbom_id, policy)`
  4. Return the `LicenseReport` as a JSON response with `StatusCode::OK`
  5. Return `StatusCode::NOT_FOUND` if the SBOM does not exist
- Route registration: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be nested under the existing `/:id` path as `/:id/license-report`
- Error handling: return `Result<Json<LicenseReport>, AppError>` matching the existing Axum handler pattern with `.context()` wrapping
- Consider adding `Cache-Control` headers via `tower-http` caching middleware, following the caching patterns noted in the repository conventions. License reports can be cached briefly since SBOM data changes infrequently

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow this handler as the direct template for path parameter extraction and response formatting
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error type and IntoResponse implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns `200 OK` with a JSON license report for a valid SBOM
- [ ] Response body matches the documented shape: `{ sbom_id, generated_at, groups: [...], summary: {...} }`
- [ ] Returns `404 Not Found` for a non-existent SBOM ID
- [ ] The endpoint is accessible at the documented path (registered in the route tree)
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID — returns 200 with correct report structure
- [ ] Integration test: call the endpoint with a non-existent SBOM ID — returns 404
- [ ] Integration test: call the endpoint for an SBOM with no packages — returns 200 with empty groups
- [ ] Integration test: verify response body includes `compliant: false` for SBOMs with denied licenses

## Verification Commands
- `cargo test --test api -- license_report` — Run license report integration tests, expect all to pass

## Documentation Updates
- `README.md` — Add the license report endpoint to the API overview section if one exists

## Dependencies
- Depends on: Task 2 — Add license report service and response models

[sdlc-workflow] Description digest: sha256:73fb9dcea805ad8f8a8e3acde411d9e1d6c75f22586e2fa5629b75182dd90743
