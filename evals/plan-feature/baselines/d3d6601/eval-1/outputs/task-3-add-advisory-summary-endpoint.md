## Repository
trustify-backend

## Target Branch
main

## Description
Add the new `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method, applies a 5-minute cache using the existing `tower-http` caching middleware, and returns the `AdvisorySeveritySummary` as JSON. If the SBOM ID does not exist, the endpoint returns a 404 response consistent with other SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Content-Type: application/json` and 5-minute cache headers

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` — the handler extracts the SBOM ID from the path, calls the service method, and returns the result as JSON or maps errors to HTTP status codes.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for `list.rs` and `get.rs` route registration. The route should be nested under the existing `/api/v2/sbom/{id}` path group.
- Apply 5-minute caching using `tower-http` caching middleware as described in the repository conventions. Configure cache headers (`Cache-Control: max-age=300`) on the route builder, following the pattern used by other cached endpoints in the codebase.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the standard error handling pattern — `AppError` implements `IntoResponse` (see `common/src/error.rs`).
- Ensure the endpoint path uses `advisory-summary` (kebab-case) consistent with existing endpoint naming.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern for single-SBOM endpoints with path parameter extraction and error mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows how to register routes under `/api/v2/sbom`
- `common/src/error.rs::AppError` — shared error type with `IntoResponse` implementation for HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 when the SBOM ID does not exist, consistent with `GET /api/v2/sbom/{id}`
- [ ] Response includes cache headers for 5-minute caching (`Cache-Control: max-age=300` or equivalent)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID that has linked advisories, verify 200 response with correct severity counts
- [ ] Integration test: call the endpoint with a non-existent SBOM ID, verify 404 response
- [ ] Integration test: verify response includes appropriate cache headers

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct
- Depends on: Task 2 — Add severity aggregation service method

[sdlc-workflow] Description digest: sha256:97585ed7ede9f26b4cd2e38e178cc91d50eda760dd90bfb5c552bedfcd5088ee
