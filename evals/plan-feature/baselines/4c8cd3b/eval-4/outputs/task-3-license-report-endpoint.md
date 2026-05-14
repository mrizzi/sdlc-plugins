## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that generates and returns a license compliance report for the specified SBOM. The endpoint loads the license policy configuration, invokes the `LicenseReportService`, and returns the structured `LicenseReport` response. Register the new route in the SBOM endpoint module and ensure it is mounted in the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that extracts the SBOM ID from the path, loads the license policy, calls `LicenseReportService::generate_report()`, and returns the `LicenseReport` as JSON
- `license-policy.json` — Default license policy configuration file at the repository root with a starter set of common SPDX license rules (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause as allowed; GPL-2.0-only, GPL-3.0-only as denied)

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add route registration for `GET /api/v2/sbom/{id}/license-report` pointing to the new handler; add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ "groups": [{ "license": "MIT", "packages": [PackageSummary, ...], "compliant": true }, ...] }`

## Implementation Notes
- **Endpoint pattern:** Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting the SBOM ID from the Axum path parameter. The handler signature should follow the same pattern: `async fn license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>`.
- **Route registration:** In `modules/fundamental/src/sbom/endpoints/mod.rs`, register the new route alongside the existing `/api/v2/sbom/{id}` GET route. Follow the pattern used for `get.rs` route registration — the existing `mod.rs` file already registers routes for `list.rs` and `get.rs`.
- **Policy loading:** Load the license policy from the file system using `LicensePolicy::load()` from Task 1. The policy file path should be configurable (e.g., via an environment variable or application state), but default to `license-policy.json` at the repository root.
- **Error handling:** Return `Result<Json<LicenseReport>, AppError>` following the convention in `common/src/error.rs`. Map service errors and policy loading errors into appropriate HTTP status codes (404 for missing SBOM, 500 for policy loading failures).
- **Response serialization:** Return `Json(report)` where `report` is the `LicenseReport` struct. Axum will serialize it automatically via serde.
- **No caching initially:** Do not add caching for the first iteration. The p95 < 500ms target for 1000 packages should be achievable without caching. Caching can be added as a follow-up if needed.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET handler demonstrating path parameter extraction, state access, service invocation, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Existing route registration showing how to wire handlers into the Axum router
- `common/src/error.rs::AppError` — Error type with `IntoResponse` implementation for converting service errors to HTTP responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` structure
- [ ] The response groups packages by license identifier with correct compliance flags
- [ ] The endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] The endpoint returns HTTP 500 with a meaningful error when the license policy file cannot be loaded
- [ ] The route is registered in the SBOM endpoint module and reachable through the server
- [ ] A default `license-policy.json` file exists at the repository root with starter rules

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/{id}/license-report` for an ingested SBOM and verify HTTP 200 with correct response structure
- [ ] Integration test: call the endpoint with a nonexistent SBOM ID and verify HTTP 404
- [ ] Integration test: verify the response contains packages grouped by license with `compliant` flags matching the policy

## Documentation Updates
- `README.md` — Add documentation for the new `GET /api/v2/sbom/{id}/license-report` endpoint including request/response examples and license policy configuration instructions

## Dependencies
- Depends on: Task 1 — License policy configuration and report models
- Depends on: Task 2 — License compliance report service
