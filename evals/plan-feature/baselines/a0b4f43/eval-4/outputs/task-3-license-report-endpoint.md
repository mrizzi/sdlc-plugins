## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` endpoint that generates and returns a license compliance report for the specified SBOM. The endpoint invokes the LicenseReportService to aggregate package-license data, apply the configured license policy, and return a structured JSON response with packages grouped by license type and compliance flags.

## Files to Create
- `modules/fundamental/src/license_report/endpoints/mod.rs` — Route registration for `/api/v2/sbom/{id}/license-report`, following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`
- `modules/fundamental/src/license_report/endpoints/report.rs` — Handler function for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/license_report/mod.rs` — Add `pub mod endpoints;` to register the endpoints sub-module
- `server/src/main.rs` — Mount the license report routes alongside existing module routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ sbom_id: UUID, generated_at: DateTime, groups: [{ license: String, packages: [PackageSummary], compliant: bool }], policy_violations: number }`

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function. Handlers extract path parameters with `Path<Uuid>`, inject services via Axum state, and return `Result<Json<T>, AppError>`.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — routes are registered as a function returning a `Router` and mounted in `server/src/main.rs`.
- The handler should:
  1. Extract the SBOM ID from the path parameter
  2. Load the `LicensePolicy` from the configured policy file path
  3. Call `LicenseReportService::generate_report(db, sbom_id, &policy)`
  4. Return the `LicenseReport` as JSON
- Return 404 with an appropriate `AppError` if the SBOM does not exist.
- Return 200 with the `LicenseReport` JSON on success.
- Consider caching via `tower-http` caching middleware for repeated report requests on the same SBOM, following the pattern used by existing endpoint route builders.
- Per `docs/constraints.md` §5 (Code Change Rules): Changes must be scoped to the files listed. Implementation must follow the patterns referenced in these notes.
- Per `docs/constraints.md` §2 (Commit Rules): Every commit must reference TC-9004 in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per `docs/constraints.md` §3 (PR Rules): The branch must be named after the Jira issue ID, and PR link must be posted to Jira after opening.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Existing SBOM route registration; follow the same Router pattern for the license report routes
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler for SBOM details; follow the same handler pattern (Path extraction, service injection, JSON response)
- `common/src/error.rs::AppError` — Existing error handling; reuse for 404 and 500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid JSON license report
- [ ] Response contains `groups` array with packages grouped by license and `compliant` flags
- [ ] Response contains `policy_violations` count matching the number of non-compliant groups
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] The endpoint is accessible via the Axum router (mounted in `server/src/main.rs`)

## Test Requirements
- [ ] Integration test: GET request to `/api/v2/sbom/{id}/license-report` with a valid SBOM returns 200 and a well-formed report
- [ ] Integration test: GET request with a non-existent SBOM ID returns 404
- [ ] Integration test: Report correctly reflects license policy compliance flags (test with a known policy and known package licenses)

## Verification Commands
- `cargo test --test api -- license_report` — All license report integration tests pass
- `cargo build` — Project compiles without errors

## Documentation Updates
- `README.md` — Add the new license report endpoint to the API endpoint listing

## Dependencies
- Depends on: Task 1 — License report model and policy (provides model types)
- Depends on: Task 2 — License report service (provides the report generation logic)
