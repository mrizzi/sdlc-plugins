# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method, applies 5-minute response caching via `tower-http` middleware, and supports an optional `?threshold` query parameter for filtering by severity level. This is the primary deliverable for the feature, enabling dashboard widgets and alerting integrations to retrieve severity breakdowns in a single call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with cache configuration and threshold query parameter

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `advisory_summary` route under `/api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Supports optional `?threshold=critical|high|medium|low` query parameter. Returns 404 if SBOM ID does not exist. Response cached for 5 minutes.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract path parameter `{id}`, call the service method, return JSON response or propagate `AppError`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs` route registration. The route should be mounted as a sub-path under the existing SBOM router.
- Cache configuration: Use `tower-http` caching middleware with a 5-minute TTL. Check existing endpoint route builders for the caching pattern used in this project. Apply `Cache-Control: max-age=300` or use the project's cache middleware configuration.
- The `threshold` query parameter is optional. Define a query struct (e.g., `AdvisorySummaryQuery`) with `threshold: Option<Severity>` to deserialize the query string. Use `axum::extract::Query` for extraction.
- Handler signature should follow the established pattern: `async fn advisory_summary(Path(id): Path<Uuid>, Query(params): Query<AdvisorySummaryQuery>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`
- Per `docs/constraints.md` §5.3: Follow the patterns referenced in Implementation Notes — use the same handler structure, error handling, and response types as existing SBOM endpoints.
- Per `docs/constraints.md` §5.1: Only modify/create the files listed above — do not touch unrelated files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM GET endpoint handler showing path parameter extraction, service call, and error response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for SBOM endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — Shows query parameter extraction pattern if used

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response includes cache headers with 5-minute TTL
- [ ] Optional `?threshold` query parameter filters severity counts correctly
- [ ] Endpoint is registered and reachable via the Axum router

## Test Requirements
- [ ] Integration test: GET request returns 200 with correct severity counts for a known SBOM
- [ ] Integration test: GET request returns 404 for a non-existent SBOM ID
- [ ] Integration test: GET with `?threshold=critical` returns only critical counts (other counts are zero)
- [ ] Integration test: Response includes correct cache control headers

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-tests --test api -- advisory_summary` — integration tests pass

## Documentation Updates
- `README.md` — Add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
