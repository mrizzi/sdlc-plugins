## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the severity aggregation service method and returns the `AdvisorySeveritySummary` response. Configure 5-minute caching using the existing tower-http caching middleware. Register the route in the SBOM endpoints module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function for GET /api/v2/sbom/{id}/advisory-summary with cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add `mod advisory_summary;` and register the new route in the route builder

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for extracting path parameters, calling the service, and returning typed JSON responses.
- The handler should extract the SBOM `id` from the path using Axum's `Path` extractor, consistent with the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Call `SbomService::advisory_severity_summary(id)` and return the result as JSON. Errors propagate through `Result<T, AppError>` automatically via the IntoResponse implementation in `common/src/error.rs`.
- Configure 5-minute cache TTL using `tower-http` caching middleware. The existing caching pattern is documented in the Key Conventions section — inspect `modules/fundamental/src/sbom/endpoints/mod.rs` for how caching middleware is applied to route builders.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (alongside the list and get routes).
- The endpoint returns 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints behavior.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for path parameter extraction, service invocation, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern and caching middleware application
- `common/src/error.rs::AppError` — error handling with IntoResponse for automatic 404 mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes cache headers with 5-minute TTL
- [ ] Route is registered in the SBOM endpoints module alongside existing routes
- [ ] Handler follows the existing endpoint pattern (Path extractor, Result<T, AppError> return type)

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response includes appropriate cache-control headers

## Verification Commands
- `cargo build` — verifies compilation with new endpoint
- `cargo test` — verifies all tests pass including new endpoint tests

## Documentation Updates
- `README.md` — add the new endpoint to any API endpoint listing if present

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method

[sdlc-workflow] Description digest: sha256:330d969732f74df225d651f080a9c132c90ad65aad16315cfccbe4b0bf2eb228
