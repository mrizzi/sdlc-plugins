# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Description
Add a new Axum endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The handler extracts the SBOM ID from the path, an optional `threshold` query parameter, calls `SbomService::get_advisory_summary`, and returns the `AdvisorySeveritySummary` as JSON. The endpoint must return 404 if the SBOM does not exist and include 5-minute `tower-http` cache configuration.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new route `/api/v2/sbom/{id}/advisory-summary` with cache middleware

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler function

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns filtered counts for severities at or above the specified threshold

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for `GET /api/v2/sbom/{id}` — use `Path<Uuid>` extractor for the SBOM ID and `Query<ThresholdQueryParam>` for the optional threshold.
- Define a `ThresholdQueryParam` struct with `pub threshold: Option<String>` deriving `Deserialize` in the handler file, following the query parameter pattern used by sibling endpoints.
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` with `.context()` error wrapping, consistent with the error handling pattern in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. Follow the route registration pattern used for `list.rs` and `get.rs`.
- Configure 5-minute caching using `tower-http` caching middleware on the route builder, following the caching pattern described in the repository conventions (cache configuration in endpoint route builders).
- The endpoint path should be nested under the existing `/api/v2/sbom/{id}` prefix to maintain consistency with the URL structure.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for Path extraction, service invocation, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern and tower-http cache middleware setup
- `common/src/error.rs::AppError` — error type for 404 and other error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Endpoint returns 404 when the SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters severity counts
- [ ] Response includes appropriate cache headers (5-minute max-age)
- [ ] Route is registered in the SBOM endpoints module

## Test Requirements
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a valid SBOM
- [ ] Integration test: returns 404 for a non-existent SBOM ID
- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: response for SBOM with no advisories returns all-zero counts
- [ ] Integration test: verify cache-control header is present with max-age=300

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test --test api sbom::advisory_summary` — integration tests should pass

## Dependencies
- Depends on: Task 2 — Add advisory severity aggregation service method
