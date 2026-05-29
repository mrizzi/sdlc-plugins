# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns the aggregated advisory severity counts for a given SBOM. The endpoint calls the service method added in Task 2, applies 5-minute response caching using `tower-http` caching middleware, and returns the `AdvisorySeveritySummary` as JSON. It returns 404 if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler function signatures, path parameter extraction, error handling, and response construction.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs` route registration.
- Apply `tower-http` caching middleware with a 5-minute TTL on the route, consistent with the caching approach documented in the repository conventions (cache configuration in endpoint route builders).
- The handler should extract the SBOM ID from the path, call `SbomService::advisory_severity_summary()`, and return the result as JSON.
- Use `Result<Json<AdvisorySeveritySummary>, AppError>` as the return type with `.context()` error wrapping per the project's error handling convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler demonstrating path parameter extraction, service call, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response includes appropriate cache headers (5-minute TTL)
- [ ] Route is registered in the SBOM endpoints module
- [ ] Handler follows the project's `Result<T, AppError>` error handling pattern

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Integration test: response headers include cache control directives with 5-minute max-age

## Verification Commands
- `cargo test --test api` — all integration tests pass including the new advisory-summary tests

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
