# Task 3 — Add license report REST endpoint

## Repository
trustify-backend

## Description
Expose the license report service via a new REST endpoint at `GET /api/v2/sbom/{id}/license-report`. This endpoint returns a structured compliance report with packages grouped by license type and compliance flags. It follows the existing endpoint registration pattern and is mounted as a sub-route of the SBOM module.

## Files to Create
- `modules/fundamental/src/license_report/endpoints/mod.rs` — route registration for the license report endpoint
- `modules/fundamental/src/license_report/endpoints/report.rs` — handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — mount the license report sub-route under the SBOM path
- `server/src/main.rs` — ensure the license report routes are included in the server route tree (if not automatically picked up via the SBOM module mount)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a `LicenseReport` JSON object containing an array of `LicenseGroup` objects, each with a license identifier, list of packages, and a compliance flag

## Implementation Notes
- Follow the existing endpoint pattern. Reference `modules/fundamental/src/sbom/endpoints/get.rs` as the canonical example for a single-resource GET handler under the SBOM path.
- The route registration pattern is demonstrated in `modules/fundamental/src/sbom/endpoints/mod.rs` — new routes are added to the router via `.route()` calls.
- The handler should:
  1. Extract the SBOM ID from the path parameter (`Path<Uuid>` or equivalent).
  2. Inject the `LicenseReportService` (via Axum `State` or `Extension`).
  3. Call the service to generate the report.
  4. Return the `LicenseReport` as JSON with `StatusCode::OK`.
  5. Return appropriate error responses (404 for non-existent SBOM, 500 for internal errors) via the `AppError` pattern.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the codebase error handling convention (see `common/src/error.rs`).
- The endpoint should be nested under the existing SBOM routes since it is a sub-resource of an SBOM (`/api/v2/sbom/{id}/license-report`), not a top-level resource.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the GET handler pattern for fetching a resource by ID under the SBOM path
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows the route registration pattern for SBOM sub-routes
- `modules/fundamental/src/advisory/endpoints/mod.rs` — another example of route registration following the same pattern
- `common/src/error.rs::AppError` — standard error type used by all endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the `LicenseReport` JSON structure
- [ ] The response contains packages grouped by license with compliance flags
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] The endpoint is registered and accessible in the running server
- [ ] Response follows the documented shape: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`

## Test Requirements
- [ ] Integration test: verify 200 response with correct grouping for an SBOM with known package-license data
- [ ] Integration test: verify 404 response for a non-existent SBOM ID
- [ ] Integration test: verify compliance flags are correctly set based on the configured license policy

## Verification Commands
- `cargo test --test api license_report` — run license report integration tests, expect all to pass

## Dependencies
- Depends on: Task 2 — Implement license report model and service
