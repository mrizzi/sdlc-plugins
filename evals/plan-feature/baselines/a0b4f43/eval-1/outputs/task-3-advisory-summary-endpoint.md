## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler and register it in the SBOM endpoint module's route configuration. This endpoint calls the `SbomService::advisory_severity_summary` method and returns the `AdvisorySeveritySummary` as a JSON response. The endpoint must include 5-minute cache configuration using the existing `tower-http` caching middleware pattern. This is the primary deliverable of feature TC-9001, enabling frontend dashboard widgets to fetch pre-computed severity breakdowns in a single API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new advisory-summary route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }` as JSON with 5-minute cache headers. Returns 404 if SBOM ID does not exist.

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`). This file demonstrates the handler function signature, path parameter extraction, service injection, error propagation, and JSON response construction used throughout the codebase.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` — this file shows how routes are registered using Axum's router builder. Add the new route alongside the existing `/api/v2/sbom/{id}` route.
- Use `tower-http` caching middleware for the 5-minute cache. The Key Conventions section of the repository structure notes: "Uses tower-http caching middleware; cache configuration in endpoint route builders." Apply cache configuration at the route level following the existing pattern.
- The handler function should: extract the SBOM ID from the path, call `SbomService::advisory_severity_summary`, and return `Json(summary)` on success or propagate the `AppError` on failure.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the codebase convention documented in the repository structure's Key Conventions.
- Per docs/constraints.md section 2 (Commit Rules): commit must reference Jira issue ID and follow Conventional Commits format.
- Per docs/constraints.md section 3 (PR Rules): branch must be named after Jira issue ID; PR link must be posted to Jira task.
- Per docs/constraints.md section 5 (Code Change Rules): inspect code before modifying (constraint 5.2), follow patterns in Implementation Notes (constraint 5.3).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Demonstrates the handler pattern for `GET /api/v2/sbom/{id}` with path parameter extraction and service call
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Shows route registration pattern for SBOM endpoints
- `modules/fundamental/src/advisory/endpoints/get.rs` — Another example of a GET handler returning a single entity with error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` endpoint is accessible and returns JSON with fields: critical, high, medium, low, total
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response includes cache headers indicating a 5-minute cache duration
- [ ] Route is registered in the SBOM endpoint module alongside existing routes
- [ ] Code compiles and existing tests pass without regression

## Test Requirements
- [ ] Integration test: endpoint returns 200 with correct severity counts for an SBOM with linked advisories
- [ ] Integration test: endpoint returns 404 for a non-existent SBOM ID
- [ ] Integration test: response contains expected JSON shape with all severity fields
- [ ] Integration test: response includes cache-control headers with 5-minute max-age

## Verification Commands
- `cargo build` — project compiles without errors
- `cargo test` — all existing tests pass

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method
