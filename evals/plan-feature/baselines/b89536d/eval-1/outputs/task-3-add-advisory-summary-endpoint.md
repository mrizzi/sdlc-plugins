# Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to `SbomService::advisory_summary`, applies 5-minute cache headers via `tower-http` caching middleware, supports an optional `?threshold` query parameter for severity filtering, and returns 404 if the SBOM does not exist.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- handler function for `GET /api/v2/sbom/{id}/advisory-summary` that extracts SBOM ID from path, optional threshold from query params, calls `SbomService::advisory_summary`, and returns JSON response with cache headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `advisory-summary` route in the SBOM router, add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache. Returns 404 if SBOM ID does not exist.
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` -- NEW: optional query parameter to filter counts to severities at or above the threshold

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, service delegation, and error handling
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the `list.rs` and `get.rs` routes
- Cache configuration: use `tower-http` caching middleware to set `Cache-Control: max-age=300` (5 minutes) on the response, following the existing cache configuration pattern in the endpoint route builders
- Define a query parameter struct (e.g., `AdvisorySummaryQuery`) with an optional `threshold` field to deserialize the `?threshold=critical` query parameter via Axum's `Query` extractor
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` to be consistent with the codebase error handling convention
- Response serialization is handled automatically by `Json<T>` wrapper since `AdvisorySeveritySummary` derives `Serialize`

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing endpoint handler to follow for path extraction, service call, and error response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of query parameter extraction for reference

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with severity counts
- [ ] Response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 with appropriate error response when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header for 5-minute caching
- [ ] Optional `?threshold` query parameter correctly filters severity counts
- [ ] Endpoint is accessible at the correct path within the SBOM API router

## Test Requirements
- [ ] Integration test: successful request returns 200 with correct severity counts JSON
- [ ] Integration test: nonexistent SBOM ID returns 404
- [ ] Integration test: response includes cache control headers
- [ ] Integration test: threshold query parameter returns filtered counts
- [ ] Integration test: SBOM with no advisories returns all-zero counts with 200 status

## Verification Commands
- `cargo test --test api -- advisory_summary` -- runs advisory summary integration tests, expects all tests to pass
- `curl -i http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary` -- returns 200 with JSON severity counts and Cache-Control header

## Documentation Updates
- `README.md` -- add the new endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 -- Add advisory summary aggregation to SbomService
