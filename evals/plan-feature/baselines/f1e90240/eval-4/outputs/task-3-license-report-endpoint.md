# Task 3: Add GET endpoint for license compliance report

- **Jira parent**: TC-9004
- **Repository**: trustify-backend
- **Target Branch**: main
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Description

Add the REST endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for the specified SBOM. The endpoint calls the license compliance service (Task 2) and returns the structured JSON response. Register the route in the SBOM endpoint module and mount it in the server.

## Files to Modify/Create

| Action | Path |
|---|---|
| Create | `modules/fundamental/src/sbom/endpoints/license_report.rs` |
| Modify | `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route |
| Modify | `server/src/main.rs` — ensure SBOM module routes are mounted (likely already done; verify new route is picked up) |

## Implementation Notes

- **`modules/fundamental/src/sbom/endpoints/license_report.rs`**: Implement an Axum handler function `get_license_report` that:
  1. Extracts the SBOM `id` from the path parameter.
  2. Calls `generate_license_report(id)` from the license compliance service.
  3. Returns `Json<LicenseReport>` on success, or maps errors to `AppError` responses.
  4. Handler signature: `async fn get_license_report(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<LicenseReport>, AppError>`.
- **`modules/fundamental/src/sbom/endpoints/mod.rs`**: Add route registration following the existing pattern from `list.rs` and `get.rs`. Add `.route("/api/v2/sbom/:id/license-report", get(get_license_report))`.
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs`.
- No caching middleware needed initially; report data is dynamic per request.

## Acceptance Criteria

- `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a JSON body matching the `LicenseReport` schema.
- Returns HTTP 404 if the SBOM ID does not exist.
- Returns HTTP 500 with an `AppError` body for internal failures.
- Route is accessible when the server starts.

## Test Requirements

- Endpoint handler unit test verifying successful JSON response shape.
- Error path test verifying 404 for non-existent SBOM ID.

## Conventions Applied

- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/endpoints/` matching the convention's model/service/endpoints module structure scope.
- **Error handling**: Applies: task modifies endpoint handler code matching the convention's `Result<T, AppError>` with `.context()` wrapping scope.
- **Endpoint registration**: Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.
- **Framework**: Applies: task modifies Axum handler code matching the convention's Axum for HTTP scope.
