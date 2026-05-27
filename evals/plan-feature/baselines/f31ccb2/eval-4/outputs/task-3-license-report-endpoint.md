## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report grouped by license type with policy violation flags. This endpoint exposes the license report service through the REST API, enabling compliance teams and CI/CD pipelines to retrieve license audit data for any ingested SBOM.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for `GET /api/v2/sbom/{id}/license-report` that calls the LicenseReportService and returns the report as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `modules/fundamental/Cargo.toml` — Add any additional dependencies needed for the endpoint (if not already present)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a JSON response with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }], total_packages: N, non_compliant_count: N }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure. The handler should accept the SBOM ID as a path parameter, invoke the `LicenseReportService`, and return the result as JSON.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where routes are registered using Axum's router builder. Add the license report route as a nested route under the existing `/api/v2/sbom/{id}` path.
- The handler should return `Result<Json<LicenseReport>, AppError>` consistent with all other endpoint handlers in the project.
- If the SBOM ID does not exist, return a 404 error using the existing `AppError` pattern from `common/src/error.rs`.
- Consider adding `tower-http` caching middleware configuration for this endpoint, following the caching pattern used by other endpoint route builders in the project.
- Per CONVENTIONS.md §Error Handling: the handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET endpoint handler demonstrating the handler pattern, path parameter extraction, and error response handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow when adding the new route
- `common/src/error.rs::AppError` — Error handling enum with `IntoResponse` implementation for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with a JSON body containing `groups`, `total_packages`, and `non_compliant_count` fields
- [ ] Each group in `groups` contains `license` (string), `packages` (array), and `compliant` (boolean) fields
- [ ] The endpoint returns 404 when the SBOM ID does not exist
- [ ] The endpoint follows the project's Axum handler pattern returning `Result<Json<LicenseReport>, AppError>`
- [ ] The route is registered in the SBOM endpoints module and accessible through the API

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 with correct JSON structure for a valid SBOM
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 404 for a non-existent SBOM ID
- [ ] Integration test: the response correctly groups packages by license and flags non-compliant licenses
- [ ] Integration test: the response includes transitive dependency packages in the license groups

## Verification Commands
- `cargo test --test api` — all integration tests pass including new license report tests
- `cargo build` — full project compiles without errors

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
