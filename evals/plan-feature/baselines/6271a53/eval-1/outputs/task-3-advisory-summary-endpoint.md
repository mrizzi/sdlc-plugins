# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint calls the `SbomService::advisory_severity_summary` method, applies 5-minute `tower-http` cache configuration, and supports an optional `?threshold` query parameter to filter counts above a specified severity level. Returns 404 if the SBOM does not exist.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query parameter support

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache middleware

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters counts to only include severities at or above the specified threshold

## Implementation Notes
- Follow the endpoint handler pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction, service injection, error handling (`Result<T, AppError>`), and response construction.
- Route registration pattern: see `modules/fundamental/src/sbom/endpoints/mod.rs` for how existing routes are registered (e.g., `list.rs`, `get.rs`). Add the new route following the same pattern.
- Cache configuration: use `tower-http` caching middleware with a 5-minute TTL. Reference the cache configuration approach described in the Key Conventions section of the repository structure (caching middleware on endpoint route builders).
- The optional `?threshold` query parameter should accept values: `critical`, `high`, `medium`, `low`. When present, only severity counts at or above the specified threshold are included in the response. Use Axum's `Query` extractor for the optional parameter.
- The threshold severity ordering is: critical > high > medium > low. When `?threshold=high`, return counts for `critical` and `high` only (set `medium` and `low` to 0 or omit them). Adjust `total` accordingly.
- Return HTTP 404 if the SBOM does not exist, consistent with the existing `GET /api/v2/sbom/{id}` endpoint behavior.
- Per constraints doc section 5.2: inspect `modules/fundamental/src/sbom/endpoints/get.rs` and `mod.rs` before implementing to confirm exact handler signature patterns, middleware application, and route registration.
- Per constraints doc section 5.4: reuse existing error handling patterns and response construction rather than introducing new patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler for `GET /api/v2/sbom/{id}`, reference for path param extraction and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern with cache middleware
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction (pagination params)
- `common/src/error.rs::AppError` — error handling with `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with severity counts JSON
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes using `tower-http` cache middleware
- [ ] Optional `?threshold` query parameter filters counts to severities at or above the threshold
- [ ] Response shape matches: `{ critical: N, high: N, medium: N, low: N, total: N }`

## Test Requirements
- [ ] Integration test: successful response with correct severity counts for a known SBOM
- [ ] Integration test: 404 response for non-existent SBOM ID
- [ ] Integration test: `?threshold=critical` returns only critical count (others are 0 or omitted), total adjusted
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: response without threshold returns all severity levels
- [ ] Integration test: verify response Content-Type is application/json

## Verification Commands
- `cargo test --test api advisory_summary` — run integration tests for the new endpoint

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to SbomService
