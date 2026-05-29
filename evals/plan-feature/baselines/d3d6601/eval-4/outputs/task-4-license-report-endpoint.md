## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for a given SBOM. The endpoint calls the license report service to aggregate package-license data, group by license type, and flag policy violations. This is the primary API surface for compliance officers and CI/CD pipelines to consume license audit data.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license-report route alongside existing SBOM endpoints
- `server/src/main.rs` — verify the SBOM module routes (including the new endpoint) are mounted (likely already handled by existing module registration)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, with packages grouped by license type and compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
- Follow the existing endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` — the handler extracts the SBOM ID from the path, calls the service, and returns the result as JSON.
- Use `axum::extract::Path` to extract the `{id}` path parameter, matching the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Return `Result<Json<LicenseReport>, AppError>` following the error handling convention in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same pattern as existing routes (e.g., `.route("/:id/license-report", get(license_report))`) — see how `get.rs` is registered for the `GET /:id` route.
- The endpoint should return HTTP 404 when the SBOM ID does not exist, using the `AppError` enum.
- Consider adding `tower-http` caching headers for the response since license reports for an ingested SBOM are deterministic (the report only changes when the SBOM is re-ingested or the policy changes).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the exact handler pattern for `GET /api/v2/sbom/{id}` including path extraction, service invocation, and error responses
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows how routes are registered and the SBOM router is configured
- `common/src/error.rs::AppError` — the error type all handlers return

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` structure
- [ ] Response groups packages by license with `compliant` flags based on configured policy
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Endpoint is properly registered and accessible via the Axum router
- [ ] Transitive dependency licenses are included in the report

## Test Requirements
- [ ] Integration test verifying HTTP 200 and correct JSON structure for a valid SBOM with known package licenses
- [ ] Integration test verifying HTTP 404 for a nonexistent SBOM ID
- [ ] Integration test verifying that non-compliant licenses are correctly flagged in the response
- [ ] Integration test verifying transitive dependencies appear in the report

## Verification Commands
- `cargo build -p trustify-server` — should compile without errors
- `cargo test -p trustify-tests -- license_report` — integration tests pass

## Documentation Updates
- `README.md` — document the new `GET /api/v2/sbom/{id}/license-report` endpoint, its request parameters, and response schema

## Dependencies
- Depends on: Task 1 — Add license compliance report model structs
- Depends on: Task 3 — Implement license report service logic

[sdlc-workflow] Description digest: sha256:2218c0e3c308f10359367f6456e8fc1b0d1bd4f5ac9330d3d4acfa9ce0cea803
