# Task 4 — Add license report REST endpoint and integration tests

## Repository
trustify-backend

## Description
Expose the license compliance report as a REST endpoint at `GET /api/v2/sbom/{id}/license-report`. This endpoint calls the license report service (Task 3) and returns the grouped license compliance data as JSON. Also add integration tests covering the full request-response cycle for compliant SBOMs, non-compliant SBOMs, transitive dependencies, and error cases.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new license report route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler for `GET /api/v2/sbom/{id}/license-report`
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns a license compliance report for the specified SBOM, with response shape `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in the SBOM module. See `modules/fundamental/src/sbom/endpoints/get.rs` for the handler pattern: extracting path parameters, calling the service, returning JSON with proper error handling.
- The handler should:
  1. Extract the SBOM `{id}` from the path
  2. Call the license report service method (from Task 3)
  3. Return the `LicenseReport` as JSON with `StatusCode::OK`
  4. Return appropriate error responses (404 for non-existent SBOM, 500 for internal errors)
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for the existing `list.rs` and `get.rs` routes. The route should be nested under the SBOM path: `.route("/api/v2/sbom/:id/license-report", get(license_report))`.
- All handlers return `Result<T, AppError>` with `.context()` wrapping, per `common/src/error.rs`.
- For integration tests, follow the pattern in `tests/api/sbom.rs`: use real PostgreSQL test database, set up test SBOM data with packages and licenses, call the endpoint, and assert on response status and body.
- Test cases should cover:
  - An SBOM with all-compliant licenses returns 200 with all groups marked `compliant: true`
  - An SBOM with a non-compliant license returns 200 with the violating group marked `compliant: false`
  - An SBOM with transitive dependencies includes those dependencies in the report
  - A request for a non-existent SBOM ID returns 404
- The `tests/Cargo.toml` may need to be updated to include any new test utilities or dependencies.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; follow its pattern for path extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `tests/api/sbom.rs` — existing SBOM integration tests; follow their test setup, assertion patterns, and database seeding approach
- `common/src/error.rs::AppError` — error type for handler error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body matching the `LicenseReport` schema
- [ ] Response groups packages by license with correct `compliant` flags
- [ ] Transitive dependency licenses are included in the report
- [ ] Non-existent SBOM ID returns 404
- [ ] Endpoint is registered and accessible through the server's route tree
- [ ] All integration tests pass

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` for a compliant SBOM returns 200 with all groups marked compliant
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` for a non-compliant SBOM returns 200 with violating groups flagged
- [ ] Integration test: report includes packages from transitive dependencies
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent-id}/license-report` returns 404
- [ ] Integration test: response JSON shape matches `{ "groups": [{ "license": "...", "packages": [...], "compliant": bool }] }`

## Verification Commands
- `cargo test -p trustify-tests --test license_report` — integration tests pass
- `cargo check` — full project compiles without errors

## Documentation Updates
- `README.md` — document the new `GET /api/v2/sbom/{id}/license-report` endpoint, its request parameters, response schema, and usage examples for compliance teams and CI/CD pipelines

## Dependencies
- Depends on: Task 3 — Add license report service logic
