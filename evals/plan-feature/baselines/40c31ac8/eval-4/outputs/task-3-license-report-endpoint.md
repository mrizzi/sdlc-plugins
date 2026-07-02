## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for a given SBOM. The endpoint extracts the SBOM ID from the path, calls the license report service, and returns the report as a JSON response. Register the new route in the SBOM endpoint module.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route pointing to the new handler

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the `get_license_report` handler function

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON object containing packages grouped by license type with compliance flags

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction and response formatting. The handler should:
1. Extract the SBOM `id` from the Axum path parameters
2. Call `generate_license_report(id, &db)` from the service layer
3. Return the `LicenseReport` as `Json<LicenseReport>` on success
4. Return appropriate HTTP error codes via `AppError` on failure (404 if SBOM not found, 500 for internal errors)

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the existing pattern used for `get.rs` and `list.rs` routes, adding `.route("/api/v2/sbom/:id/license-report", get(license_report::get_license_report))`.

Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<LicenseReport>, AppError>` and use `.context()` wrapping for all fallible operations. Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: place the endpoint handler in the `endpoints/` subdirectory following the existing `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for Axum handler pattern, path parameter extraction, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` is registered and reachable
- [ ] Handler extracts SBOM ID from path and calls the service layer
- [ ] Successful requests return HTTP 200 with `LicenseReport` JSON body
- [ ] Requests for non-existent SBOMs return HTTP 404
- [ ] Internal errors return HTTP 500 with appropriate error message
- [ ] Code compiles without errors (`cargo check -p trustify-fundamental`)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 2 — Implement license compliance report service

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
