# Task 3: Create the advisory-summary endpoint with caching

## Repository

trustify-backend

## Target Branch

main

## Dependencies

- Task 2 (severity aggregation query in SbomService)

## Description

Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls `SbomService::advisory_severity_summary` and returns the severity counts as JSON. The endpoint must include a 5-minute cache header using the existing `tower-http` caching middleware, consistent with other cached endpoints in the codebase. Register the new route in the SBOM endpoint module.

## Files to Create

- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new route under `/api/v2/sbom/{id}/advisory-summary`

## API Changes

- **New endpoint**: `GET /api/v2/sbom/{id}/advisory-summary`
- **Response**: `200 OK` with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- **Error responses**: `404 Not Found` when SBOM ID does not exist
- **Cache**: `Cache-Control: max-age=300` (5 minutes) via tower-http caching middleware

## Implementation Notes

- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for extracting path parameters, calling the service, and returning JSON responses.
- The handler signature should follow the Axum extractor pattern: `async fn advisory_summary(Path(id): Path<Uuid>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same `.route()` builder pattern as existing routes like `get.rs` and `list.rs`.
- Apply the 5-minute cache using `tower-http` caching middleware on the route builder, consistent with the caching approach documented in the repo conventions.
- The handler should call `service.advisory_severity_summary(id, &db).await?` and wrap the result in `Json()`.

### Applicable Conventions

- **Endpoint registration**: Applies: task creates `advisory_summary.rs` and modifies `mod.rs` matching the convention's endpoints directory scope (`modules/fundamental/src/sbom/endpoints/`).
- **Error handling**: Applies: task creates an endpoint handler matching the convention's Rust handler scope -- all handlers return `Result<T, AppError>`.
- **Framework (Axum)**: Applies: task creates a new Axum route handler matching the convention's HTTP framework scope.

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Handler follows existing Axum extractor and error handling patterns

## Test Requirements

- [ ] Integration test: valid SBOM ID returns 200 with correct JSON shape
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response headers include cache-control with max-age=300

## Documentation Updates

- Add the new endpoint to the REST API reference documentation
- Document the response schema, path parameters, and cache behavior

[Description digest: sha256-md:c5f9d4e3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5 would be posted as a comment]
