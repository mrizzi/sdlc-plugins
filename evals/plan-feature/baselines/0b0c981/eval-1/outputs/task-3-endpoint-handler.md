## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler and register its route in the SBOM endpoints module. The handler calls `SbomService::get_advisory_severity_summary`, returns the `AdvisorySeveritySummary` as JSON, and applies 5-minute cache headers using the existing `tower-http` caching middleware. The endpoint returns 404 if the SBOM does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new route `/api/v2/sbom/{id}/advisory-summary` and add `pub mod advisory_summary;`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns JSON `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` with 5-minute cache headers. Returns 404 if SBOM ID does not exist.

## Implementation Notes
Follow the existing endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). That file demonstrates the standard handler signature: an async function accepting Axum extractors (`Path<Uuid>`, `State<AppState>`), calling a service method, and returning `Result<Json<T>, AppError>`.

For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`. Existing routes are registered using Axum's router builder. Add the new route as:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))
```

For caching, apply `tower-http` caching middleware with a 5-minute max-age. Reference the existing cache configuration pattern in the SBOM endpoint route builders (documented in repo conventions: "Caching: Uses `tower-http` caching middleware; cache configuration in endpoint route builders").

The handler function should:
1. Extract the SBOM ID from the URL path using `Path<Uuid>`
2. Call `SbomService::get_advisory_severity_summary(sbom_id)` from the app state
3. Return `Json(summary)` on success, or propagate the `AppError` (including 404) on failure

Per constraints §5.2: inspect `modules/fundamental/src/sbom/endpoints/get.rs` and `mod.rs` before implementing.
Per constraints §5.3: follow the handler signature and route registration patterns from those files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET handler pattern for SBOM detail endpoint; follow the same function signature, extractor usage, and error propagation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern; follow the same router builder approach
- `modules/fundamental/src/advisory/endpoints/get.rs` — Alternative reference for GET handler patterns in the advisory domain

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` endpoint is registered and accessible
- [ ] Endpoint returns JSON with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 status when SBOM ID does not exist
- [ ] Response includes cache headers with 5-minute max-age
- [ ] Handler follows the existing Axum handler pattern (extractors, service call, error propagation)
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` returns 404
- [ ] Integration test: response includes appropriate cache headers

## Verification Commands
- `cargo test -p trustify-tests --test api` — expected: all integration tests pass

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method


[sdlc-workflow] Description digest: sha256:e9f7670cc4dc4e4e6ae3cf74a4d61c32512001675af3862c73d1dc199e9f0c92
