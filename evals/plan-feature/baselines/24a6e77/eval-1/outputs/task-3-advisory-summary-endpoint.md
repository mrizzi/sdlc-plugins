# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Description
Create the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that serves the advisory severity aggregation data. The endpoint must accept an SBOM ID path parameter and an optional `threshold` query parameter, call `SbomService::get_advisory_summary`, and return the `AdvisorySeveritySummary` as JSON. The response must be cached for 5 minutes using the existing `tower-http` caching middleware. The endpoint must return 404 if the SBOM does not exist, consistent with sibling SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function for the advisory summary route, including query parameter parsing for `threshold`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route `GET /api/v2/sbom/{id}/advisory-summary` alongside existing SBOM routes, add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache, optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
- Follow the endpoint handler pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (the `GET /api/v2/sbom/{id}` handler) for function signature, Axum extractor usage, error mapping, and response construction
- Route registration pattern: add the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same `.route()` builder pattern used for the existing `list.rs` and `get.rs` handlers
- For the `threshold` query parameter, define a `ThresholdQuery` struct with `#[derive(Deserialize)]` and use Axum's `Query` extractor — reference how existing endpoints handle optional query parameters
- Configure 5-minute cache using `tower-http` caching middleware — apply cache headers (e.g., `Cache-Control: max-age=300`) on the response, following the caching patterns described in the repository's key conventions
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the standard error handling pattern from `common/src/error.rs`
- The severity threshold values should be validated — invalid values should return a 400 Bad Request response
- Per constraints (Section 5.1): keep changes scoped to the SBOM endpoints module — do not modify unrelated endpoint modules
- Per constraints (Section 5.3): follow the patterns referenced in these Implementation Notes

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — closest sibling endpoint handler, demonstrates Axum path parameter extraction, service call, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter handling with Axum `Query` extractor
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for adding new routes to the SBOM module
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Response includes cache headers for 5-minute caching (e.g., `Cache-Control: max-age=300`)
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts to those at or above the specified level
- [ ] Invalid threshold values return 400 Bad Request
- [ ] Endpoint is registered and accessible in the Axum router

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: invalid threshold value returns 400
- [ ] Integration test: response includes appropriate cache control headers

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-tests --test api` — integration tests should pass

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation query to SbomService
