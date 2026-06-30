# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the new `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. This endpoint calls the `SbomService::get_advisory_severity_summary` method, applies 5-minute cache headers via `tower-http` caching middleware, and supports an optional `?threshold` query parameter for filtering severity levels. The endpoint follows existing SBOM endpoint patterns and is registered in the SBOM module's route configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary` that extracts the SBOM ID path parameter and optional `threshold` query parameter, calls the service method, and returns the `AdvisorySeveritySummary` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory_summary` route under `/api/v2/sbom/{id}/advisory-summary` with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 200 status; returns 404 if SBOM ID does not exist
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: optional query parameter to filter counts to only include severities at or above the given threshold

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for path parameter extraction, error handling, and response return conventions.
- The handler should:
  1. Extract `id` from path parameters (matching the pattern in `get.rs`)
  2. Extract optional `threshold` from query parameters using Axum's `Query` extractor
  3. Call `SbomService::get_advisory_severity_summary(id, threshold)`
  4. Return `Json(summary)` on success or propagate the `AppError` on failure
- All handlers return `Result<T, AppError>` with `.context()` wrapping — follow this pattern from `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern used for `list.rs` and `get.rs`.
- Apply `tower-http` caching middleware with a 5-minute TTL to the route. Reference existing cache configuration patterns in the endpoint route builders.
- The response Content-Type is `application/json`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details; demonstrates path parameter extraction, service call pattern, and error response handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for SBOM endpoints; shows how to mount new routes under `/api/v2/sbom`
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter handling for SBOM list endpoint

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON response shape `{ critical, high, medium, low, total }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts correctly
- [ ] Response includes cache headers with 5-minute TTL
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Integration test: response Content-Type is `application/json`
- [ ] Integration test: response includes appropriate cache-control headers

## Verification Commands
- `cargo build -p trustify-fundamental` — expected outcome: compiles without errors
- `cargo test --test api` — expected outcome: integration tests pass

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method to SbomService
