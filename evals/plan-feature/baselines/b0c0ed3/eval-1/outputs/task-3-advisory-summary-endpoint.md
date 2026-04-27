## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::advisory_summary` and returns the aggregated severity counts as JSON. Configure 5-minute caching using the existing `tower-http` cache middleware. Register the new route in the SBOM endpoint module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route and add `mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 status, or 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — it demonstrates extracting a path parameter (`{id}`), calling a service method, handling errors, and returning a JSON response.
- The handler function signature should follow the Axum extractor pattern: accept `Path(id)` for the SBOM ID and a `State` extractor for the service, returning `Result<Json<AdvisorySeveritySummary>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing routes (list, get). Follow the route registration pattern used for the existing `GET /api/v2/sbom/{id}` route in that file.
- Configure 5-minute caching using the `tower-http` caching middleware — follow the cache configuration pattern used in the existing endpoint route builders as described in the repository's key conventions.
- The `server/main.rs` file mounts all module routes — no changes should be needed there since the SBOM module routes are already mounted and the new route will be added within the existing SBOM route group.
- Per the repository's key conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. The framework is Axum for HTTP.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler for single SBOM; follow its structure for path parameter extraction, service invocation, and error handling.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration module; follow its pattern for adding the new route to the router.
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse` for automatic HTTP error responses.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when the SBOM ID does not exist
- [ ] Response includes cache headers indicating 5-minute cache duration
- [ ] Route is registered in the SBOM endpoint module alongside existing routes
- [ ] No changes required in `server/main.rs`

## Test Requirements
- [ ] Verify the endpoint returns 200 with correct JSON shape for an SBOM with linked advisories
- [ ] Verify the endpoint returns 404 for a non-existent SBOM ID
- [ ] Verify response includes appropriate cache-control headers

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns expected JSON response (requires running server)

## Documentation Updates
- `README.md` — Add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct
- Depends on: Task 2 — Add advisory_summary service method
