## Repository
trustify-backend

## Target Branch
main

## Description
Add the REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method (created in Task 1), applies an optional `?threshold` query parameter to filter counts above a given severity level, wraps the response with a 5-minute cache header via tower-http caching middleware, and returns 404 if the SBOM does not exist.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function `advisory_summary` that extracts the SBOM ID from the path, optional `threshold` query parameter, calls `SbomService::advisory_severity_summary`, applies threshold filtering if specified, and returns the response as JSON with cache control headers

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route `GET /api/v2/sbom/{id}/advisory-summary` in the SBOM router, add `pub mod advisory_summary;`, configure 5-minute cache via tower-http layer on this route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns only severity counts at or above the specified threshold level

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, error handling, and response formatting.
- The handler signature should follow the Axum extractor pattern: `async fn advisory_summary(Path(id): Path<Uuid>, Query(params): Query<ThresholdParams>, State(service): State<SbomService>) -> Result<Json<AdvisorySeveritySummary>, AppError>`.
- Define a `ThresholdParams` struct with an optional `threshold` field (e.g., `Option<String>` or a severity enum). Valid values: "critical", "high", "medium", "low". When specified, zero out counts below the threshold level and recalculate total.
- For caching, apply the tower-http `CacheControl` layer to this specific route, matching the existing caching configuration patterns in the codebase. Set `max-age=300` (5 minutes).
- Return 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints. The `AppError` enum (see `common/src/error.rs`) already handles this pattern — use `.context()` on the service call.
- Per CONVENTIONS.md §Endpoint Registration: register the route in `endpoints/mod.rs` following the existing pattern for route mounting. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoints/ directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` and use `.context()` wrapping on all fallible operations. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's .rs handler file scope.
- Per CONVENTIONS.md §Caching: use tower-http caching middleware for cache control headers. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint handler scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET /api/v2/sbom/{id} handler; follow the same pattern for path extraction, service call, error handling, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; follow existing `.route()` calls to add the new endpoint
- `common/src/error.rs::AppError` — error type for 404 and other error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with fields: critical, high, medium, low, total
- [ ] Response includes Cache-Control header with max-age=300
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `?threshold=<severity>` query parameter filters counts to only include severities at or above the threshold
- [ ] Endpoint is registered in the SBOM route group and accessible at the correct path
- [ ] Response time target: p95 < 200ms for SBOMs with up to 500 advisories

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct severity counts
- [ ] Test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for non-existent SBOM
- [ ] Test: Response includes Cache-Control header with max-age=300
- [ ] Test: ?threshold=critical returns only critical count and total
- [ ] Test: ?threshold with invalid value returns 400

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{id}/advisory-summary | jq .` — returns severity count JSON
- `curl -sI http://localhost:8080/api/v2/sbom/{id}/advisory-summary | grep Cache-Control` — shows max-age=300

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists
- API documentation (OpenAPI/Swagger spec if present) — add endpoint path, query parameters, request/response schema, and 404 error response

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service

---
[sdlc-workflow] Description digest: sha256-md:e04dfc89111f7675d817b646d5aefab4f7d39e22959d4c534f44ba1cd3664116
