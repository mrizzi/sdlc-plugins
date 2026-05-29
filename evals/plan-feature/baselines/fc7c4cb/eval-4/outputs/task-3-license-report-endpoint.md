## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that generates and returns a license compliance report for the specified SBOM. The endpoint invokes the `LicenseReportService` to produce the report and returns it as a JSON response. This is the user-facing entry point for the license compliance report feature.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license report route alongside existing SBOM routes (`/api/v2/sbom`)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — implement the `GET /api/v2/sbom/{id}/license-report` handler function

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON response with structure `{ sbom_id, groups: [{ license: "MIT", packages: [...], compliant: true }], policy_violations: N, generated_at: "..." }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler) for function signature, path parameter extraction, dependency injection, and response construction.
- The handler should extract the SBOM ID from the path parameter, load the license policy (via the policy loader from Task 1), call `LicenseReportService::generate_report`, and return the result as JSON.
- Return `Result<Json<LicenseReport>, AppError>` following the error handling convention used throughout the codebase (see `common/src/error.rs`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs` route registration. The route should be nested under the existing `/api/v2/sbom` router.
- The endpoint does not use `PaginatedResults<T>` since the report is a single aggregated response, not a list. Return the `LicenseReport` directly.
- Verify that the route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` properly connects to the server route mounting in `server/src/main.rs`. The existing SBOM module registration should automatically include the new sub-route — confirm this is the case.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — direct reference for handler function pattern, path parameter extraction, and response type
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for handler return value

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReport` JSON body for an existing SBOM with package data
- [ ] The response JSON contains `groups` array with packages grouped by license and `compliant` flags
- [ ] The endpoint returns HTTP 404 (or appropriate error) when the SBOM ID does not exist
- [ ] The route is registered and accessible through the Axum server without additional server configuration changes
- [ ] Response time is within acceptable bounds for the p95 < 500ms target on SBOMs with up to 1000 packages

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 and valid JSON for an SBOM with known package-license data
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent}/license-report` returns 404 or appropriate error
- [ ] Integration test: response JSON structure matches the `LicenseReport` schema (has `groups`, each group has `license`, `packages`, `compliant`)
- [ ] Integration test: non-compliant licenses are correctly flagged in the response based on the loaded policy

## Dependencies
- Depends on: Task 1 — License report models and policy configuration
- Depends on: Task 2 — License report service

[sdlc-workflow] Description digest: sha256:91b65fa0b13f4dc79ca117e1915725fd2acb145db818acd485234d45fa69dd4b
