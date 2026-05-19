## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint with 5-minute cache-control headers. This is the primary deliverable of feature TC-9001, exposing the severity aggregation to API consumers.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- Endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`. Extracts the SBOM `id` path parameter, calls `SbomService::advisory_severity_summary`, and returns the `AdvisorySeveritySummary` as JSON. Sets `Cache-Control: max-age=300` response header using `tower-http` caching middleware.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the new route `GET /{id}/advisory-summary` within the existing SBOM router group, following the pattern used for `list.rs` and `get.rs` routes.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Cache-Control: max-age=300`. Returns 404 if SBOM ID does not exist.

## Implementation Notes
Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` for the handler function signature. The handler should:
1. Accept `Path<Uuid>` for the SBOM ID (same pattern as `get.rs`).
2. Inject `SbomService` via Axum state extraction (same pattern as sibling endpoint handlers).
3. Call `SbomService::advisory_severity_summary(id)`.
4. Return `Result<Json<AdvisorySeveritySummary>, AppError>` -- the `AppError` type in `common/src/error.rs` implements `IntoResponse`, so 404 and 500 errors are handled automatically.
5. Apply cache-control using `tower-http` caching middleware configured in the route builder, consistent with the project's caching convention documented in the Key Conventions section of the repo structure.

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the same pattern as existing routes (e.g., how `get.rs` is registered as `GET /{id}`).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Follow handler signature, path extraction, service injection, and error handling patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Follow route registration pattern for adding the new route
- `common/src/error.rs::AppError` -- Reuse for automatic error-to-HTTP-status mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns a JSON response with fields `critical`, `high`, `medium`, `low`, `total`
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] Returns HTTP 404 when SBOM ID does not exist
- [ ] Returns HTTP 200 with correct severity counts for a valid SBOM
- [ ] Endpoint is registered and reachable in the running server

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct JSON shape for a valid SBOM
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 404 for an unknown SBOM ID
- [ ] Integration test: response includes `Cache-Control` header with max-age=300

## Verification Commands
- `cargo check -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental` -- all tests pass

## Dependencies
- Depends on: Task 2 -- Aggregation service method (provides `SbomService::advisory_severity_summary`)
