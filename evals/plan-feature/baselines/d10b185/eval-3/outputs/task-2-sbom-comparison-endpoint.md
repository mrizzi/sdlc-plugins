# Task 2 — Add SBOM comparison REST endpoint with integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the SBOM comparison service (from Task 1) as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The endpoint validates that both query parameters are present and are valid SBOM IDs, delegates to `SbomService::compare`, and returns the structured diff as JSON. This endpoint is consumed by the frontend comparison page.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that parses query params, calls the comparison service, and returns `SbomComparison` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod compare;` and register the `/compare` route in the router
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as `SbomComparison` JSON

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `get.rs`: define an async handler function that extracts query params, calls the service, and returns `Result<Json<T>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes. The route should be `.route("/compare", get(compare::handler))` added to the existing SBOM router.
- Query parameter extraction: use Axum's `Query<CompareParams>` extractor with a struct `CompareParams { left: String, right: String }`. Return `AppError` (400 Bad Request) if either parameter is missing.
- The handler should validate both SBOM IDs exist before calling `SbomService::compare`. If either SBOM does not exist, return a 404 with a descriptive error message.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test data in the PostgreSQL test database, call the endpoint via the test client, and assert on response status and body structure.
- Per non-functional requirements: response time p95 < 1s for SBOMs with up to 2000 packages each. The service layer (Task 1) handles performance; the endpoint layer just wires things together.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for handler function pattern (query extraction, service delegation, JSON response)
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for single-entity endpoint pattern with path parameter validation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration to follow for adding the new route
- `common/src/error.rs::AppError` — error response handling
- `tests/api/sbom.rs` — existing integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON when both IDs are valid
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response body matches the `SbomComparison` struct shape with all six diff categories
- [ ] Endpoint is registered and accessible via the SBOM route group

## Test Requirements
- [ ] Integration test: valid comparison returns 200 and correct diff structure
- [ ] Integration test: missing `left` param returns 400
- [ ] Integration test: missing `right` param returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparing identical SBOMs returns 200 with empty diff arrays
- [ ] Integration test: response includes correct `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, and `license_changes` for a known test dataset

## Verification Commands
- `cargo test --test api sbom::compare` — all comparison endpoint integration tests pass

## Documentation Updates
- `README.md` — Add the comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and diff service
