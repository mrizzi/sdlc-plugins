## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_severity_summary` method, applies 5-minute caching using `tower-http` middleware, and returns a 404 if the SBOM does not exist. This is the primary MVP endpoint for feature TC-9001 that enables dashboard widgets and alerting integrations to retrieve severity breakdowns in a single call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the advisory summary route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache TTL; returns 404 if SBOM not found

## Implementation Notes
- Create the handler function following the Axum handler signature: `pub async fn get_advisory_summary(Path(id): Path<Uuid>, State(service): State<SbomService>) -> Result<Json<SeveritySummary>, AppError>`.
- Call `service.get_advisory_severity_summary(id, &db).await` and return the result as `Json(summary)`.
- Use `.context("fetching advisory severity summary")` for error wrapping, consistent with existing endpoint error handling in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Configure 5-minute caching using `tower-http` caching middleware on the route builder, matching the cache configuration pattern used by other SBOM endpoints.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes (list, get), mounting at `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::get_advisory_summary))`.
- Per CONVENTIONS.md §Module Pattern: place the endpoint handler in the `endpoints/` subdirectory of the `sbom` domain module. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established handler pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoints/ directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping on fallible operations. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `endpoints/mod.rs` using the same pattern as `list.rs` and `get.rs` registration. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.
- Per CONVENTIONS.md §Caching: configure `tower-http` caching middleware on the route builder with a 5-minute (300s) TTL. See existing endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs` for the caching configuration pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint caching scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — endpoint handler pattern for `GET /api/v2/sbom/{id}` (handler signature, Path extraction, error handling, response wrapping)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration and caching middleware configuration pattern
- `common/src/error.rs::AppError` — error handling with `IntoResponse` implementation

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `SeveritySummary` JSON with correct severity counts
- [ ] Returns 404 with appropriate error message when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (subsequent identical requests within TTL return cached response)
- [ ] Route is registered and reachable in the running server

## Test Requirements
- [ ] Integration test: verify 200 response with correct severity counts for a known SBOM
- [ ] Integration test: verify 404 response for non-existent SBOM ID
- [ ] Integration test: verify response JSON shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Verification Commands
- `cargo test --test api advisory_summary` — expected: all advisory summary integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — expected: JSON response with severity count fields

## Documentation Updates
- `docs/api/` — add the new endpoint to the REST API reference with path, parameters, response shape, and caching behavior

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
