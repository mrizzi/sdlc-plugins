## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint handler that invokes the license report service and returns the structured JSON response. Register the route in the SBOM endpoint module and mount it in the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function:
  - Extract the SBOM `id` from the path parameter
  - Load the `LicensePolicy` (from config or injected state)
  - Call the license report service to generate the report
  - Return the `LicenseReport` as a JSON response with `StatusCode::OK`
  - Return `StatusCode::NOT_FOUND` if the SBOM does not exist

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod license_report;` and register the `GET /api/v2/sbom/{id}/license-report` route in the router builder, following the pattern used by existing routes in `list.rs` and `get.rs`
- `server/src/main.rs` — No changes expected if the SBOM module is already mounted, but verify the SBOM routes are registered

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response handling
- The handler signature should match Axum conventions: `async fn get_license_report(Path(id): Path<String>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>`
- The `LicensePolicy` should be loaded once and stored in the application state (or loaded per-request from a cached source) to meet the p95 < 500ms performance requirement
- The route path is `/api/v2/sbom/{id}/license-report` — this is a sub-resource of the existing SBOM routes
- No new database tables are needed — the service aggregates from existing entity tables

Per CONVENTIONS.md: All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs`.

Per CONVENTIONS.md: Endpoint registration goes in each module's `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` to register the new route.

## Acceptance Criteria
- `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body for an existing SBOM
- `GET /api/v2/sbom/{id}/license-report` returns 404 for a non-existent SBOM ID
- Response content-type is `application/json`
- The endpoint is accessible at the documented path and discoverable via OpenAPI spec if applicable

## Test Requirements
- Endpoint handler tests are covered in Task 5 (integration tests)
- Verify route registration by confirming the handler compiles and the route is reachable

## Dependencies
- Depends on: Task 3 — License Report Service (needs the service to generate the report)

[sdlc-workflow] Description digest: sha256-md:f9231c0db419ee9319295948c8e066f3e4a55b8c77aa944f14f9ba1a4215990a
