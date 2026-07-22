# Task 3: Add advisory-summary endpoint with caching

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::get_advisory_summary` and returns the severity counts as JSON. The endpoint must support an optional `?threshold=critical|high|medium|low` query parameter. Configure `tower-http` caching middleware with a 5-minute TTL on this route. Register the route in the SBOM endpoint module.

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `200 OK` with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns `404 Not Found` when the SBOM ID does not exist
- [ ] Optional `?threshold=` query parameter filters severity counts to only include severities at or above the specified level
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Route is registered in the SBOM endpoints module alongside existing SBOM routes
- [ ] Endpoint is documented with `utoipa` attributes for OpenAPI spec generation

## Test Requirements

- [ ] Handler unit test verifies 200 response with correct JSON structure for valid SBOM
- [ ] Handler unit test verifies 404 response for nonexistent SBOM
- [ ] Handler unit test verifies threshold query parameter is parsed and passed to service
- [ ] Handler unit test verifies Cache-Control header is present with max-age=300

## Dependencies

- Task 2 (advisory severity aggregation service) -- requires `SbomService::get_advisory_summary`

## API Changes

- **New endpoint**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Parameters**: `id` (path, UUID, required), `threshold` (query, string, optional, enum: critical|high|medium|low)
  - **Response 200**: `{ "critical": u64, "high": u64, "medium": u64, "low": u64, "total": u64 }`
  - **Response 404**: Standard error body when SBOM not found
  - **Cache**: `Cache-Control: max-age=300`

## Files to Create

- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- handler function for the advisory-summary endpoint

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes

## Implementation Notes

- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` which extracts path parameters, calls a service method, and returns `Result<Json<T>, AppError>`.
  - Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` and modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/` scope.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the existing `get` and `list` routes.
  - Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Use `tower-http` caching middleware as described in the caching convention. Apply `SetResponseHeader` or a cache layer on the route builder to add `Cache-Control: max-age=300`.
  - Applies: task creates an endpoint file matching the convention's caching scope.
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` following the error handling convention, using `.context()` for wrapping errors from the service layer.
  - Applies: task creates handler code matching the convention's error handling scope.
- Use Axum's `Query<T>` extractor for the optional threshold parameter, defining a query params struct with `threshold: Option<SeverityThreshold>`.
