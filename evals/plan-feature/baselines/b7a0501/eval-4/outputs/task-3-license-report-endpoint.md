# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a structured license compliance report for the specified SBOM. The endpoint loads the license policy, delegates to `LicenseReportService` (Task 2), and returns the grouped license data with compliance flags. This is the primary user-facing API for the license compliance feature.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`; extracts SBOM ID from path, loads policy, calls `LicenseReportService::generate_report()`, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes; add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "..." }], compliant: true }] }` with `200 OK` on success, `404 Not Found` for invalid SBOM ID

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` for handler signature, path parameter extraction, error handling, and response serialization
- The handler should accept `Path<Uuid>` for the SBOM ID parameter and return `Result<Json<LicenseReport>, AppError>`
- Load the `LicensePolicy` from the config file (consider injecting it as application state via Axum's `Extension` or `State` extractor, similar to how the database connection is injected)
- Route registration in `endpoints/mod.rs` should follow the existing pattern: add a `.route("/api/v2/sbom/:id/license-report", get(license_report::handler))` alongside existing SBOM routes
- Per constraints doc section 2.1: commits must reference TC-9004 in the footer
- Per constraints doc section 3.1: feature branch must be named after the Jira issue ID
- Per constraints doc section 5.3: follow patterns referenced in Implementation Notes

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for handler pattern, path extraction, error handling, and response shape
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error handling with `IntoResponse` implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with grouped license data for a valid SBOM
- [ ] Response body matches the schema: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Returns 404 for non-existent SBOM IDs
- [ ] Endpoint is registered and accessible through the Axum router
- [ ] Error responses use the standard `AppError` format

## Test Requirements
- [ ] Handler returns 200 with correct response shape for a valid SBOM
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response JSON matches expected schema

## Dependencies
- Depends on: Task 2 — Add license report service with transitive dependency resolution
