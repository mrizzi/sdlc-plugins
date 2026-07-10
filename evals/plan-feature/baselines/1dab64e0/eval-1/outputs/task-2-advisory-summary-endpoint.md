## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint returns 404 if the SBOM ID does not exist, supports an optional `?threshold=<severity>` query parameter to filter counts at or above the given severity level, and includes 5-minute response caching using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for GET /api/v2/sbom/{id}/advisory-summary with optional threshold query param

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`. Optional query param `?threshold=critical|high|medium|low` filters counts to only include severities at or above the given level.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, path parameter extraction, and error handling.
- Use `SbomService::get_advisory_summary` (from Task 1) to fetch the severity counts.
- Validate that the SBOM exists before calling the service method — return 404 using the same pattern as the existing `GET /api/v2/sbom/{id}` endpoint in `get.rs`.
- For the `?threshold` query parameter, define a query struct with an optional `threshold` field (enum: Critical, High, Medium, Low). Filter the response to zero out severity levels below the threshold.
- Configure 5-minute cache TTL using tower-http caching middleware in the route builder, following the caching pattern used by existing endpoints.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap errors with `.context()`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust syntax scope.
- Per CONVENTIONS.md §Endpoint registration: register the route in `endpoints/mod.rs` and ensure `server/main.rs` mounts the module.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Caching: use tower-http caching middleware configured in the endpoint route builder.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint for SBOM details; follow the same handler pattern, path extraction, and 404 handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow for the new endpoint
- `common/src/error.rs::AppError` — error type for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for a valid SBOM
- [ ] Returns 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints
- [ ] `?threshold=critical` returns only the critical count (other severity counts zeroed)
- [ ] Response is cached for 5 minutes
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: valid SBOM returns correct severity counts
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: `?threshold=high` returns only high and critical counts
- [ ] Integration test: response headers indicate cache configuration

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
