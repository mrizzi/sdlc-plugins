## Repository
trustify-backend

## Target Branch
main

## Description
Create the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the advisory summary service and returns the severity counts as JSON. Register the route in the SBOM endpoints module with 5-minute `tower-http` caching. Support an optional `threshold` query parameter for filtering severity counts.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler for the advisory-summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route under `/api/v2/sbom/{id}/advisory-summary` with cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above the specified severity level. Returns 404 if SBOM ID does not exist. Response is cached for 5 minutes.

## Implementation Notes
Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for:
- Axum path extractor for the SBOM `{id}` parameter
- Axum query extractor for the optional `threshold` parameter
- Returning `Result<Json<AdvisorySeveritySummary>, AppError>` as the handler return type
- Service injection via Axum state

For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` which registers routes for `list.rs` and `get.rs`. Add the new route as a nested path under the existing SBOM route prefix.

For caching, use `tower-http` caching middleware as described in the repo conventions. Configure a 5-minute TTL on the route builder for the advisory-summary endpoint.

Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and they are mounted via `server/main.rs`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in endpoint route builders.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern for SBOM detail endpoint with path extractor
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error type implementing `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with severity counts
- [ ] Response shape matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `threshold` query parameter filters severity counts
- [ ] Response includes 5-minute cache headers via `tower-http` caching
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Endpoint returns 200 with correct severity counts for a valid SBOM
- [ ] Endpoint returns 404 for non-existent SBOM ID
- [ ] Threshold query parameter correctly filters the response
- [ ] Response includes appropriate cache-control headers

## Verification Commands
- `cargo build` — Confirms the endpoint compiles and route registration is correct
- `cargo test` — Confirms all tests pass including the new endpoint tests

## Documentation Updates
- `README.md` — Add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 3 — Add advisory summary aggregation service method