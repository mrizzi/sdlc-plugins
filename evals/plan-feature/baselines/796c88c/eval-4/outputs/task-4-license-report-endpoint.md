## Repository
trustify-backend

## Target Branch
main

## Description
Implement the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` that exposes the license compliance report to API consumers. The endpoint loads the license policy configuration, invokes the license report service, and returns the structured JSON response. This task wires together the policy model, response models, and service logic into a functional API endpoint.

## Files to Modify
- `modules/fundamental/sbom/endpoints/mod.rs` -- Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/sbom/endpoints/license_report.rs` -- Endpoint handler:
  - `async fn get_license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>`
  - Loads `LicensePolicy` from the configured JSON file path
  - Calls `LicenseReportService::generate_report(id, &db, &policy)`
  - Returns `Json(report)` with HTTP 200
  - Returns HTTP 404 if SBOM not found

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license and compliance flags

## Implementation Notes
- Follow the pattern in `modules/fundamental/sbom/endpoints/get.rs` for handler signature, state extraction, and error handling
- Route registration should follow the pattern in `modules/fundamental/sbom/endpoints/mod.rs` -- add the new route alongside existing `.route("/:id", get(get_sbom))` style registrations
- The endpoint path should be nested under the existing SBOM routes: `/api/v2/sbom/{id}/license-report`
- Consider caching the `LicensePolicy` in application state rather than reading from disk on every request, using the existing `tower-http` caching patterns
- Set appropriate `Cache-Control` headers -- the report is derived data that can be cached for a short period (e.g., 60 seconds)
- Return `Content-Type: application/json`
- If OpenAPI documentation is generated (check existing endpoints), add `#[utoipa::path]` annotation with request/response schema documentation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON response
- [ ] Returns HTTP 404 with appropriate error body when the SBOM ID does not exist
- [ ] Response JSON matches the schema defined in Task 2
- [ ] License policy is loaded from the configured file path
- [ ] Route is properly registered and discoverable alongside other SBOM endpoints

## Test Requirements
- [ ] Handler test: valid SBOM ID returns 200 with correctly structured JSON
- [ ] Handler test: non-existent SBOM ID returns 404
- [ ] Handler test: response contains expected fields (sbom_id, groups, counts)

## Dependencies
- Depends on: Task 3 -- Implement license report service
