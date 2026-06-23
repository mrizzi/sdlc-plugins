# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for a given SBOM. The endpoint loads the license policy, invokes the `LicenseReportService`, and returns the grouped license data with compliance flags as JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `server/src/main.rs` — no changes expected if route registration follows the existing module mounting pattern, but verify

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler function `get_license_report(Path(id): Path<Uuid>, ...) -> Result<Json<LicenseReport>, AppError>` that loads the policy, calls `LicenseReportService::generate_report`, and returns the result

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: "MIT", packages: [{ name: "serde", version: "1.0" }], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it demonstrates how to extract path parameters, call a service, and return JSON responses with proper error handling.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as existing routes (e.g., `list.rs`, `get.rs`).
- The handler should load the `LicensePolicy` from the configured path. Consider accepting the policy as application state (via Axum's `Extension` or `State` extractor) initialized at startup in `server/src/main.rs`.
- Return `Result<Json<LicenseReport>, AppError>` consistent with all other endpoint handlers.
- Performance: the p95 target is <500ms for SBOMs with up to 1000 packages. The service query should be efficient — avoid N+1 queries by joining package-license data in a single query.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per constraints doc section 3 (PR Rules): name the branch after the Jira issue ID; post the PR link as a comment on the Jira task.
- Per constraints doc section 5 (Code Change Rules): scope changes to listed files; inspect code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the same handler function pattern (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — follow the route registration pattern for adding the new endpoint
- `common/src/error.rs::AppError` — use for all error responses, with `.context()` wrapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a JSON body containing license groups
- [ ] Each license group includes the license name, list of packages, and a `compliant` boolean
- [ ] Non-existent SBOM IDs return 404
- [ ] Response time is within p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with grouped license data
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with mixed compliant and non-compliant licenses returns correct compliance flags
- [ ] Integration test: SBOM with no packages returns an empty groups array

## Verification Commands
- `cargo test --test api -- license_report` — run license report integration tests
- `curl http://localhost:8080/api/v2/sbom/{id}/license-report` — manual verification of endpoint response

## Dependencies
- Depends on: Task 2 — Add LicenseReportService to aggregate licenses and evaluate compliance

[sdlc-workflow] Description digest: sha256-md:82dee127188efd67ef544931f904659d8b2a3cc8087fcfbad0f11054973f2a68
