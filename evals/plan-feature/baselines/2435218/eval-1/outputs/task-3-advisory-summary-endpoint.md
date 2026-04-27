# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary Endpoint

## Repository
trustify-backend

## Description
Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns advisory severity counts for a given SBOM. The endpoint must call the `SbomService` aggregation method (Task 2) and return the `AdvisorySeveritySummary` as a JSON response. The endpoint must support 5-minute response caching using the existing `tower-http` caching middleware infrastructure. It must also support an optional `?threshold=<severity>` query parameter to filter counts at or above a given severity level (non-MVP but included for completeness).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint, including the optional `threshold` query parameter logic

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route alongside existing SBOM routes, with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns only severity counts at or above the specified threshold

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for path parameter extraction (`{id}`), service injection, error handling, and response type.
- Follow the route registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for adding the new route — observe how existing routes like `get.rs` and `list.rs` are registered.
- The handler should return `Result<Json<AdvisorySeveritySummary>, AppError>` following the Axum handler convention used throughout the codebase.
- For caching: use the `tower-http` caching middleware already configured in the project. Reference existing endpoint route builders in `modules/fundamental/src/sbom/endpoints/mod.rs` for how cache configuration is applied. Set a 5-minute TTL.
- For the `threshold` query parameter: accept an optional query param `threshold` whose value is one of `critical`, `high`, `medium`, `low`. When provided, zero out severity counts below the threshold and recalculate the total. This is non-MVP but should be included.
- Return 404 when the SBOM ID does not exist, propagated from the service layer.
- Per constraints doc section 5.3: follow patterns referenced in Implementation Notes.
- Per constraints doc section 2: commits must reference TC-9001 and use Conventional Commits format.
- Per constraints doc section 3.1: feature branch must be named after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET endpoint; pattern reference for path parameter extraction, service injection, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern and cache middleware configuration
- `common/src/error.rs::AppError` — error handling for 404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts in JSON format
- [ ] Response includes fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes
- [ ] Optional `?threshold=<severity>` query parameter filters counts at or above the threshold
- [ ] Endpoint is registered and accessible when server starts

## Test Requirements
- [ ] Integration test: GET advisory-summary returns 200 with correct counts for an SBOM with known advisories
- [ ] Integration test: GET advisory-summary returns 404 for non-existent SBOM
- [ ] Integration test: GET advisory-summary with `?threshold=critical` returns only critical count (others zeroed) and adjusted total
- [ ] Integration test: GET advisory-summary with `?threshold=high` returns critical and high counts
- [ ] Integration test: verify response JSON structure matches expected schema

## Verification Commands
- `cargo test -p trustify-fundamental -- advisory_summary` — run advisory-summary related tests
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — verify endpoint returns expected JSON response

## Documentation Updates
- `README.md` — add the new endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary Response Model
- Depends on: Task 2 — Add Advisory Severity Aggregation Query to SbomService
