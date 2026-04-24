# Task 4 — Add license report REST endpoint and integration tests

## Repository
trustify-backend

## Description
Expose the license compliance report via a new REST endpoint at `GET /api/v2/sbom/{id}/license-report`. This endpoint loads the license policy configuration, calls the `LicenseReportService`, and returns the structured `LicenseReport` JSON response. This task also adds comprehensive integration tests for the endpoint.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for the license report endpoint
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `GET /api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `tests/Cargo.toml` — Add any additional test dependencies if needed

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM, grouped by license with compliance flags. Response shape: `{ sbom_id: string, groups: [{ license: string, packages: [{ name: string, version: string, transitive: bool }], compliant: bool }], compliant: bool }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it shows the established handler signature, extractor usage, and `Result<Json<T>, AppError>` return type
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — add the new route using `.route("/api/v2/sbom/:id/license-report", get(license_report))` alongside existing SBOM routes
- The handler should:
  1. Extract the SBOM ID from the path using Axum extractors (see `get.rs` for the pattern)
  2. Load the `LicensePolicy` from the configured path (consider injecting via Axum state/extension)
  3. Call `LicenseReportService::generate()` with the database connection, SBOM ID, and policy
  4. Return `Json(report)` on success or propagate `AppError` on failure
- Mount the route in `server/src/main.rs` if the SBOM module route registration does not auto-include it (check the existing mounting pattern)
- Integration tests should follow the pattern in `tests/api/sbom.rs` — use `assert_eq!(resp.status(), StatusCode::OK)` and verify JSON response structure
- Per `docs/constraints.md` Section 2 (Commit Rules): commits must reference TC-9004, follow Conventional Commits, and include the `Assisted-by` trailer
- Per `docs/constraints.md` Section 3 (PR Rules): branch must be named after the Jira issue ID

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler signature, path extractor, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` — additional reference for route registration in a different module
- `server/src/main.rs` — reference for route mounting pattern
- `tests/api/sbom.rs` — reference for integration test setup, assertions, and test database patterns
- `common/src/error.rs::AppError` — error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with correct JSON structure for a valid SBOM
- [ ] Endpoint returns 404 for a nonexistent SBOM ID
- [ ] Response JSON matches the specified shape: `{ sbom_id, groups: [{ license, packages, compliant }], compliant }`
- [ ] License compliance flags in the response correctly reflect the configured policy
- [ ] Transitive dependencies are included in the report
- [ ] Integration tests pass against the test database

## Test Requirements
- [ ] Integration test: request license report for a valid SBOM with known packages and licenses, verify 200 response with correct grouping
- [ ] Integration test: request license report for a nonexistent SBOM, verify 404 response
- [ ] Integration test: verify that non-compliant licenses are flagged correctly in the response
- [ ] Integration test: verify that transitive dependencies appear with `transitive: true`
- [ ] Integration test: verify overall `compliant` field is `false` when any group is non-compliant
- [ ] Integration test: verify empty SBOM (no packages) returns a valid empty report

## Verification Commands
- `cargo test --test api license_report` — All license report integration tests pass
- `cargo clippy --all-targets` — No warnings introduced
- `cargo build` — Project compiles successfully

## Documentation Updates
- `README.md` — Document the new `GET /api/v2/sbom/{id}/license-report` endpoint, including request/response format and license policy configuration

## Dependencies
- Depends on: Task 2 — Add license report response model
- Depends on: Task 3 — Implement license report service with transitive dependency resolution
