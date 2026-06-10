## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint must apply 5-minute response caching using the existing tower-http caching middleware and return a 404 status when the SBOM ID does not exist. It must also support an optional `?threshold` query parameter for severity filtering.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary with cache configuration and threshold query parameter extraction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new /api/v2/sbom/{id}/advisory-summary route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache, 404 for missing SBOM, optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function structure — it demonstrates how to extract path parameters, call service methods, and return typed JSON responses with proper error handling via `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing GET routes. Follow the route registration pattern used for `/api/v2/sbom/{id}` (get endpoint).
- Apply tower-http caching middleware with a 5-minute max-age configuration. Reference the caching patterns described in the repository conventions: "Uses tower-http caching middleware; cache configuration in endpoint route builders."
- Extract the optional `threshold` query parameter using Axum's `Query<>` extractor. Define a small query params struct (e.g., `AdvisorySummaryParams`) with an `Option<String>` threshold field.
- The handler should call `SbomService::get_advisory_severity_summary()` from Task 2 and return the result as JSON.
- Ensure the endpoint is documented with `utoipa` OpenAPI attributes (`#[utoipa::path(...)]`) following the pattern of existing endpoints.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler demonstrating path parameter extraction, service invocation, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new route
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction pattern using Axum's Query extractor

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `{ critical, high, medium, low, total }` fields
- [ ] Endpoint returns HTTP 404 when SBOM ID does not exist
- [ ] Response includes cache-control headers with 5-minute max-age
- [ ] Optional `?threshold` query parameter filters severity counts
- [ ] Endpoint is registered in the SBOM route tree at the correct path
- [ ] OpenAPI schema is generated for the endpoint via utoipa attributes

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts for an existing SBOM
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for non-existent SBOM ID
- [ ] Integration test: response includes expected cache-control headers
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns filtered counts

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — endpoint unit tests pass

## Documentation Updates
- `README.md` — add the new endpoint to any API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
