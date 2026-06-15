## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated severity counts for a given SBOM. The endpoint delegates to the service method, applies 5-minute caching via tower-http middleware, and supports an optional `threshold` query parameter for severity filtering.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/advisory-summary` route with 5-minute cache configuration

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Handler function for GET /api/v2/sbom/{id}/advisory-summary

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter

## Implementation Notes
1. **Handler function**: Create the endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`. The handler should:
   - Extract `id` from the path using Axum's `Path<Uuid>` extractor
   - Extract the optional `threshold` query parameter using `Query<ThresholdParams>` where `ThresholdParams` is a small struct with `threshold: Option<String>`
   - Call `SbomService::advisory_severity_summary(id, threshold)` 
   - Return `Json<AdvisorySeveritySummary>` on success
   - Return the `AppError` (from `common/src/error.rs`) directly on failure (404 for missing SBOM, 500 for DB errors)

2. **Route registration**: In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the route following the existing patterns for `list.rs` and `get.rs` registration. Register as `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))`.

3. **Caching**: Apply tower-http caching middleware with a 300-second (5-minute) TTL on the route, consistent with the caching approach described in the repo conventions. Use the same middleware pattern used for other cached routes.

4. **OpenAPI schema**: Add `#[utoipa::path]` attribute to the handler with appropriate `params`, `responses`, and `tag` annotations, following the documentation pattern in existing endpoint files like `modules/fundamental/src/sbom/endpoints/get.rs`.

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.

Per CONVENTIONS.md §Caching: uses `tower-http` caching middleware; cache configuration in endpoint route builders.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's caching scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` JSON response
- [ ] Endpoint returns 404 when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (Cache-Control header set)
- [ ] Optional `?threshold` query parameter filters counts to only include severities at or above the threshold
- [ ] OpenAPI schema is annotated on the handler

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo run -- &; curl -s http://localhost:8080/api/v2/sbom/{test-id}/advisory-summary | jq .` — returns JSON with severity counts

## Dependencies
- Depends on: Task 2 — Add severity aggregation service method

[sdlc-workflow] Description digest: sha256-md:d17aff11ea44b6c36e67af008a56c7976a1e2c80b29220cbe443a2d457abe7fc
