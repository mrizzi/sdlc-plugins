## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/license-report` route handler and wire it into the Axum router. The handler extracts the SBOM ID from the path, delegates to `LicenseReportService` (Task 1) with the loaded `LicensePolicy` (Task 2), and returns the `LicenseReportResponse` (Task 3) as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler `get_license_report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route under the existing `/api/v2/sbom` router
- `server/src/main.rs` — no structural change needed if `Arc<LicensePolicy>` state is already added in Task 2; confirm the module is mounted

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReportResponse` JSON; 404 if the SBOM does not exist; 500 on query failure

## Implementation Notes
Handler signature pattern — follow `modules/fundamental/src/sbom/endpoints/get.rs`:

```rust
// modules/fundamental/src/sbom/endpoints/license_report.rs

pub async fn get_license_report(
    State(db): State<Arc<DatabaseConnection>>,
    State(policy): State<Arc<LicensePolicy>>,
    Path(id): Path<Uuid>,
) -> Result<Json<LicenseReportResponse>, AppError> {
    let groups = LicenseReportService::get_license_groups(id, &db, &policy).await?;
    let response = LicenseReportResponse { sbom_id: id, groups };
    Ok(Json(response))
}
```

In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the route to the existing `Router`:

```rust
.route("/:id/license-report", get(license_report::get_license_report))
```

This follows the pattern already used by `list.rs` and `get.rs` in the same directory. The route is nested under the `/api/v2/sbom` prefix mounted in `server/src/main.rs`, so no changes to that file are required beyond confirming the `LicensePolicy` state is present (Task 2).

Return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist in the database. Use `.context("SBOM not found")` for the error message.

No authentication bypass, debug endpoints, or SQL proxy endpoints are to be added. The endpoint is protected by the same middleware stack applied to all `/api/v2/sbom` routes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern: `State`, `Path`, `Result<Json<T>, AppError>`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing router to extend with `.route()`
- `common/src/error.rs::AppError` — `NotFound` variant for missing SBOM

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns HTTP 200 with a valid `LicenseReportResponse` JSON body for an existing SBOM
- [ ] Response JSON shape matches `{ "sbom_id": "<uuid>", "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Returns HTTP 404 when the SBOM ID does not exist
- [ ] Returns HTTP 500 (via `AppError`) on unexpected database errors
- [ ] Route is correctly nested under `/api/v2/sbom` — full path is `/api/v2/sbom/{id}/license-report`
- [ ] `cargo build` succeeds with no new warnings

## Test Requirements
- [ ] Integration test in `tests/api/sbom.rs`: seed an SBOM with known packages and licenses; call `GET /api/v2/sbom/{id}/license-report`; assert `StatusCode::OK` and that `groups` contains the expected license buckets with correct `compliant` flags
- [ ] Integration test: call the endpoint with a non-existent SBOM ID; assert `StatusCode::NOT_FOUND`

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/{id}/license-report` to the API reference section with the response schema and a note about the `LICENSE_POLICY_PATH` environment variable

## Dependencies
- Depends on: Task 1 — License query service
- Depends on: Task 2 — License policy configuration
- Depends on: Task 3 — License report response model
