## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::get_advisory_severity_summary` method (from Task 1), applies 5-minute caching via the existing `tower-http` caching middleware, and supports an optional `?threshold` query parameter to filter counts at or above a given severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: i64, high: i64, medium: i64, low: i64, total: i64 }`. Returns 404 if SBOM ID does not exist. Supports optional `?threshold=critical|high|medium|low` query parameter to filter counts at or above the specified severity level.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for handler function structure: path parameter extraction, service call, response serialization, error handling.
- The handler should extract the SBOM ID from the path using Axum's `Path` extractor, consistent with `get.rs`.
- Define an optional `threshold` query parameter using Axum's `Query` extractor. Parse the threshold value as a severity enum (`critical`, `high`, `medium`, `low`). When present, filter the `AdvisorySeveritySummary` to include only counts at or above the specified severity and recalculate `total`.
- Apply 5-minute caching using the existing `tower-http` caching middleware configuration pattern. See how caching is configured in existing endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` routes are registered. The new route should be `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` or equivalent.
- Return `Json<AdvisorySeveritySummary>` as the success response type, or `AppError` for errors.
- Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` and mount via `server/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for the 5-minute cache requirement.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint configuration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler for `/api/v2/sbom/{id}`; use as structural template for path parameter extraction, service injection, and error response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; follow the same pattern for adding the new route
- `common/src/error.rs::AppError` — error type implementing `IntoResponse` for Axum error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical, high, medium, low, total }` with correct counts
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes using existing cache infrastructure
- [ ] Optional `?threshold=critical` query parameter filters counts to only severity levels at or above the threshold
- [ ] Route is registered and accessible via the Axum server

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a known SBOM
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for a non-existent SBOM ID
- [ ] Integration test: `?threshold=critical` returns only critical count and recalculated total
- [ ] Integration test: `?threshold=high` returns critical and high counts with recalculated total

## Verification Commands
- `cargo test --test api -- sbom::advisory_summary` — expected: all advisory summary integration tests pass

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method

[sdlc-workflow] Description digest: sha256-md:723683f3a9ee18cb50525044b90c6a81f5bee9d58111a3ef9816b35720347716
