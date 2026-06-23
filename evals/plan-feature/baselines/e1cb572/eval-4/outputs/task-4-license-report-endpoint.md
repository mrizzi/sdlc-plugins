# Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint for generating license compliance reports. The endpoint accepts an SBOM ID as a path parameter, loads the license policy, invokes the license report service to generate the report, and returns the structured JSON response. This is the user-facing API that compliance officers and CI/CD pipelines will call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/license-report` route under the existing `/api/v2/sbom` router
- `server/src/main.rs` — No changes expected if the SBOM module's routes are already mounted; verify during implementation

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, grouped by license type with compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [{ "name": "serde", "version": "1.0", "transitive": false }], "compliant": true }] }`

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it demonstrates path parameter extraction (`Path<Id>`), service invocation, and JSON response return for a single-resource GET endpoint.
- Route registration pattern: see `modules/fundamental/src/sbom/endpoints/mod.rs` for how routes are registered under the SBOM router. Add the new route as `.route("/{id}/license-report", get(license_report))`.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the `LicensePolicy` from the configured path (consider using Axum's `State` or `Extension` extractor for the policy, initialized at startup in `server/src/main.rs`)
  3. Call `LicenseReportService::generate_report()` to produce the report
  4. Return the `LicenseReportResponse` as JSON
- Error handling: return `Result<Json<LicenseReportResponse>, AppError>` following the pattern in all existing endpoint handlers. Non-existent SBOM should return 404.
- Do not add caching for now — the feature description does not mention caching requirements, and report data may change as the license policy changes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern for `GET /api/v2/sbom/{id}` (path parameter extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for the SBOM module
- `common/src/error.rs::AppError` — Consistent error responses with `.context()` wrapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing grouped license data
- [ ] Response body matches the specified shape: `{ "groups": [{ "license": "...", "packages": [...], "compliant": bool }] }`
- [ ] Non-existent SBOM ID returns 404 with an appropriate error message
- [ ] The endpoint is registered and accessible through the Axum router

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 for a valid SBOM with expected license groups
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 404 for non-existent SBOM
- [ ] Integration test: response body has correct shape with `groups`, `license`, `packages`, and `compliant` fields

## Verification Commands
- `cargo test -p fundamental` — endpoint handler tests pass
- `cargo build` — project compiles with new endpoint

## Dependencies
- Depends on: Task 3 — Add license report service with dependency resolution and compliance evaluation

[sdlc-workflow] Description digest: sha256-md:d33fcee259e7623dd886279f02fa79a0bde949970962bd3ebe399749be5645ed