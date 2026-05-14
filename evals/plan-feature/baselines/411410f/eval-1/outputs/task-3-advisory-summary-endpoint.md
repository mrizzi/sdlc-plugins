## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/{id}/advisory-summary` HTTP endpoint handler and register it in the SBOM route tree. This endpoint calls `SbomService::get_advisory_severity_summary`, returns the aggregated severity counts as JSON, and applies 5-minute caching via `tower-http` middleware. It also accepts an optional `?threshold` query parameter.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function `get_advisory_summary` that extracts the SBOM ID from the path, the optional `threshold` query parameter, calls the service method, and returns `Json<AdvisorySeveritySummary>` or an `AppError` response.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod advisory_summary;` and register the new route `GET /:id/advisory-summary` in the existing SBOM router, with `tower-http` cache layer set to a 5-minute TTL.

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting path parameters (`Path<Uuid>`), injecting service dependencies (`State` or `Extension`), and returning `Result<Json<T>, AppError>`.
- Define a `ThresholdQuery` struct with `#[derive(Deserialize)]` containing `pub threshold: Option<String>` for the query parameter extraction, using Axum's `Query<ThresholdQuery>` extractor.
- For caching, follow the existing pattern referenced in the conventions: use `tower-http` caching middleware. Apply a `CacheControl` header with `max-age=300` (5 minutes) and `public` directives. Check how existing endpoints in `modules/fundamental/src/sbom/endpoints/mod.rs` configure route-level middleware and replicate the pattern.
- The handler signature should look like: `pub async fn get_advisory_summary(Path(id): Path<Uuid>, Query(params): Query<ThresholdQuery>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the route using `.route("/:id/advisory-summary", get(advisory_summary::get_advisory_summary))` following the pattern of existing routes like `get.rs` being mounted on `/:id`.
- Add `#[utoipa::path]` attribute to the handler for OpenAPI spec generation, documenting the path parameter, query parameter, success response (200 with `AdvisorySeveritySummary`), and error response (404).

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body matching `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Optional `?threshold=critical` query parameter is accepted and filters results
- [ ] Response includes `Cache-Control: public, max-age=300` header
- [ ] Route is registered in the SBOM router in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler is annotated with `#[utoipa::path]` for OpenAPI spec

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{valid_id}/advisory-summary` returns 200 with correct JSON shape
- [ ] Integration test: `GET /api/v2/sbom/{invalid_id}/advisory-summary` returns 404
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns filtered counts
- [ ] Integration test: Response headers include `Cache-Control` with `max-age=300`

## Dependencies
- Depends on: Task 2 — Aggregation service (provides `SbomService::get_advisory_severity_summary`)
