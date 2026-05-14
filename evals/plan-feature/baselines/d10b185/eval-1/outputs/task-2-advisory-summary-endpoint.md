# Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The endpoint delegates to the `SbomService::get_advisory_severity_summary` method (from Task 1), applies a 5-minute cache via `tower-http` caching middleware, and supports an optional `?threshold` query parameter that filters counts to only severities at or above the specified level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler function for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts SBOM ID from path, optional `threshold` from query params, calls `SbomService::get_advisory_severity_summary`, applies threshold filtering if present, returns JSON response with 5-minute cache header.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route with `tower-http` caching middleware configured for 5-minute TTL. Add `pub mod advisory_summary;`.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Returns 404 if SBOM ID does not exist. Supports optional `?threshold=critical|high|medium|low` query parameter to filter counts to severities at or above the specified level.

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for handler function signature, path parameter extraction, error handling with `Result<T, AppError>`, and response construction.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for mounting the new route alongside existing SBOM routes.
- Use `tower-http` caching middleware as described in the repository conventions (Key Conventions section). Configure the cache TTL to 5 minutes (300 seconds) using the same cache configuration pattern used by other endpoint route builders.
- The `threshold` query parameter is optional and accepts one of: `critical`, `high`, `medium`, `low`. When present, zero out severity counts below the threshold level. The `total` field should reflect only the filtered counts.
- Handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the pattern of existing handlers that return `Result<T, AppError>` with `.context()` wrapping (per `common/src/error.rs`).
- Per `docs/constraints.md` section 5.3: follow patterns referenced in Implementation Notes. Per section 5.1: keep changes scoped to listed files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for handler function signature, path extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Reference for route registration and middleware configuration
- `common/src/error.rs::AppError` — Error type for returning 404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns HTTP 404 when SBOM ID does not exist
- [ ] Response includes cache headers with 5-minute TTL
- [ ] Optional `?threshold` parameter filters severity counts correctly
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Verify handler returns correct JSON shape for a valid SBOM ID
- [ ] Verify handler returns 404 for a non-existent SBOM ID
- [ ] Verify `?threshold=critical` returns only the critical count (others zeroed) with adjusted total
- [ ] Verify `?threshold=high` returns critical and high counts with others zeroed

## Verification Commands
- `cargo build` — compiles without errors
- `cargo test` — all existing tests continue to pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and SbomService aggregation method
