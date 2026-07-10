## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the `GET /api/v2/sbom/{id}/license-report` endpoint in the SBOM endpoints module.
This endpoint calls the license report service to generate a compliance report for the
specified SBOM and returns the structured response. The endpoint follows the existing
Axum handler patterns and integrates with the server's route registration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID from the path, calls the license report service, and returns the `LicenseReport` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route and add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReport` JSON with `{ groups: [{ license: String, packages: [PackageSummary], compliant: bool }] }`

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`
for the handler function signature, path parameter extraction, and response construction.

The handler should:
1. Extract the SBOM ID from the path parameter using Axum's `Path` extractor
2. Load the license policy (from the config file or injected state)
3. Call `LicenseReportService::generate_report()` with the SBOM ID and policy
4. Return the `LicenseReport` as a JSON response
5. Map service errors to appropriate HTTP status codes via `AppError`

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the
same pattern used for the existing `GET /api/v2/sbom/{id}` route in `get.rs`.

Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<LicenseReport>, AppError>`
with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs`
following the established pattern.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory
structure.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's module directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern for `GET /api/v2/sbom/{id}` including path extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — demonstrates route registration pattern; follow for adding the new license-report route
- `common/src/error.rs::AppError` — the error type that implements `IntoResponse` for automatic HTTP status code mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error responses for internal failures
- [ ] Route is registered and accessible at the correct path
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Endpoint returns 200 with correct JSON shape for a valid SBOM with license data
- [ ] Endpoint returns 404 for a non-existent SBOM ID
- [ ] Response JSON matches the `LicenseReport` schema with `groups` array

## Dependencies
- Depends on: Task 1 — Add license report model types
- Depends on: Task 3 — Add license report service
