## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint. This endpoint calls the `SbomService::advisory_severity_summary` method created in Task 1 and returns the severity counts as JSON. The endpoint must return 404 if the SBOM ID does not exist, apply a 5-minute cache TTL via the existing tower-http caching middleware, and accept an optional `?threshold=critical|high|medium|low` query parameter to filter counts above a given severity level.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function `get_advisory_summary` that extracts SBOM ID from path, optional threshold from query, calls the service, returns JSON response with 5-minute cache header

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add `mod advisory_summary;` and register the `/api/v2/sbom/{id}/advisory-summary` route in the router
- `server/src/main.rs` — no changes expected if the SBOM module is already mounted, but verify the SBOM module router is included

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 OK
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered severity counts above the specified threshold
- Returns 404 if SBOM ID does not exist

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for path parameter extraction, error handling, and response structure. Use `axum::extract::Path` for the SBOM ID and `axum::extract::Query` for the optional threshold parameter.

The handler should:
1. Extract `id: Uuid` from path using `Path(id)` (same pattern as `get.rs`)
2. Extract optional `threshold: Option<SeverityThreshold>` from query using `Query`
3. Call `sbom_service.advisory_severity_summary(id, threshold).await`
4. On `Ok(summary)` return `Json(summary)` with status 200
5. On SBOM-not-found error, return 404 via `AppError` (from `common/src/error.rs`)

For caching, apply the `tower-http` cache control layer to this route with a 5-minute (300s) max-age. Follow the existing caching pattern described in the repo conventions: cache configuration in endpoint route builders.

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes (list.rs, get.rs). The route registration pattern uses Axum's `.route()` method chaining.

Per CONVENTIONS.md: endpoint registration goes in each module's `endpoints/mod.rs`; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler; reuse the same Path extraction, error handling, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` — error type for 404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] Response includes `Cache-Control: max-age=300` header (5-minute cache)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and total
- [ ] Endpoint is registered at the correct path and accessible via the server

## Test Requirements
- [ ] Handler returns 200 with correct severity counts for an SBOM with known advisories
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Handler returns correct filtered counts when threshold query param is provided
- [ ] Response Content-Type is application/json

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `curl -s http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary | jq .` — returns severity summary JSON

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model and aggregation service
