## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance report for a given SBOM. The endpoint invokes the LicenseReportService (from Task 2) and returns the structured report as JSON. This endpoint enables compliance teams and CI/CD pipelines to retrieve license audit data with a single API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route and add `pub mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a LicenseReport JSON response containing packages grouped by license with compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler signature, path parameter extraction, service invocation, and JSON response construction.
- The handler should:
  1. Extract the SBOM `{id}` from the path parameters
  2. Obtain a database connection from the application state
  3. Call `LicenseReportService::generate_report(db, sbom_id)` (from Task 2)
  4. Return the LicenseReport as `Json<LicenseReport>` on success
  5. Return appropriate HTTP error codes: 404 if the SBOM does not exist, 500 for internal errors
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used to register the existing `get` and `list` routes.
- The endpoint should be mounted under the existing `/api/v2/sbom` route prefix — it is a sub-resource of a specific SBOM.
- Per constraints (Section 2, Commit Rules): use Conventional Commits format with Jira issue ID in footer.
- Per constraints (Section 3, PR Rules): name the branch after the Jira issue ID and post the PR link to the task.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler for SBOM details; follow the same pattern for path extraction, service call, and response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow when mounting the new route
- `common/src/error.rs::AppError` — standard error type implementing IntoResponse; use for error returns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseReport JSON response for an existing SBOM
- [ ] The endpoint returns 404 for a non-existent SBOM ID
- [ ] The response groups packages by license and includes `compliant` flags
- [ ] The route is properly registered and discoverable at the expected path

## Test Requirements
- [ ] Integration test: GET request returns 200 with correctly structured license report for a seeded SBOM with known licenses
- [ ] Integration test: GET request returns 404 for non-existent SBOM ID
- [ ] Integration test: report correctly flags non-compliant licenses when policy marks a license as denied
- [ ] Integration test: report includes transitive dependency licenses

## Verification Commands
- `cargo test --package trustify-tests license_report` — all integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{id}/license-report | jq .` — returns valid JSON with groups array

## Documentation Updates
- `README.md` — add license report endpoint to the API overview section

## Dependencies
- Depends on: Task 2 — Implement LicenseReportService

[sdlc-workflow] Description digest: sha256-md:cfaa52b8dccd546e4c0b12678ee8429b125237b0fe43f44005265ad54d3f7479
