## Repository
trustify-backend

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that calls the advisory summary service method and returns the severity counts as JSON. The endpoint includes a 5-minute cache-control header using the existing tower-http caching middleware pattern. It also registers the new route in the SBOM endpoints module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for GET /api/v2/sbom/{id}/advisory-summary that extracts the SBOM ID from the path, calls the advisory_summary service, and returns the AdvisorySeveritySummary as JSON with appropriate cache headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod advisory_summary;` and register the new route (GET on `/{id}/advisory-summary`) in the SBOM router, alongside existing routes like `/{id}` from `get.rs`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with Cache-Control: max-age=300

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting the SBOM ID from `axum::extract::Path`, injecting the database connection via Axum state/extension, and returning `Result<Json<T>, AppError>`.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — look at how the existing `.route("/:id", get(get::handler))` is registered and add a parallel `.route("/:id/advisory-summary", get(advisory_summary::handler))`.
- For caching, apply a `tower_http::set_header::SetResponseHeaderLayer` or similar middleware to set `Cache-Control: public, max-age=300` on the response. Reference the caching patterns described in the repository conventions — tower-http caching middleware in endpoint route builders.
- The handler should be a thin layer: extract path param, call service, return JSON. No business logic in the handler.
- Use `common/src/error.rs::AppError` for error conversion — the service already returns AppError, so the `?` operator handles propagation.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Direct pattern for SBOM ID path extraction, handler signature, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow

## Acceptance Criteria
- [ ] Handler function exists in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`
- [ ] Route is registered at `GET /api/v2/sbom/{id}/advisory-summary`
- [ ] Response body is JSON with fields: critical, high, medium, low, total
- [ ] Response includes Cache-Control header with max-age=300 (5 minutes)
- [ ] Returns HTTP 404 with appropriate error body when SBOM ID does not exist
- [ ] Returns HTTP 200 on success
- [ ] `cargo check -p trustify-module-fundamental` passes

## Test Requirements
- [ ] Integration test that calls GET /api/v2/sbom/{id}/advisory-summary for a valid SBOM and verifies HTTP 200 with correct JSON shape
- [ ] Integration test that calls the endpoint for a non-existent SBOM ID and verifies HTTP 404
- [ ] Integration test that verifies the Cache-Control response header is present and set to max-age=300
- [ ] Integration test that verifies the response JSON contains all five fields (critical, high, medium, low, total) with correct integer types

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — handler tests pass
- `curl -v http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary` — returns JSON with severity counts and Cache-Control header

## Dependencies
- Depends on: Task 2 — Advisory summary service (requires the service method to call)
