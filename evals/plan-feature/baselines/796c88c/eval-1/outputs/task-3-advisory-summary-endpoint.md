## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` HTTP endpoint handler. This handler extracts the SBOM ID from the path, calls the service method, applies 5-minute cache headers, and returns the `AdvisorySeveritySummary` as JSON. The endpoint is registered under the existing SBOM route group.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `pub async fn get_advisory_summary(Path(id): Path<Uuid>, State(service): State<SbomService>, db: Extension<impl ConnectionTrait>) -> Result<Json<AdvisorySeveritySummary>, AppError>` with cache-control headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod advisory_summary;` and register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::get_advisory_summary))`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns aggregated advisory severity counts (`{ critical, high, medium, low, total }`) for the specified SBOM. Returns 404 if SBOM not found. Response cached for 5 minutes via Cache-Control headers.

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, state access, and return type.
- Apply cache headers using `tower-http` caching middleware or by setting `Cache-Control: public, max-age=300` on the response, consistent with the project's caching convention described in the repo conventions.
- The handler is minimal: extract path param, call `service.advisory_summary(id, &db).await?`, wrap result in `Json()`.
- Register the route in the existing SBOM endpoint module's router setup in `endpoints/mod.rs`, following the pattern used by `get.rs` and `list.rs`.
- Return `AppError` directly from the `?` operator — the `IntoResponse` impl in `common/src/error.rs` handles 404 mapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern for `GET /api/v2/sbom/{id}` showing path extraction, service call, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — IntoResponse impl that converts `NotFound` to HTTP 404

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical, high, medium, low, total }`
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control` header with `max-age=300` (5-minute cache)
- [ ] Route is registered in SBOM endpoint module's router

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo run` then `curl http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary` — returns expected JSON

## Dependencies
- Depends on: Task 2 — Advisory summary service

## Applicable Conventions
- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `endpoints/` scope.
- **Error handling**: Applies: task modifies endpoint handler returning `Result<T, AppError>` matching the convention's error handling scope.
- **Caching**: Applies: task adds cache-control headers matching the convention's `tower-http` caching middleware scope.
- **Endpoint registration**: Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.

[sdlc-workflow] Description digest: sha256-md:1cdaf5ef3209976d641b1c638f11faac8433bb8411bc1acf9ef14e4b0872649e
