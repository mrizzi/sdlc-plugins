## Repository
trustify-backend

## Description
Create the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint handler and register it in the SBOM route configuration. This endpoint calls the service-layer aggregation method and returns the severity counts as JSON. It also returns 404 when the SBOM does not exist.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary` for the new endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `mod advisory_summary;` and register the `GET /{id}/advisory-summary` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with status 200, or 404 if SBOM not found

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract the `id` path parameter using Axum's `Path<Uuid>` extractor, obtain the database connection from app state, call the service method, and return `Json(summary)`.
- The handler signature should be `async fn get_advisory_summary(Path(id): Path<Uuid>, State(state): State<AppState>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- The `AppError::NotFound` returned by the service layer will automatically convert to a 404 HTTP response via the `IntoResponse` impl in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using `.route("/:id/advisory-summary", get(advisory_summary::get_advisory_summary))`, following the pattern used for the existing `/:id` GET route.
- Add OpenAPI documentation attributes (`#[utoipa::path(...)]`) to the handler, consistent with other endpoint handlers in the crate.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for path parameter extraction and service invocation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Automatic error-to-response conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler has OpenAPI annotations for schema generation
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID and verify 200 status with expected JSON fields
- [ ] Integration test: call the endpoint with a non-existent SBOM ID and verify 404 status

## Verification Commands
- `cargo build -p fundamental` — Compiles without errors
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — Returns JSON with severity counts

## Dependencies
- Depends on: Task 2 — SBOM advisory aggregation service (provides `SbomService::advisory_summary` method)
