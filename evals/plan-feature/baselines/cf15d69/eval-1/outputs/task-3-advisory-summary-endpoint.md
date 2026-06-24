## Repository
trustify-backend

## Target Branch
main

## Description
Create the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` and register it in the SBOM route configuration. The endpoint extracts the SBOM ID from the path, an optional `threshold` query parameter, calls `SbomService::advisory_summary`, and returns the `AdvisorySeveritySummary` as JSON. A 5-minute cache TTL is configured using `tower-http` caching middleware on this route.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query param

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache TTL

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns aggregated severity counts `{ critical, high, medium, low, total }` for advisories linked to the specified SBOM
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: Returns only counts at or above the specified severity threshold

## Implementation Notes
Follow the handler patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. The handler should extract `Path(id)` for the SBOM UUID and `Query(params)` for the optional threshold parameter. Call `SbomService::advisory_summary(id, threshold)` and return `Json(result)`. Error cases are handled by `AppError`'s `IntoResponse` implementation from `common/src/error.rs`.

In `modules/fundamental/src/sbom/endpoints/mod.rs`, register the route following the same pattern used for `get.rs` and `list.rs`. Apply `tower-http` caching middleware with a 300-second (5-minute) max-age header.

Per Key Conventions (Endpoint registration): Each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per Key Conventions (Error handling): All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` files scope.

Per Key Conventions (Caching): Uses `tower-http` caching middleware; cache configuration in endpoint route builders. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint/caching scope.

Per Key Conventions (Framework): Axum for HTTP handlers. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` files scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` endpoint returns JSON with `{ critical, high, medium, low, total }` fields
- [ ] Endpoint returns HTTP 404 if SBOM ID does not exist
- [ ] Optional `?threshold=critical|high|medium|low` query param filters severity counts
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`

## Test Requirements
- [ ] Handler unit test for successful response shape
- [ ] Handler unit test for 404 when SBOM not found
- [ ] Handler unit test for threshold query parameter parsing

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental sbom::endpoints` — endpoint unit tests pass

## Dependencies
- Depends on: Task 2 — advisory summary service method

[sdlc-workflow] Description digest: sha256-md:53bd95fe491180e7caefac039ba07e2e0f040850d0a7aaa79add0db85e53f32c
