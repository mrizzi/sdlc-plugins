## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler with 5-minute cache-control headers and optional `?threshold` query parameter. This endpoint calls the service method from Task 2 and returns the severity counts as JSON. It also supports an optional threshold filter that returns only severity counts at or above the specified severity level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — new endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new advisory-summary route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache header
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: optional query parameter to filter counts at or above the given severity level

## Implementation Notes
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function signatures, route registration, and response construction.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same pattern as `get.rs` and `list.rs` — add the route as a nested path under the existing `/api/v2/sbom/{id}` prefix.
- The handler should extract the SBOM `{id}` path parameter, call `SbomService::advisory_severity_summary()`, and return the result as JSON.
- Per Key Conventions §Endpoint registration: register the route in the module's `endpoints/mod.rs` and it will be mounted by `server/src/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Per Key Conventions §Caching: use `tower-http` caching middleware to set `Cache-Control: max-age=300` (5 minutes) on the response. Reference the existing caching configuration in endpoint route builders for the established pattern.
- For the `?threshold` query parameter: define an optional `Query<ThresholdParam>` extractor with a `threshold` field. When provided, zero out severity counts below the threshold level (e.g., `?threshold=high` returns critical and high counts, zeroes medium and low). Recompute `total` to match the filtered counts.
- Severity ordering for threshold: critical > high > medium > low.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for path parameter extraction, service injection, and JSON response construction for a single-SBOM endpoint
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — error handling for 404 and internal errors

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Endpoint returns HTTP 404 if the SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Optional `?threshold` query parameter filters counts to only include severities at or above the specified level
- [ ] Endpoint is registered in the SBOM module's route table
- [ ] Handler returns `Result<T, AppError>` per error handling conventions

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Integration test: response includes correct Cache-Control header

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method

[sdlc-workflow] Description digest: sha256-md:5285a132040ce1f725a3d8b36eed916ddab7d29f90766faab5a5fec98ff61ebe
