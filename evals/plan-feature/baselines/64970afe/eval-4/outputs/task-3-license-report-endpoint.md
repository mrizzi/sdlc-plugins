## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint for TC-9004. This task creates the Axum handler function that receives an SBOM ID path parameter, invokes the LicenseReportService (from Task 2) to generate the compliance report, and returns the structured JSON response. It also registers the new route in the SBOM endpoints module so it is mounted by the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the license-report route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report for the specified SBOM, with response shape `{ groups: [{ license: string, packages: [...], compliant: bool }] }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler signature, path parameter extraction, error handling, and response serialization.
- The handler should extract the SBOM ID from the path using Axum's `Path` extractor, call `LicenseReportService::generate_report(sbom_id)`, and return the `LicenseReport` as JSON.
- Return appropriate HTTP error codes: 404 if the SBOM ID does not exist, 500 for internal errors. Use `AppError` from `common/src/error.rs` for error mapping.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes. Follow the existing route registration pattern (e.g., `.route("/{id}/license-report", get(license_report::handler))`).
- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs`; the server mounts all modules via `server/src/main.rs` (no changes needed to main.rs since the SBOM module is already mounted).
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on service errors.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow its pattern for path parameter extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow the same pattern for adding the new route
- `common/src/error.rs::AppError` — reuse for error responses (404, 500)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the LicenseReport JSON structure
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error responses for internal failures
- [ ] Route is registered and accessible without changes to `server/src/main.rs`

## Test Requirements
- [ ] Verify the endpoint returns 200 with correct JSON structure for a valid SBOM ID
- [ ] Verify the endpoint returns 404 for a non-existent SBOM ID
- [ ] Verify the response JSON matches the expected `{ groups: [...] }` shape

## Dependencies
- Depends on: Task 2 — Implement license compliance report service
