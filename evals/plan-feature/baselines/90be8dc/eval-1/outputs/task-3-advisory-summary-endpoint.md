## Repository
trustify-backend

## Description
Add a new Axum HTTP handler for `GET /api/v2/sbom/{id}/advisory-summary` that calls the advisory severity aggregation service and returns the summary as JSON. Register the route in the SBOM endpoint module so it is mounted by the server.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function for the advisory-summary endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` JSON response with aggregated advisory severity counts for the specified SBOM

## Implementation Notes
Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler structure:

1. Extract the SBOM ID from the path using Axum's `Path<String>` or `Path<Uuid>` extractor, matching the existing pattern in `get.rs`.
2. Obtain the `SbomService` from Axum's state/extension, following the same dependency injection pattern as other SBOM handlers.
3. Call `sbom_service.get_advisory_severity_summary(id)` from Task 2.
4. Return `Json<AdvisorySeveritySummary>` on success, or let `AppError` handle the 404/error response via its `IntoResponse` implementation from `common/src/error.rs`.
5. In `modules/fundamental/src/sbom/endpoints/mod.rs`, add a `.route("/{id}/advisory-summary", get(advisory_summary::handler))` call to the existing SBOM router, following the pattern used for `get.rs` route registration.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for path parameter extraction, service injection, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Automatic error-to-response conversion

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Route is registered in the SBOM router in `endpoints/mod.rs`
- [ ] Handler follows existing endpoint conventions (error handling, service injection, response type)

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors
- `cargo build` — Full project builds successfully

## Dependencies
- Depends on: Task 2 — Implement advisory severity aggregation service
