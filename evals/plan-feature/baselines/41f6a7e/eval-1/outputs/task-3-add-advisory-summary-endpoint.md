# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the service method from Task 2, applies 5-minute cache headers using the existing tower-http caching middleware, and supports an optional `?threshold` query parameter for filtering by severity level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary with optional `?threshold` query parameter

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns severity counts filtered to only include levels at or above the specified threshold

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler signature, path parameter extraction, service injection, and error handling with `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the existing list and get routes. The route should be nested under the SBOM path prefix.
- For the `?threshold` query parameter, define an optional query struct (e.g., `AdvisorySummaryQuery { threshold: Option<String> }`) using Axum's `Query` extractor. Parse the threshold value as a severity level enum. Return 400 Bad Request for invalid threshold values.
- Apply 5-minute cache configuration using the existing `tower-http` caching middleware pattern used in endpoint route builders. Reference the existing route builder configuration in `modules/fundamental/src/sbom/endpoints/mod.rs` for how caching is configured on routes.
- The handler should extract the SBOM ID from the path, the optional threshold from query params, call `SbomService::get_advisory_summary`, and return the result as JSON.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for path parameter extraction, service injection, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern
- `common/src/error.rs::AppError` — error handling for 404 and 400 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Endpoint supports optional `?threshold` query parameter
- [ ] Endpoint returns 400 for invalid threshold values
- [ ] Response includes cache headers with 5-minute max-age
- [ ] Route is registered in the SBOM module's route configuration

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Integration test: GET /api/v2/sbom/{nonexistent}/advisory-summary returns 404
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns only critical count
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid returns 400
- [ ] Integration test: verify response includes appropriate cache headers

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory summary integration tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — returns JSON with severity counts

## Documentation Updates
- `README.md` — add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method
