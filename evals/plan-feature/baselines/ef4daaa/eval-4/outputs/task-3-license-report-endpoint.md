# Task 3 -- Add License Report Endpoint

## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a license compliance
report for a given SBOM. The endpoint calls the license report service (Task 2) and returns
the structured report as JSON. This is the user-facing API that compliance officers and
CI/CD pipelines will call to check license compliance.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new license-report route
  alongside existing SBOM routes
- `server/src/main.rs` -- ensure the SBOM module routes (including the new endpoint) are mounted
  (likely already handled by existing route registration, but verify)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` -- handler for
  GET /api/v2/sbom/{id}/license-report

## API Changes
- `GET /api/v2/sbom/{id}/license-report` -- NEW: returns license compliance report
  - Response: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
  - 200 OK on success
  - 404 Not Found if SBOM ID does not exist
  - Content-Type: application/json

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`
  for handler structure, parameter extraction, and error handling.
- The handler should:
  1. Extract the SBOM `id` from the path parameters (same pattern as `get.rs`)
  2. Call `LicenseReportService::generate_report(id)` (or equivalent)
  3. Return `Json<LicenseReport>` on success, or propagate `AppError` on failure
- Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow
  the existing pattern for `.route("/api/v2/sbom/:id/...", get(handler))`.
- All handlers return `Result<T, AppError>` with `.context()` wrapping, per the pattern
  in `common/src/error.rs`.
- Per constraints doc section 2: commits must reference TC-9004 and follow Conventional Commits.
- Per constraints doc section 3: branch must be named after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference implementation for single-SBOM
  endpoint handler (path parameter extraction, service call, response pattern)
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow
- `common/src/error.rs::AppError` -- error handling pattern for endpoint responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with correct JSON shape
- [ ] Response body matches: `{ groups: [{ license: string, packages: [...], compliant: bool }] }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Endpoint is registered and accessible via the API router
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Integration test: GET request for a valid SBOM returns 200 with grouped license data
- [ ] Integration test: GET request for non-existent SBOM returns 404
- [ ] Integration test: response JSON shape matches the documented API contract
- [ ] Integration test: SBOM with mixed compliant/non-compliant licenses returns correct flags

## Verification Commands
- `cargo build` -- project compiles without errors
- `cargo test` -- all tests pass including new license report tests

## Documentation Updates
- `README.md` -- add license report endpoint to the API documentation section if one exists

## Dependencies
- Depends on: Task 2 -- Add License Report Service
