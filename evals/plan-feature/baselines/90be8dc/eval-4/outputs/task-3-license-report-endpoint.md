## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license report service and returns the structured compliance report as JSON. Register the route in the SBOM module's endpoint configuration and mount it in the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`; extracts SBOM ID from path, calls the service, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the new route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license type and compliance flags

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (the SBOM ID) and in `modules/fundamental/src/sbom/endpoints/list.rs` for response serialization. The handler function signature should follow the Axum pattern:

```rust
async fn license_report(
    Path(id): Path<Uuid>,
    State(service): State<SbomService>,
) -> Result<Json<LicenseReport>, AppError>
```

Use `.context()` wrapping for errors as documented in `common/src/error.rs::AppError`. Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same `.route()` pattern used for existing SBOM routes. The route should be nested under the existing `/api/v2/sbom` router as `/api/v2/sbom/{id}/license-report`.

Reference `server/src/main.rs` for how module routes are mounted — no changes should be needed there since the SBOM module's routes are already mounted, and this adds a sub-route.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for extracting SBOM ID from path and returning a JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error type with `.context()` wrapping for all handler returns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` schema
- [ ] Response contains `groups` array with each entry having `license`, `packages`, and `compliant` fields
- [ ] Returns HTTP 404 with an error message when the SBOM ID does not exist
- [ ] Returns HTTP 500 with a structured error when service encounters an internal error
- [ ] Route is properly registered and accessible without changes to `server/src/main.rs`

## Verification Commands
- `cargo build -p trustify-module-fundamental` — Compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` — Returns structured JSON with license groups

## Dependencies
- Depends on: Task 2 — Implement license report service logic with dependency tree walking
