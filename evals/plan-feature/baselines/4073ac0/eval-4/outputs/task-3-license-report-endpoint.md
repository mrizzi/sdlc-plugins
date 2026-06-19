## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns the license compliance report for a given SBOM. Register the route within the existing SBOM endpoint module. The handler delegates to the LicenseReportService and returns the structured JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license-report route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license and compliance flags based on the configured policy. Response shape: `{ groups: [{ license: string, packages: [{ name: string, version: string }], compliant: bool }] }`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function signature, path parameter extraction, and response formatting.
- The handler should extract the SBOM ID from the path using Axum's `Path` extractor, call `LicenseReportService::generate_report(sbom_id)`, and return the `LicenseReport` as JSON.
- Return `Result<Json<LicenseReport>, AppError>` consistent with the error handling pattern in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same router builder pattern as the existing `list.rs` and `get.rs` routes. The route should be nested under the existing `/api/v2/sbom` prefix as `/{id}/license-report`.
- No authentication changes are needed beyond what the existing SBOM endpoints already require.
- Consider adding `tower-http` caching middleware configuration for this endpoint, following patterns from other endpoint route builders, since license reports for a given SBOM are unlikely to change frequently.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for single-resource GET handler with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error response type implementing IntoResponse

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseReport` for a valid SBOM ID
- [ ] Response JSON matches the specified shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] Returns appropriate error (404) for non-existent SBOM ID
- [ ] Route is registered within the existing SBOM endpoint module
- [ ] Handler uses `Result<Json<LicenseReport>, AppError>` return type

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct license grouping
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON structure matches expected schema

## Dependencies
- Depends on: Task 2 — Implement license report service
