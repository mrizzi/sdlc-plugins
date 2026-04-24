## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that serves the aggregated advisory severity counts for a given SBOM. This endpoint calls the aggregation service method (Task 2) and returns the `AdvisorySeveritySummary` as JSON. The response must include a 5-minute cache-control header using the existing tower-http caching middleware. The endpoint returns 404 if the SBOM does not exist, consistent with other SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID from the path, calls the service method, and returns the result as JSON with cache headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/advisory-summary` route alongside existing SBOM routes (next to the routes for `list.rs` and `get.rs`)

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Cache-Control: max-age=300` header. Returns 404 if SBOM ID does not exist.

## Implementation Notes
- Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the endpoint handler structure: extract path parameter `{id}`, call the service method, return `Result<Json<T>, AppError>`.
- Use Axum's `Path` extractor for the SBOM ID, consistent with the existing `get.rs` handler.
- Apply a 5-minute cache-control header using the tower-http caching middleware. Look at how other endpoints in `modules/fundamental/src/sbom/endpoints/mod.rs` configure caching via route builder options.
- Error handling: the service method returns `AppError::NotFound` for missing SBOMs, which Axum translates to a 404 response via the `IntoResponse` implementation in `common/src/error.rs`.
- Register the route as `.route("/{id}/advisory-summary", get(advisory_summary))` in the SBOM router in `modules/fundamental/src/sbom/endpoints/mod.rs`, following the existing pattern for `/{id}` routes.
- Per constraints (section 5.3), follow the patterns referenced in the task's Implementation Notes exactly.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Direct pattern reference for single-SBOM endpoint handler with ID path parameter extraction, service call, and 404 handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern and cache middleware configuration
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for automatic HTTP status code mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` endpoint is registered and reachable
- [ ] Endpoint returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for a valid SBOM
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Handler follows the existing endpoint pattern (Path extractor, service call, Json response)
- [ ] `cargo check -p trustify-module-fundamental` compiles with no errors

## Test Requirements
- [ ] Integration test: GET valid SBOM returns 200 with correct severity counts
- [ ] Integration test: GET non-existent SBOM returns 404
- [ ] Integration test: Response contains Cache-Control header with max-age=300

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 1 — Advisory summary model
- Depends on: Task 2 — Aggregation service
