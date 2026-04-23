## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns advisory severity counts for a given SBOM. This endpoint calls the `SbomService::advisory_severity_summary` method and returns the result as JSON. It must include 5-minute response caching using the existing `tower-http` caching middleware. The endpoint returns 404 if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route in the SBOM router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json`. Returns 404 if SBOM not found. Response cached for 5 minutes via `Cache-Control: max-age=300`.

## Implementation Notes
- Create the handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract the path parameter `id` using Axum's `Path` extractor, call the service method, and return `Json<AdvisorySeveritySummary>`.
- The handler signature should be `async fn advisory_summary(Path(id): Path<Uuid>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`, following the existing handler pattern where `AppError` implements `IntoResponse` via `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding a `.route("/:id/advisory-summary", get(advisory_summary::advisory_summary))` call to the existing SBOM router, following the pattern used for the `get.rs` handler registration.
- Apply `tower-http` caching middleware with a 5-minute TTL on the route, following the caching convention described in the repository's key conventions.
- Add OpenAPI documentation annotations using `utoipa` macros (`#[utoipa::path(...)]`) on the handler function, following the patterns in `modules/fundamental/src/sbom/endpoints/get.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the handler pattern: path extraction, service call, JSON response, error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to add the new route
- `common/src/error.rs::AppError` — Error type that implements `IntoResponse` for automatic 404/500 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON severity counts
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header for 5-minute caching
- [ ] Endpoint is registered in the SBOM router in `endpoints/mod.rs`
- [ ] OpenAPI documentation is generated for the endpoint via `utoipa` annotations

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 and correct JSON shape for a valid SBOM
- [ ] Integration test: returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes cache-control header with max-age=300

## Dependencies
- Depends on: Task 2 — Aggregation service (requires `SbomService::advisory_severity_summary` method)
