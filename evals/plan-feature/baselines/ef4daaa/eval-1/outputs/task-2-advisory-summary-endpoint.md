# Task 2 — Add advisory summary endpoint with caching and route registration

## Repository
trustify-backend

## Description
Wire the advisory severity summary service method (from Task 1) into a new HTTP endpoint `GET /api/v2/sbom/{id}/advisory-summary`. Register the route in the SBOM endpoints module. Configure 5-minute caching using the existing `tower-http` caching middleware. Support the optional `?threshold` query parameter to filter severity counts above a given severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route
- `modules/fundamental/Cargo.toml` — add dependencies if needed for cache middleware

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns JSON `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters severity counts to only include levels at or above the specified threshold

## Implementation Notes
- Follow the endpoint pattern established by `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). The new handler should extract the SBOM ID from the path, call `SbomService::advisory_severity_summary`, and return the result as JSON or propagate the `AppError`.
- The handler function should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the established pattern in sibling endpoint files.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes. Follow the route registration pattern used for `list.rs` and `get.rs`.
- For the optional `?threshold` query parameter: define a query params struct (e.g., `AdvisorySummaryParams`) with an optional `threshold` field. When present, filter the response to only include severity levels at or above the threshold. Severity ordering: Critical > High > Medium > Low.
- The `?threshold` parameter is non-MVP but should be included in this implementation since it's a simple filter on the response struct.
- Configure 5-minute caching using `tower-http` caching middleware, following the cache configuration pattern documented in the repository's Key Conventions. Apply the cache layer to this specific route.
- Per constraints doc section 2.1-2.3: Commits must reference TC-9001 in the footer, follow Conventional Commits, and include the AI assistance trailer.
- Per constraints doc section 3.1: Feature branch must be named `TC-9001`.
- Per constraints doc section 5.1: Changes must be scoped to the files listed — no unrelated files.
- Per constraints doc section 5.3: Implementation must follow patterns referenced in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler for `GET /api/v2/sbom/{id}`; follow its pattern for path extraction, service call, and response return
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration file; follow its pattern for adding the new route
- `common/src/error.rs::AppError` — error type for consistent error responses (404 for missing SBOM)
- `common/src/model/paginated.rs::PaginatedResults` — example response wrapper pattern (this endpoint uses a simpler direct struct return)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical, high, medium, low, total }` for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes (cache-control headers present)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (other levels zeroed or omitted)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts
- [ ] Route is properly registered and accessible through the Axum router

## Test Requirements
- [ ] Integration test: successful response with correct severity counts for a known SBOM
- [ ] Integration test: 404 response for non-existent SBOM ID
- [ ] Integration test: threshold query parameter filters severity counts correctly
- [ ] Integration test: response includes appropriate cache-control headers

## Verification Commands
- `cargo test --test api -- advisory_summary` — run advisory summary integration tests
- `cargo build` — verify compilation succeeds

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
