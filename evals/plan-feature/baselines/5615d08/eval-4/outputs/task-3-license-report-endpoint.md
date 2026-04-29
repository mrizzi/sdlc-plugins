## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that exposes the license compliance report to API consumers. This endpoint wires the license report service into the Axum router, handling request parsing, service invocation, and JSON response serialization. This completes the API surface for TC-9004.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID path parameter, calls `LicenseReportService` to generate the report, and returns the `LicenseReport` as a JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the new route in the SBOM router alongside existing routes (following the pattern used for `list.rs` and `get.rs`)
- `server/src/main.rs` — No changes needed if the SBOM module router is already mounted (verify this)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license and compliance flags based on the configured license policy

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract the SBOM ID from the path using Axum's `Path<String>` extractor, obtain the database connection from the application state, and call the service layer.
- The handler signature should be: `async fn license_report(Path(id): Path<String>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>` — matching the `Result<T, AppError>` pattern used across all handlers (see `common/src/error.rs`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding `.route("/{id}/license-report", get(license_report::handler))` to the existing SBOM router, following the same pattern as the `/{id}` route for `get.rs`.
- The `LicensePolicy` should be loaded once at application startup and stored in the Axum application state (or loaded lazily and cached). If modifying `AppState` is too invasive for this task, the handler can load the policy file on each request as an initial implementation, with a TODO for caching optimization.
- Return appropriate HTTP status codes: `200 OK` for a successful report, `404 Not Found` for a non-existent SBOM ID (propagated from the service layer via `AppError`).
- The JSON response shape should match the requirements: `{ "sbom_id": "...", "generated_at": "...", "groups": [{ "license": "MIT", "packages": [...], "compliant": true }], "summary": { "total": N, "compliant": N, "non_compliant": N } }`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Direct pattern to follow for path parameter extraction, state access, and response formatting
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to extend
- `common/src/error.rs::AppError` — Error handling and `IntoResponse` implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns `200 OK` with a JSON license compliance report
- [ ] Response JSON contains `groups` array with each group having `license`, `packages`, and `compliant` fields
- [ ] Response JSON contains `summary` with `total`, `compliant`, and `non_compliant` counts
- [ ] Returns `404 Not Found` for a non-existent SBOM ID
- [ ] Endpoint is registered under the existing `/api/v2/sbom` route prefix
- [ ] No new backdoor, debug, or admin endpoints are added

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/license-report` for a valid SBOM returns 200 with expected JSON structure
- [ ] Integration test: GET request for a non-existent SBOM ID returns 404
- [ ] Integration test: Response groups contain correct compliance flags based on the license policy
- [ ] Integration test: Response summary counts are consistent with the groups data

## Verification Commands
- `cargo build -p fundamental` — Module builds without errors
- `cargo test -p fundamental -- license_report` — All license report tests pass

## Dependencies
- Depends on: Task 2 — License report model and service (provides `LicenseReportService` and `LicenseReport`)
