## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint handler that invokes the license report service and returns the compliance report as a JSON response. Register the new route in the SBOM endpoint module so it is mounted alongside existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Endpoint handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod license_report;` and register the new route in the router
- `server/src/main.rs` — Only if the SBOM module routes are not already auto-mounted; verify existing mount point covers the new sub-route

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseComplianceReport` JSON response containing packages grouped by license with compliance flags

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (for `GET /api/v2/sbom/{id}`). The handler should:

1. Extract the SBOM `{id}` path parameter using Axum's `Path` extractor.
2. Obtain a database connection from the application state (follow the pattern in existing endpoint handlers).
3. Call the license report service method from Task 2.
4. Return the `LicenseComplianceReport` as `Json<LicenseComplianceReport>` with `StatusCode::OK`.
5. Handle errors by returning `AppError` (which implements `IntoResponse` per `common/src/error.rs`).

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should add the route as a nested route under the existing `/api/v2/sbom` prefix, e.g.: `.route("/:id/license-report", get(license_report::handler))`.

Verify that `server/src/main.rs` already mounts the fundamental module's SBOM routes -- if so, no change to `main.rs` is needed as the new route will be picked up automatically.

Note: This endpoint returns a single report object, not a paginated list, so `PaginatedResults<T>` from `common/src/model/paginated.rs` is NOT used here.

Per CONVENTIONS.md (Key Conventions from repository structure): each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` and modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md (Key Conventions from repository structure): all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET handler; reuse the path parameter extraction, state access, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern; follow the same `.route()` chaining approach
- `common/src/error.rs::AppError` — Error type with `IntoResponse`; use as the error return type

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON `LicenseComplianceReport` body
- [ ] Response body contains `groups` array with `license`, `packages`, and `compliant` fields
- [ ] Invalid/non-existent SBOM ID returns appropriate error status (404)
- [ ] Route is registered in the SBOM endpoints module and accessible through the server
- [ ] Endpoint follows existing authentication/authorization middleware (inherits from SBOM route group)

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with expected report structure
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON matches `LicenseComplianceReport` schema (groups, compliant flags, counts)

## Dependencies
- Depends on: Task 2 — Implement license compliance report service logic

## additional_fields
- labels: ai-generated-jira
- priority: Major
- fixVersions: RHTPA 1.5.0
