## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_summary` method and returns the `SeveritySummary` as JSON. It supports an optional `?threshold=<severity>` query parameter to filter counts to only severities at or above the specified level. The endpoint response is cached for 5 minutes using the existing `tower-http` caching middleware. Returns 404 if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Supports optional `?threshold=critical|high|medium|low` query parameter to filter counts to severities at or above the threshold.

## Implementation Notes
Follow the existing endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) and `modules/fundamental/src/sbom/endpoints/list.rs` (GET /api/v2/sbom). These handlers demonstrate the conventions for:
- Extracting path parameters (SBOM ID) using Axum extractors
- Calling service methods and mapping errors to HTTP responses
- Returning JSON responses with `Result<Json<T>, AppError>`

For the `?threshold` query parameter, define a query parameter struct with an optional `threshold` field. Use an enum (`Severity`) or string matching to validate the threshold value. When the threshold is provided, zero out severity counts below the threshold level in the response.

For caching, apply the `tower-http` caching middleware with a 5-minute TTL on the route builder. See existing route registrations in `modules/fundamental/src/sbom/endpoints/mod.rs` for how caching middleware is applied to routes.

The route registration must be added to `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for registering `.get()` routes under the `/api/v2/sbom` prefix.

Per CONVENTIONS.md §Endpoint registration: register the new route in `endpoints/mod.rs` and ensure it is mounted via `server/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Error handling: handler returns `Result<Json<SeveritySummary>, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in the endpoint route builder.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET handler; follow its pattern for path parameter extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern; follow for adding the new route with caching middleware
- `common/src/error.rs::AppError` — Error handling; reuse for 404 and internal error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts to only those at or above the specified level
- [ ] Response is cached for 5 minutes using `tower-http` caching middleware
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Integration test verifying successful 200 response with correct severity counts
- [ ] Integration test verifying 404 response for non-existent SBOM ID
- [ ] Integration test verifying `?threshold=critical` returns only critical count
- [ ] Integration test verifying cached response (second request within 5 minutes returns same data)

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors
- `cargo test -p trustify-fundamental` — All tests pass

## Documentation Updates
- `README.md` — Add the new endpoint to the API reference if an API section exists

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService
