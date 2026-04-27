## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a structured license compliance report for a given SBOM. This endpoint wires up the `LicenseReportService` to the Axum router and returns the `LicenseReport` JSON response. It follows the existing endpoint registration pattern used by other SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — ensure the SBOM module routes (which now include the license report) are mounted (should already be in place if the SBOM module is registered)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the Axum handler for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with packages grouped by license and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — the handler function extracts a path parameter (`id`), calls a service method, and returns `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `list` and `get` routes. The route registration pattern uses Axum's `.route()` method chaining — add `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))`.
- The handler should:
  1. Extract the SBOM ID from the path parameter.
  2. Load the license policy configuration from the configured policy file path (or use a default policy).
  3. Call `LicenseReportService::generate_report(sbom_id, &policy)`.
  4. Return `Json(report)` on success, or propagate `AppError` on failure.
- Error cases to handle: SBOM not found (return 404), policy file not found or invalid (return 500 with descriptive error), database errors (propagate as 500).
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the convention in `common/src/error.rs`.
- Per docs/constraints.md 4.7: follow the patterns found in existing endpoint files, not abstract guidance.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference implementation for an SBOM endpoint that extracts a path parameter and calls a service; follow the same function signature and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; add the new route using the same `.route()` chaining style
- `common/src/error.rs::AppError` — error type used by all endpoint handlers for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Response shape matches `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error when the license policy configuration is missing or invalid
- [ ] Route is registered in the SBOM endpoints module
- [ ] Handler follows the existing endpoint pattern (path extraction, service call, JSON response)

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` for a valid SBOM returns 200 with grouped license data
- [ ] Integration test: `GET /api/v2/sbom/{invalid-id}/license-report` returns 404
- [ ] Integration test: response JSON structure matches the expected `LicenseReport` schema

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental -- license_report` — expected: all license report endpoint tests pass

## Documentation Updates
- `README.md` — add the new `GET /api/v2/sbom/{id}/license-report` endpoint to the API reference section, including request parameters, response shape, and license policy configuration instructions

## Dependencies
- Depends on: Task 2 — License report service
