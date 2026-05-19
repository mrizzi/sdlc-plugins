## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/license-report` and register the route in the SBOM endpoint module. This exposes the license compliance report service via the REST API, returning a JSON response with packages grouped by license and compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for the license report endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route at `/api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response body: `{ "sbom_id": "...", "groups": [{ "license": "MIT", "packages": [{ "name": "serde", "version": "1.0", "purl": "pkg:cargo/serde@1.0" }], "compliant": true }], "generated_at": "2026-05-19T00:00:00Z", "policy_name": "default" }`

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`:

1. **Handler function** — Define an async handler that extracts the SBOM `{id}` path parameter using Axum's `Path` extractor, exactly as done in `get.rs`. The handler should:
   - Load the `LicensePolicy` (from file or default)
   - Call `LicenseReportService::generate_report()` from `modules/fundamental/src/sbom/service/license_report.rs`
   - Return `Json(report)` on success
   - Return the appropriate `AppError` variant on failure (which implements `IntoResponse` via `common/src/error.rs`)

2. **Route registration** — In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the route using the same pattern as the existing `/api/v2/sbom/{id}` route. The new route should be nested under the existing SBOM path: `.route("/:id/license-report", get(license_report::handler))`.

3. **Error responses** — Return 404 if the SBOM ID does not exist. Return 500 if the policy file cannot be loaded (with a logged warning). All errors flow through `AppError` which already implements `IntoResponse`.

4. **Content type** — The response should be `application/json`. Axum's `Json` extractor handles this automatically.

The handler function signature should follow the pattern: `async fn handler(Path(id): Path<String>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM detail endpoint; follow its pattern for path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type that implements `IntoResponse`
- `modules/fundamental/src/sbom/service/license_report.rs::LicenseReportService` — service to call from the handler

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` is routable and returns a JSON license report
- [ ] Response JSON structure matches the schema: `{ sbom_id, groups: [{ license, packages, compliant }], generated_at, policy_name }`
- [ ] Returns HTTP 404 for non-existent SBOM IDs
- [ ] Returns HTTP 500 with a meaningful error message if the policy file is malformed
- [ ] The route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] No new backdoor, debug, or admin endpoints are created — only the documented license-report endpoint

## Test Requirements
- [ ] Verify the route is registered and accessible (handler is wired up correctly)
- [ ] Verify the JSON response structure matches the expected schema

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors
- `cargo check -p trustify-server` — should compile (verifies route mounting)

## Dependencies
- Depends on: Task 3 — Implement license report service with transitive dependency resolution
