## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license report service and returns the compliance report as a JSON response. Register the route in the SBOM module's endpoint configuration.

## Jira Metadata
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler function for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the license-report route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a `LicenseReport` JSON object containing packages grouped by license type with compliance flags. Returns 404 if SBOM ID is not found. Returns 200 with the full report on success.

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure:

1. Extract the SBOM `id` from the path using Axum's `Path` extractor.
2. Inject the database connection via Axum's state/extension mechanism (match existing patterns in `get.rs` and `list.rs`).
3. Call `LicenseReportService::generate_report(db, sbom_id)`.
4. Return `Json(report)` on success, or let `AppError` handle error responses via its `IntoResponse` impl from `common/src/error.rs`.

For route registration in `modules/fundamental/src/sbom/endpoints/mod.rs`, follow the existing pattern used for `get.rs` and `list.rs`. The route should be nested under the existing `/api/v2/sbom` path as `/{id}/license-report`.

The endpoint does not need pagination (it returns a complete report) so `PaginatedResults<T>` from `common/src/model/paginated.rs` is NOT used here.

Per CONVENTIONS.md §Module Pattern: follow `model/ + service/ + endpoints/` structure for the endpoint layer. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's module file scope.

Per CONVENTIONS.md §Error Handling: handler returns `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Endpoint Registration: register route in `endpoints/mod.rs`; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Direct pattern for single-resource GET handler with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error handling via IntoResponse implementation
- `modules/fundamental/src/advisory/endpoints/get.rs` — Additional reference for handler patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid `LicenseReport` JSON body
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Route is properly registered in the SBOM module's endpoint configuration
- [ ] Response Content-Type is `application/json`
- [ ] Handler follows existing Axum handler patterns (Path extractor, state injection, Result<Json<T>, AppError> return)

## Test Requirements
- [ ] Integration test: GET request returns 200 with valid LicenseReport JSON for an existing SBOM
- [ ] Integration test: GET request returns 404 for non-existent SBOM ID
- [ ] Integration test: Response contains correctly grouped license data matching test fixtures
- [ ] Integration test: Non-compliant licenses are flagged in the response

## Dependencies
- Depends on: Task 2 — Implement license report service with transitive dependency resolution

[sdlc-workflow] Description digest: sha256-md:02e0f9c58f3536c3eee0826cbd1f1d68ebf3d201e0b90e27c4b154c519348463
