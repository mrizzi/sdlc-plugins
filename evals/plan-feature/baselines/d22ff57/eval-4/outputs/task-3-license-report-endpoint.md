# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that exposes the license compliance report service. The endpoint accepts an SBOM ID as a path parameter, invokes the license report service, and returns a JSON response with packages grouped by license type and compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Handler function for `GET /api/v2/sbom/{id}/license-report`. Extracts the SBOM ID from the path, calls the license report service, and returns the `LicenseReport` as JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `license-report` route under the existing `/api/v2/sbom` route group. Add `pub mod license_report;`.
- `server/src/main.rs` — Verify the SBOM module routes are mounted (they likely already are); no change needed if the SBOM endpoint module's route registration is already mounted.

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: "MIT", packages: [{ name: "...", version: "...", license: "MIT" }], compliant: true }] }`. Returns 404 if the SBOM ID does not exist. Returns 200 with the report on success.

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}` handler). Mirror the function signature, extractor usage, error handling, and return type.
- Route registration: follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which registers routes for `/api/v2/sbom`. Add the new route as a nested route: `.route("/{id}/license-report", get(license_report::handler))`.
- The handler should accept `Path<Uuid>` (or equivalent SBOM ID type) and an injected service/state, returning `Result<Json<LicenseReport>, AppError>`.
- Error handling: return `AppError` for service errors, consistent with the pattern in `common/src/error.rs`. A 404 response for a missing SBOM should use the same error variant used by the existing `get.rs` handler.
- Consider adding `tower-http` caching headers if appropriate, following the caching middleware pattern described in the repository conventions.
- Per constraints doc section 2, commits must reference TC-9004 in the footer and follow Conventional Commits.
- Per constraints doc section 3, the feature branch must be named after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; follow its extractor and error handling pattern.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for the SBOM module.
- `common/src/error.rs::AppError` — shared error type with `IntoResponse` implementation.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the license report JSON
- [ ] Response body matches the shape: `{ groups: [{ license: string, packages: [...], compliant: boolean }] }`
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Endpoint is registered and accessible under the SBOM route group
- [ ] Error responses follow the existing `AppError` format

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/license-report` returns 200 with correct response shape for an SBOM with known packages and licenses
- [ ] Integration test: endpoint returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes compliance flags correctly set based on the license policy
- [ ] Integration test: response includes packages from transitive dependencies

## Dependencies
- Depends on: Task 2 — Implement license report service with transitive dependency resolution
