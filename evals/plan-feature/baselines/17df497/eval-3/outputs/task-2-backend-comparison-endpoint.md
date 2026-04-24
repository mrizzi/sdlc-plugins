# Task 2 — Backend comparison endpoint and route registration

## Repository
trustify-backend

## Description
Add the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters, invokes the `SbomService::compare()` method, and returns the structured JSON diff response. Register the new route in the SBOM module's endpoint configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint, query parameter extraction, and JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route and add `pub mod compare;`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` as JSON. Query params `left` and `right` are required UUIDs. Returns 400 if either param is missing. Returns 404 if either SBOM does not exist.

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` — these use Axum handler functions with typed extractors and return `Result<Json<T>, AppError>`.
- The route registration pattern is in `modules/fundamental/src/sbom/endpoints/mod.rs` — add the `/compare` path as a GET route alongside the existing `/` and `/{id}` routes.
- Use Axum's `Query` extractor to parse the `left` and `right` query parameters. Define a `CompareQuery` struct with `left: Uuid` and `right: Uuid` fields.
- Call `SbomService::compare(left, right)` and return the result as `Json(result)`.
- Validate that both query parameters are present and are valid UUIDs — Axum's typed extraction handles this automatically, returning 400 for invalid/missing params.
- The handler should follow the `Result<T, AppError>` return type pattern with `.context()` wrapping, consistent with other endpoints.
- Consider adding cache headers via `tower-http` caching middleware configuration on the route builder, consistent with existing endpoint patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference implementation for single-resource GET endpoint handler pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation for list endpoint with query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error handling for invalid parameters and not-found cases

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Invalid UUID format in query parameters returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Endpoint is registered in the SBOM module's route configuration
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with expected diff structure
- [ ] Integration test: missing `left` param returns 400
- [ ] Integration test: missing `right` param returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: both params present but invalid UUID format returns 400

## Verification Commands
- `cargo test --test api sbom::compare` — all comparison endpoint integration tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}"` — returns JSON with the six diff categories

## Dependencies
- Depends on: Task 1 — Backend SBOM comparison model and service
