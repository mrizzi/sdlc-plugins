# Task 3 — Add Advisory Summary Endpoint with Caching

## Repository
trustify-backend

## Description
Add a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the `SbomService::advisory_summary` method and returns the `AdvisorySeveritySummary` response. Configure 5-minute cache TTL using the existing `tower-http` caching middleware. Register the route in the SBOM endpoints module.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route in the SBOM endpoint router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` JSON response with 5-minute cache TTL

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for handler structure, path parameter extraction, and error handling.
- The handler should:
  1. Extract the SBOM `{id}` path parameter
  2. Call `SbomService::advisory_summary(id)` 
  3. Return `Result<Json<AdvisorySeveritySummary>, AppError>` following the project's error handling pattern
- Route registration: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. Follow the existing route registration pattern visible in that file.
- Caching: configure 5-minute (300-second) cache TTL using `tower-http` caching middleware, consistent with the project's caching approach. Reference existing cache configuration in endpoint route builders.
- The endpoint does NOT use `PaginatedResults<T>` — this is a single aggregated response.
- The `server/src/main.rs` file mounts all modules; since this is a new route within the existing SBOM module, no changes to `main.rs` should be needed.
- Per `docs/constraints.md` §5.1: changes must be scoped to the files listed.
- Per `docs/constraints.md` §5.3: follow the patterns referenced in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; follow its path parameter extraction, service call, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; add the new route alongside existing ones
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for Axum

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response includes cache headers with 5-minute TTL
- [ ] Route is registered in the SBOM endpoints module
- [ ] Handler follows the existing Axum handler pattern (`Result<Json<T>, AppError>`)

## Test Requirements
- [ ] Endpoint returns 200 with correct severity counts for a valid SBOM
- [ ] Endpoint returns 404 for a nonexistent SBOM ID
- [ ] Response content-type is `application/json`
- [ ] Response body matches the `AdvisorySeveritySummary` schema

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — should return severity summary JSON (with running server)

## Documentation Updates
- `docs/api/` or REST API reference — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation including path, parameters, response shape, and cache behavior

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary Response Model
- Depends on: Task 2 — Add Advisory Summary Service Method to SbomService
