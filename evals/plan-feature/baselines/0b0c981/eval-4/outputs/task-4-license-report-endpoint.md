## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that returns a structured license compliance report for a given SBOM. The endpoint delegates to the license report service and returns the grouped license data with compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (which now include license-report) are mounted (likely already handled by existing SBOM route registration)

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report grouped by license type with compliance flags. Response shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Use Axum extractors for the SBOM `{id}` path parameter
  - Return `Result<Json<LicenseReport>, AppError>` with `.context()` error wrapping
  - Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same pattern as existing GET routes
- The handler should:
  1. Extract the SBOM ID from the path
  2. Call `LicenseReportService::generate_report(sbom_id)` from Task 3
  3. Return the LicenseReport as JSON
- No pagination needed — the report returns all license groups for the SBOM
- No caching needed for the initial implementation; can be added later if performance requires it
- Per docs/constraints.md §5.3: follow the patterns referenced in Implementation Notes (Axum handler pattern from existing endpoints)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the Axum handler pattern for GET /api/v2/sbom/{id} with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows route registration pattern to follow
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseReport JSON body
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Response shape matches: `{ "groups": [{ "license": string, "packages": [...], "compliant": boolean }] }`
- [ ] Route is registered and accessible through the server

## Test Requirements
- [ ] Integration test: call endpoint with a valid SBOM ID and verify 200 response with correct JSON shape
- [ ] Integration test: call endpoint with non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify compliance flags are correctly set in the response based on license policy

## Verification Commands
- `cargo test --test api` — run integration tests to verify endpoint behavior

## Documentation Updates
- `README.md` — Add the new license-report endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 3 — License report service

[sdlc-workflow] Description digest: sha256:fa671e0ec82ffa599cf33e10dbfc6ee696b50a24391aee7e67c5536e077f161d
