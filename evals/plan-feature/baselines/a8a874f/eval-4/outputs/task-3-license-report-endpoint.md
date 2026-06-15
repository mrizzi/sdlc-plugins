# Task 3: Implement the license-report endpoint

## Repository

trustify-backend

## Target Branch

main

## Description

Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that returns a license compliance report for a given SBOM. The endpoint handler extracts the SBOM ID from the path, loads the license policy configuration, calls the service method to generate the report, and returns the `LicenseReport` as a JSON response.

## Files to Create

- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- Axum handler function for `GET /api/v2/sbom/{id}/license-report`. Extracts the SBOM `id` from the path using `Path<Uuid>`, loads the `LicensePolicy`, invokes the service to generate the report, and returns `Json<LicenseReport>`. Returns 404 if the SBOM ID does not exist, and 500 with an appropriate error for other failures.

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Add `pub mod license_report;` and register the new route (`.route("/api/v2/sbom/:id/license-report", get(license_report::handler))`) in the existing router configuration.

## Implementation Notes

- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract path parameters with `axum::extract::Path`, inject shared state (database connection, configuration) via Axum extractors, and return `Result<Json<T>, AppError>`.
- The route should be registered alongside the existing SBOM routes in `endpoints/mod.rs`, following the same registration pattern used for `list.rs` and `get.rs`.
- Ensure the endpoint requires the same authentication/authorization as other SBOM endpoints (no special bypass, no unauthenticated access).
- The license policy file path can be injected via application state/configuration or loaded per-request from a well-known path. Prefer injecting it through shared application state for consistency with the existing architecture.

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/{id}/license-report` returns a `200 OK` with a JSON `LicenseReport` body for a valid SBOM ID
- [ ] Returns `404 Not Found` when the SBOM ID does not exist
- [ ] Returns appropriate error responses for invalid input (e.g., malformed UUID)
- [ ] The endpoint is registered in the SBOM module's route configuration
- [ ] Authentication requirements match existing SBOM endpoints
- [ ] Response content type is `application/json`

## Test Requirements

- Endpoint handler tests are covered in Task 4 (integration tests). This task focuses on wiring the handler and route registration.

[Description digest: sha256-md:c8d41f3a2e5b097163f8e2db9a406c7e15bf53d80e94a62c17d038f5b9e274a1 would be posted as a comment]
