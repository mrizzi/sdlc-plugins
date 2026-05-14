## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to the `SbomService::get_advisory_severity_summary` method (from Task 1), applies 5-minute caching via `tower-http` caching middleware, and supports an optional `?threshold` query parameter that filters counts to only include severities at or above the specified level.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` for the given SBOM; supports optional `?threshold=critical|high|medium|low` query parameter to filter severity levels; returns 404 if SBOM ID does not exist

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint, including threshold query parameter parsing and response construction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler function structure: extract path parameters, call the service method, return `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes (e.g., the `GET /api/v2/sbom/{id}` route registered in that file).
- For the `?threshold` query parameter, define a query struct (e.g., `AdvisorySummaryQuery`) with an `Option<String>` threshold field and use Axum's `Query` extractor. Valid values are `critical`, `high`, `medium`, `low`. When present, zero out severity counts below the threshold and recalculate `total`.
- Apply 5-minute caching using `tower-http` caching middleware on the route builder, following the caching pattern described in the repository conventions (cache configuration in endpoint route builders).
- Return HTTP 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints like `GET /api/v2/sbom/{id}`.
- The handler should call `SbomService::get_advisory_severity_summary` and transform the result based on the threshold parameter before returning.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function structure, path parameter extraction, and error response patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — standard error handling; reuse for 404 responses
- `modules/fundamental/src/sbom/model/advisory_summary.rs::AdvisorySeveritySummary` — the response type created in Task 1

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with fields `critical`, `high`, `medium`, `low`, `total`
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes
- [ ] Optional `?threshold` query parameter filters counts to severities at or above the specified level
- [ ] Total count is recalculated when threshold is applied

## Test Requirements
- [ ] Test that the endpoint returns correct severity counts for an SBOM with known advisories
- [ ] Test that the endpoint returns 404 for a non-existent SBOM ID
- [ ] Test that the `?threshold=critical` parameter returns only the critical count (other levels zeroed) with recalculated total
- [ ] Test that the `?threshold=high` parameter returns critical and high counts with recalculated total

## Verification Commands
- `cargo test --test api` — integration tests should pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
