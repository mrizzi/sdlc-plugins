## Repository
trustify-backend

## Description
Expose `GET /api/v2/sbom/{id}/advisory-summary` as an Axum handler that delegates to `SbomService::advisory_severity_summary` and applies a 5-minute `Cache-Control` header using the existing `tower-http` caching middleware already used elsewhere in the sbom endpoints module. Register the route in the sbom endpoints `mod.rs` and mount it through `server/main.rs` (no change to main.rs needed if the sbom router is already mounted at `/api/v2/sbom`).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add `pub mod advisory_summary;` and register the route `GET /:id/advisory-summary` on the sbom router with 5-minute cache middleware

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `AdvisorySeveritySummary` JSON `{ critical, high, medium, low, total }`; 404 if SBOM not found; `Cache-Control: max-age=300` on success responses

## Implementation Notes
Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs`, which handles `GET /api/v2/sbom/{id}`:

1. Extract `Path(sbom_id): Path<Uuid>` from the request.
2. Extract `State(service): State<SbomService>` and the database connection (check `get.rs` for the exact extractor pattern — it may use `Extension<DatabaseConnection>` or an `AppState` struct).
3. Call `service.advisory_severity_summary(sbom_id, &db).await?` — the `?` propagates `AppError` via its `IntoResponse` implementation in `common/src/error.rs`.
4. Return `Json(summary)` wrapped in `Ok(...)`.

For the 5-minute cache, inspect `modules/fundamental/src/sbom/endpoints/mod.rs` to see how existing routes apply `tower-http` cache middleware. The pattern likely uses `.layer(CacheLayer::new(...))` or a `cache_control` middleware call on the route. Apply the same middleware to the new route with `max-age=300`.

Handler signature example (adjust based on actual state extractor pattern in `get.rs`):
```rust
pub async fn get_advisory_summary(
    State(service): State<SbomService>,
    Extension(db): Extension<DatabaseConnection>,
    Path(sbom_id): Path<Uuid>,
) -> Result<Json<AdvisorySeveritySummary>, AppError> {
    let summary = service.advisory_severity_summary(sbom_id, &db).await?;
    Ok(Json(summary))
}
```

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern: `Path<Uuid>` extractor, `State<SbomService>`, `Result<Json<T>, AppError>` return type
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration and cache middleware application pattern
- `common/src/error.rs::AppError` — `IntoResponse` impl converts service errors to HTTP responses automatically

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{valid-id}/advisory-summary` returns HTTP 200 with correct JSON body
- [ ] `GET /api/v2/sbom/{nonexistent-id}/advisory-summary` returns HTTP 404
- [ ] Successful response includes `Cache-Control: max-age=300` header
- [ ] Route is reachable at `/api/v2/sbom/{id}/advisory-summary` (i.e., mounted correctly through the existing sbom router)
- [ ] `cargo check -p fundamental` and `cargo check -p server` pass with no warnings

## Verification Commands
- `curl -i http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — expect HTTP 200, `Cache-Control: max-age=300`, JSON with `critical/high/medium/low/total` keys
- `curl -i http://localhost:8080/api/v2/sbom/00000000-0000-0000-0000-000000000000/advisory-summary` — expect HTTP 404

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/{id}/advisory-summary` to the API endpoint listing with response shape and cache behavior documented

## Dependencies
- Depends on: Task 2 — Add `advisory_severity_summary` service method to `SbomService`
