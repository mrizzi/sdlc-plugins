## Repository
trustify-backend

## Description
Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_severity_summary` method and returns the `AdvisorySeveritySummary` as JSON. It supports an optional `?threshold` query parameter to filter counts above a specified severity level. The endpoint returns 404 if the SBOM does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered severity counts above the given threshold

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}): the handler extracts the path parameter `id`, calls the service method, and returns `Result<Json<T>, AppError>`.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. The route should be nested under the SBOM scope at `/api/v2/sbom/{id}/advisory-summary`.
- Parse the optional `?threshold` query parameter using Axum's `Query<T>` extractor. Define a query params struct (e.g., `AdvisorySummaryParams`) with an `Option<SeverityThreshold>` field.
- The handler should call `SbomService::get_advisory_severity_summary(id, threshold)` and return the result as JSON.
- Error handling follows the project convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. The `AppError` enum in `common/src/error.rs` implements `IntoResponse` so errors are automatically converted to appropriate HTTP status codes (404 for not-found).
- Per the key conventions: each module's `endpoints/mod.rs` registers routes, and `server/main.rs` mounts all modules. No changes to `server/main.rs` should be needed if the SBOM module's route group already mounts sub-routes dynamically.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern: path parameter extraction, service call, JSON response, error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — demonstrates route registration pattern within the SBOM module
- `common/src/error.rs::AppError` — error type that implements IntoResponse for automatic HTTP status code mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns filtered counts
- [ ] `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` returns 404
- [ ] Response content-type is `application/json`
- [ ] The route is registered in the SBOM module's route configuration

## Test Requirements
- [ ] Handler unit test: mock SbomService returning known counts, verify JSON response shape and status 200
- [ ] Handler unit test: mock SbomService returning not-found error, verify status 404
- [ ] Handler unit test: verify threshold query parameter is correctly parsed and forwarded to the service method

## Verification Commands
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — should return JSON with severity count fields
- `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/v2/sbom/nonexistent/advisory-summary` — should return 404

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory severity aggregation service method
