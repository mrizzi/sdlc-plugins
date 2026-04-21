# Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Repository
trustify-backend

## Description
Create the new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to the `AdvisoryService::get_severity_summary_for_sbom` method, applies a 5-minute response cache, and supports an optional `?threshold=` query parameter.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for `/api/v2/sbom/{id}/advisory-summary`
- `server/src/main.rs` — no changes expected if route mounting is already handled by the SBOM module's `endpoints/mod.rs`, but verify during implementation

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler function for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: returns only counts at or above the specified severity

## Implementation Notes
- Follow the endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — handlers extract path parameters, call a service method, and return a JSON response wrapped in `Result<Json<T>, AppError>`.
- Register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes (see `list.rs` and `get.rs` for the registration pattern).
- Apply `tower-http` caching middleware with a 5-minute TTL. Reference the caching approach documented in the repo conventions (Key Conventions: "Uses `tower-http` caching middleware; cache configuration in endpoint route builders").
- The `threshold` query parameter should be optional. Parse it as an enum or string matching one of: `critical`, `high`, `medium`, `low`.
- Return 404 if the SBOM ID does not exist — this is handled by `AdvisoryService::get_severity_summary_for_sbom` returning `AppError::NotFound`.
- Per constraints §5.3: follow patterns referenced in Implementation Notes. Per constraints §2.1–2.3: when committing, include Jira ID footer and Conventional Commits format.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM endpoint handler to follow as a pattern for path extraction and response wrapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error handling, `IntoResponse` implementation for 404

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns JSON `{ critical, high, medium, low, total }` with status 200
- [ ] Endpoint returns 404 if SBOM ID does not exist
- [ ] Response includes cache-control headers with a 5-minute TTL
- [ ] Optional `?threshold=critical|high|medium|low` query param filters severity counts
- [ ] Endpoint is registered and reachable through the Axum router

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct severity counts shape
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: response includes appropriate cache-control headers
- [ ] Integration test: `?threshold=high` returns only critical and high counts

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory-summary integration tests pass

## Documentation Updates
- `README.md` — add the new endpoint to the REST API reference section

## Dependencies
- Depends on: Task 2 — Add severity aggregation query to AdvisoryService
