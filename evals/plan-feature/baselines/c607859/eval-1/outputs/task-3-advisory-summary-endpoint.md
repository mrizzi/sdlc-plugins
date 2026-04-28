# Task 3 — Add advisory summary endpoint

## Repository
trustify-backend

## Description
Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated severity counts for advisories linked to a given SBOM. The endpoint calls the service method created in Task 2, returns the `AdvisorySeveritySummary` response, supports an optional `?threshold` query parameter for severity filtering, returns 404 for non-existent SBOMs, and includes 5-minute cache configuration using the existing `tower-http` caching middleware.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route in the SBOM route builder

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered counts for severities at or above the given threshold

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for the `GET /api/v2/sbom/{id}` endpoint: extract path parameter, call service method, return JSON response or error.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as existing routes (e.g., `.route("/:id", get(get::handler))` — add `.route("/:id/advisory-summary", get(advisory_summary::handler))`).
- For the optional `?threshold` query parameter, use Axum's `Query<ThresholdQueryParam>` extractor. Define the query param struct in the handler file if sibling endpoints follow that pattern.
- Configure 5-minute caching using `tower-http` caching middleware, consistent with the caching patterns described in the repository conventions. Look at how existing endpoints configure cache headers or middleware layers.
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` from the handler, consistent with the error handling pattern using `AppError` from `common/src/error.rs`.
- Per constraints doc section 2: commits must reference Jira issue ID. Per section 3: branch must be named after the Jira issue.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference endpoint handler showing path parameter extraction, service invocation, and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error response handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters counts by severity level
- [ ] Response includes cache headers for 5-minute caching
- [ ] Route is registered in the SBOM endpoints module
- [ ] Code compiles without errors

## Test Requirements
- [ ] Integration test: successful request returns correct severity count JSON shape
- [ ] Integration test: request for non-existent SBOM ID returns 404
- [ ] Integration test: request with `?threshold=critical` returns only critical-and-above counts
- [ ] Integration test: response includes appropriate cache control headers

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — endpoint tests should pass

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
