# Task 4: Add license report endpoint handler

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` that invokes the LicenseReportService and returns the license compliance report as a JSON response. Register the route in the SBOM module's route configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route

## Implementation Notes
- Follow the existing endpoint handler pattern from `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}):
  - Extract the SBOM ID from the path using Axum's `Path<Uuid>` extractor
  - Inject `LicenseReportService` via Axum's state/extension mechanism (same pattern as `SbomService` injection in existing handlers)
  - Call `service.generate_report(id)` and return `Json(report)` on success
  - Return `AppError` on failure — the `IntoResponse` impl in `common/src/error.rs` handles error serialization
- In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the route using the same registration pattern as the existing `get.rs` handler:
  - Add `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))` to the router
- The handler function signature should follow the pattern:
  ```rust
  pub async fn handler(
      Path(id): Path<Uuid>,
      State(service): State<LicenseReportService>,
  ) -> Result<Json<LicenseReport>, AppError>
  ```
- Ensure the endpoint is authenticated using the same middleware applied to other SBOM endpoints (no special auth bypass).

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseReport` body for a valid SBOM
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns appropriate error status for server errors
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Endpoint follows existing authentication and middleware patterns (no auth bypass)
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct JSON structure
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: response JSON contains `groups` array with `license`, `packages`, and `compliant` fields

## Dependencies
- Depends on: Task 3 — Implement license report service
