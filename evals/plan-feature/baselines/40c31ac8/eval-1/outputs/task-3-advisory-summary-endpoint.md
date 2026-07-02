## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that returns aggregated advisory severity counts for a given SBOM. Register the route in the SBOM endpoint module and configure 5-minute cache headers using the existing tower-http caching middleware. This is the core MVP endpoint that replaces the frontend's multi-page advisory fetch with a single aggregation call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Async handler function for the advisory summary route

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `GET /api/v2/sbom/{id}/advisory-summary` route and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Cache-Control: max-age=300`

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for function signature: `async fn handler(Path(id): Path<Uuid>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (e.g., `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))`).
- Apply tower-http `CacheControl` layer with `max_age = 300` seconds (5 minutes) to the route, consistent with the caching infrastructure documented in the repo conventions.
- Call `SbomService::get_advisory_summary()` from the handler, passing the SBOM ID extracted from the path.
- The handler propagates the `AppError::NotFound` from the service layer when the SBOM ID does not exist, resulting in a 404 response.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust language scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM detail endpoint handler to use as structural template for handler signature and error propagation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — Standard error type that implements `IntoResponse` for automatic HTTP status mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON severity counts for a valid SBOM
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Route is registered in SBOM endpoint module at the correct path

## Test Requirements
- [ ] Handler returns 200 with correct JSON structure for valid SBOM
- [ ] Handler returns 404 for non-existent SBOM ID
- [ ] Cache-Control header is present with max-age=300

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
