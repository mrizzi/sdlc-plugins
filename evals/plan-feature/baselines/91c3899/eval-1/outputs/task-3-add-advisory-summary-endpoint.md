## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` HTTP endpoint that returns advisory severity counts for a given SBOM. This endpoint calls the service method added in Task 2 and returns the `AdvisorySeveritySummary` as a JSON response. It accepts an optional `?threshold` query parameter to filter counts by severity level. The endpoint must return 404 if the SBOM does not exist, consistent with existing SBOM endpoints.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for GET /api/v2/sbom/{id}/advisory-summary

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`. Accepts optional `?threshold=critical|high|medium|low` query parameter.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for the handler function signature, path parameter extraction, and error response mapping.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for the existing `list.rs` and `get.rs` route registrations.
- The handler should extract the SBOM ID from the path and the optional `threshold` query parameter, then call `SbomService::get_advisory_summary()`.
- Return `Json(summary)` on success. Let `AppError` handle the 404 mapping automatically via the `IntoResponse` implementation in `common/src/error.rs`.
- Define a query parameter struct (e.g., `AdvisorySummaryQuery`) with an optional `threshold: Option<String>` field, extracted via Axum's `Query` extractor.
- Per Error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.
- Per Endpoint registration convention: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Module pattern convention: each domain module follows model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoints directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow this handler's pattern for path parameter extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Follow the existing route registration pattern for adding the new route
- `common/src/error.rs::AppError` — Reuse for error-to-HTTP-status mapping (404 for not found)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON with severity counts
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Optional `?threshold` query parameter is accepted and passed to the service layer
- [ ] Route is registered in the SBOM module's route configuration
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: GET advisory-summary for a valid SBOM returns 200 with correct JSON shape
- [ ] Integration test: GET advisory-summary for non-existent SBOM returns 404
- [ ] Integration test: GET advisory-summary with `?threshold=critical` returns filtered counts

## Verification Commands
- `cargo check -p trustify-fundamental` — expected: compilation succeeds
- `cargo test -p trustify-tests` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model
- Depends on: Task 2 — Add advisory severity aggregation service
