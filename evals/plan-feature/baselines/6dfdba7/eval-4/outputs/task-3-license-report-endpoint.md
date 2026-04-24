## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` REST endpoint that invokes the license compliance report service and returns the structured compliance report as JSON. This exposes the license compliance feature to API consumers including compliance officers and CI/CD pipelines.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`, route registration function.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the license-report route in the existing SBOM router.
- `server/src/main.rs` — Verify the license-report routes are mounted via the existing SBOM module registration (may require no change if SBOM routes are auto-mounted).

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON response with packages grouped by license and compliance flags.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it defines an async handler function that extracts path parameters, calls the service layer, and returns a JSON response wrapped in `Result<Json<T>, AppError>`.
- The handler should:
  1. Extract the SBOM `id` from the URL path using Axum's `Path` extractor.
  2. Load the `LicensePolicyConfig` from the `license-policy.json` file (or from a shared application state if preferred).
  3. Call `LicenseReportService::generate_report(db, &id, &policy)`.
  4. Return the `LicenseReport` as `Json(report)`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be nested under the existing `/api/v2/sbom` prefix as `/{id}/license-report`.
- Error handling: Return appropriate HTTP status codes — `404 Not Found` if the SBOM ID does not exist, `500 Internal Server Error` for unexpected failures. Use `AppError` from `common/src/error.rs` which already implements `IntoResponse`.
- The endpoint requires authentication consistent with other SBOM endpoints (no special auth bypass).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Direct pattern reference for an Axum handler extracting `Path<String>` and returning `Json<T>`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Pattern for route registration; add the new route alongside existing SBOM routes
- `common/src/error.rs::AppError` — Standard error type implementing `IntoResponse`; use for all error returns
- `modules/fundamental/src/sbom/service/license_report.rs::LicenseReportService` — Service from Task 2 that generates the report

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` structure
- [ ] Response body contains `groups` array with `license`, `packages`, and `compliant` fields per group
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] The endpoint requires authentication (no auth bypass)
- [ ] Route is registered and reachable through the Axum router
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Unit test: Handler returns 200 with valid LicenseReport JSON for a known SBOM
- [ ] Unit test: Handler returns 404 for a non-existent SBOM ID
- [ ] Unit test: Response JSON structure matches expected format with `groups`, `total_packages`, and `non_compliant_count` fields

## Dependencies
- Depends on: Task 2 — Implement license compliance report service
