## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns advisory severity counts for a given SBOM. The endpoint delegates to the `SbomService::advisory_severity_summary` method created in the previous task, returns a JSON response with the `AdvisorySeveritySummary` shape, and applies a 5-minute cache using `tower-http` caching middleware. Returns 404 if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache header

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting the SBOM ID path parameter and returning a JSON response.
- The handler should call `SbomService::advisory_severity_summary(id)` and return the result as JSON.
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` following the error handling convention where all handlers return `Result<T, AppError>` with `.context()` wrapping.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes, following the same route registration pattern.
- Apply 5-minute cache using `tower-http` caching middleware in the route builder, following the caching pattern established in existing endpoint route builders. Set `Cache-Control: max-age=300`.
- Response time target is p95 < 200ms for SBOMs with up to 500 advisories.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling endpoint handler pattern for path parameter extraction and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for automatic 404 conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns HTTP 200 with JSON body `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Endpoint is registered in the SBOM route module and reachable via the Axum router

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a valid SBOM with linked advisories
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Integration test: response includes correct `Cache-Control` header

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
