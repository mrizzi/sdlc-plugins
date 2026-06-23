# Task 3: Add advisory-summary endpoint handler and route registration

## Repository
trustify-backend

## Target Branch
main

## Description
Create the HTTP endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that invokes the service method from Task 2 and returns the `AdvisorySeveritySummary` as JSON. Register the route in the SBOM endpoints module with 5-minute cache configuration using `tower-http` caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler function that extracts the SBOM ID from the path, optional `threshold` query parameter, calls `SbomService::advisory_severity_summary`, and returns `Json<AdvisorySeveritySummary>` or appropriate error response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add `mod advisory_summary;` declaration and register the new route `GET /api/v2/sbom/{id}/advisory-summary` in the route builder, with 5-minute (`300s`) cache configuration via `tower-http` caching middleware

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 200 status; returns 404 if SBOM does not exist
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — NEW: optional query parameter to filter counts to only include severities at or above the specified level

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (`Path(id): Path<Uuid>`) and service injection.
- For the optional query parameter, define a `#[derive(Deserialize)] struct AdvisorySummaryQuery { threshold: Option<SeverityThreshold> }` and extract with `Query(params): Query<AdvisorySummaryQuery>`.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the convention in existing endpoint handlers.
- For caching, reference how routes are configured in `modules/fundamental/src/sbom/endpoints/mod.rs` -- apply `tower-http` cache layer with `max-age=300` to the advisory-summary route specifically.
- For route registration, follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where existing routes like `get.rs` and `list.rs` are mounted. The new route nests under the existing `/api/v2/sbom/{id}/` prefix.
- Per Key Conventions §Endpoint registration: each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` handler files scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler signature, path extraction, service injection, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration and cache middleware configuration
- `common/src/error.rs::AppError` — error type that implements `IntoResponse` for automatic HTTP error mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body containing `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Optional `?threshold=critical` query parameter filters the severity counts
- [ ] Response has `Cache-Control: max-age=300` header (5-minute cache)
- [ ] Endpoint is registered and accessible via the server's route tree

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` for a valid SBOM returns 200 with correct JSON shape
- [ ] Integration test: `GET /api/v2/sbom/{nonexistent}/advisory-summary` returns 404
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns filtered counts
- [ ] Integration test: verify response `Content-Type` is `application/json`

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- sbom::endpoints` — endpoint tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
- Depends on: Task 2 — Add advisory severity aggregation query to SbomService

---

> [sdlc-workflow] Description digest: sha256-md:c9f3e6b28d5a107753f2c8946b7da0e23g0cbf04f6d83279eaf5b41c6f9d8032
