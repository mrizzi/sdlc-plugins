## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that generates and returns a license compliance report for a given SBOM. This endpoint exposes the LicenseReportService to API consumers, enabling compliance officers and CI/CD pipelines to retrieve structured license audit data.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID from the path, calls LicenseReportService.generate_report(), and returns the LicenseReport as a JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod license_report;` and register the new route in the SBOM router alongside existing routes (list, get)
- `server/src/main.rs` — No changes expected if the SBOM module's route registration is already mounted; verify that the SBOM endpoint module is included in the server's route tree

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license and compliance flags based on the configured policy. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function structure: extract path parameters using Axum's `Path<Uuid>` extractor, obtain the database connection from the application state, call the service method, and return `Json(report)` wrapped in a Result
- Route registration should follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add a `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))` call to the existing SBOM router
- The handler function signature should be: `pub async fn handler(Path(id): Path<Uuid>, State(db): State<DatabaseConnection>) -> Result<Json<LicenseReport>, AppError>`
- Error handling: return `AppError` for invalid SBOM IDs or service errors, following the pattern in `common/src/error.rs`
- The endpoint must go through the same authentication/authorization middleware as other SBOM endpoints — no special authentication bypass or debug access
- Per constraints doc section 5.1: changes must be scoped only to the files listed above — no unrelated modifications
- Per constraints doc section 5.3: follow the patterns referenced in these implementation notes

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the exact handler pattern to follow (path extraction, state access, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — demonstrates how to register new routes in the SBOM module router
- `modules/fundamental/src/advisory/endpoints/get.rs` — another example of the single-entity GET handler pattern for cross-referencing

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the LicenseReport schema for a valid SBOM ID
- [ ] The endpoint returns an appropriate error response (HTTP 404) for a non-existent SBOM ID
- [ ] The endpoint is registered under the SBOM module's route tree and accessible through the server
- [ ] The endpoint uses the same authentication/authorization middleware as other SBOM endpoints
- [ ] Response JSON contains `groups` array where each entry has `license` (string), `packages` (array), and `compliant` (boolean) fields

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/license-report` returns 200 with correct JSON structure for an SBOM with known packages and licenses
- [ ] Integration test: GET request with a non-existent SBOM ID returns 404
- [ ] Integration test: Response body correctly groups packages by license
- [ ] Integration test: Compliance flags in the response match the configured license policy

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{test-sbom-id}/license-report | jq .` — returns well-formed JSON with groups array

## Dependencies
- Depends on: Task 2 — License report service layer
