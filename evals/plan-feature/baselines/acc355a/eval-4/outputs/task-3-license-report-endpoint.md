# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that exposes the license compliance report service to API consumers. The endpoint accepts an SBOM ID as a path parameter and returns a structured JSON response with packages grouped by license and compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route
- `server/src/main.rs` — Ensure the SBOM module routes (which now include the license-report sub-route) are mounted (likely already handled by existing module mount, but verify)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license type and compliance flags

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — this demonstrates the Axum handler signature, path parameter extraction, service injection, and error response pattern.
- The handler should:
  1. Extract the SBOM `id` from the path using Axum's `Path` extractor
  2. Call `LicenseReportService` to generate the report
  3. Return the `LicenseReport` as JSON with `StatusCode::OK`
  4. Return `AppError` (404) if the SBOM is not found
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs` — add a `.route("/:id/license-report", get(license_report::handler))` or equivalent.
- The response content type is `application/json`. The response shape is:
  ```json
  {
    "groups": [
      {
        "license": "MIT",
        "packages": [
          { "name": "serde", "version": "1.0.0" }
        ],
        "compliant": true
      }
    ]
  }
  ```
- All handlers must return `Result<T, AppError>` using the error type from `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern for SBOM endpoints with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows route registration pattern to follow
- `modules/fundamental/src/advisory/endpoints/get.rs` — alternative example of a GET-by-ID endpoint pattern
- `common/src/error.rs::AppError` — standard error type for endpoint error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON license report
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response body matches the documented JSON structure with `groups` array
- [ ] Route is properly registered in the SBOM module's route configuration

## Test Requirements
- [ ] Unit test: handler returns 200 with valid license report for an existing SBOM
- [ ] Unit test: handler returns 404 for a non-existent SBOM ID

## Documentation Updates
- `README.md` — Add the new license report endpoint to the API reference section, including the endpoint path, HTTP method, request parameters, and response shape

## Dependencies
- Depends on: Task 2 — Add license report service with compliance checking
