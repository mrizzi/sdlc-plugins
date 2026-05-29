## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::get_advisory_summary` and returns the severity counts as a JSON response. The endpoint must be registered in the SBOM route module and configured with 5-minute `tower-http` caching middleware. The endpoint returns 404 if the SBOM ID does not exist, consistent with other SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 200 OK, or 404 if SBOM not found

## Implementation Notes
- Follow the existing endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) — it extracts the SBOM ID from the path, calls a service method, and returns the result as JSON.
- The handler function signature should follow the Axum pattern: accept path parameters and the service as state, return `Result<Json<AdvisorySeveritySummary>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. Follow the same route registration pattern used for `list.rs` and `get.rs`.
- Configure `tower-http` caching middleware for the route with a 5-minute TTL. Reference the existing cache configuration patterns described in the repository conventions — cache configuration is done in endpoint route builders.
- The 404 response for non-existent SBOM IDs should be handled by the service layer error propagation (the service method returns an `AppError` that implements `IntoResponse`), so the handler does not need explicit 404 logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler for SBOM details, demonstrating path parameter extraction and service call pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type that handles 404 responses via `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `AdvisorySeveritySummary` JSON for a valid SBOM
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes correct `Cache-Control` headers for 5-minute caching
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Verify cache headers are present in the response

## Verification Commands
- `cargo build` — verify compilation succeeds
- `cargo test` — verify all tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model
- Depends on: Task 2 — Add severity aggregation service method

[sdlc-workflow] Description digest: sha256:fb129369d61b74a7a1a86f6860a2f21115fd8ee1f9d964276d026eacb7c4087c
