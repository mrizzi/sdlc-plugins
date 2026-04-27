## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. This endpoint calls `SbomService::get_advisory_severity_summary` and returns the `AdvisorySeveritySummary` as a JSON response. The endpoint is configured with 5-minute response caching using the existing `tower-http` caching middleware. This is the public-facing entry point for the severity aggregation feature, enabling dashboard widgets and alerting integrations to retrieve severity breakdowns in a single API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID path parameter, calls `SbomService::get_advisory_severity_summary`, and returns the result as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — import the new `advisory_summary` module and register the `GET /api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes, with 5-minute `tower-http` cache layer configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK; returns 404 if the SBOM ID does not exist; response cached for 5 minutes

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, service invocation, and JSON response construction. The handler signature should match: `async fn handler(Path(id): Path<Uuid>, State(service): State<SbomService>, ...) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs` route registrations. Nest the route under the existing `/api/v2/sbom` prefix as `.route("/:id/advisory-summary", get(advisory_summary::handler))`.
- Configure 5-minute caching using `tower-http` caching middleware on the route, consistent with the existing cache configuration patterns in endpoint route builders. Set `max-age` to 300 seconds.
- Error handling: the handler returns `Result<_, AppError>`, and the service method already produces 404 errors for missing SBOMs via `AppError` from `common/src/error.rs` -- the handler does not need additional error mapping.
- Per `docs/constraints.md` section 2 (Commit Rules): commit messages must follow Conventional Commits and reference TC-9001. Per section 3 (PR Rules): branch must be named after the Jira issue ID. Per section 5 (Code Change Rules): inspect `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` before writing to match their patterns exactly.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler for `GET /api/v2/sbom/{id}`; use as the primary reference for handler signature, path extraction, service call, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration file; follow the existing `.route()` pattern and cache configuration pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` — reference for how advisory routes are structured as an alternative module pattern
- `common/src/error.rs::AppError` — error type used by all handlers; already implements `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON response shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes via `tower-http` caching middleware (Cache-Control: max-age=300)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler follows the existing endpoint patterns (path extraction, service call, error handling)
- [ ] Code compiles and the endpoint is reachable via the Axum server

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{valid-id}/advisory-summary` returns 200 with correct severity counts
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` returns 404
- [ ] Integration test: response includes cache-control headers with 5-minute max-age

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary | jq .` — returns expected JSON shape

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
