# Task 4 — Add SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that returns the structured diff between two SBOMs. This endpoint calls the comparison service method and returns the result as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route alongside existing `/api/v2/sbom` routes
- `server/src/main.rs` — Verify the sbom module routes are mounted (likely already done, but confirm)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as JSON. Query params `left` and `right` are required SBOM IDs. Response body is `SbomComparisonResult`.

## Implementation Notes
- Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Extract query parameters using Axum's `Query` extractor.
  - Call the service method and return the result.
  - Return `Result<Json<SbomComparisonResult>, AppError>`.
- Define a `CompareQuery` struct with `left` and `right` fields (both required SBOM IDs) for the query parameter extraction.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. The existing pattern uses a function that returns a `Router` — add `.route("/compare", get(compare_handler))` to the router chain.
- Return `AppError::NotFound` if either SBOM ID does not exist (propagated from the service layer).
- Return `AppError::BadRequest` if `left` or `right` query params are missing.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler pattern to follow for parameter extraction and response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error handling for bad requests and not found

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response JSON field names are snake_case matching the model definition
- [ ] Endpoint is accessible at the registered route path

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing query params return 400
- [ ] Integration test: invalid SBOM ID returns 404
- [ ] Integration test: verify response JSON matches expected `SbomComparisonResult` shape

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison endpoint tests pass

## Documentation Updates
- `README.md` — Add the comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison diff service logic
