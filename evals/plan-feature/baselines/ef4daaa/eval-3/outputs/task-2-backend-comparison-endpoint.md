# Task 2 — Backend comparison endpoint and route registration

## Repository
trustify-backend

## Description
Add the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service method as a REST API. This endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff as JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` as JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `list.rs` and `get.rs` for handler function structure.
- The handler should:
  1. Extract `left` and `right` query parameters (both required UUIDs/IDs)
  2. Validate that both parameters are present; return 400 Bad Request if either is missing
  3. Call `SbomService::compare(left, right)` from the service layer (added in Task 1)
  4. Return the `SbomComparisonResult` as JSON with status 200
  5. Return 404 if either SBOM ID is not found (propagated from service error)
- Use `Result<Json<SbomComparisonResult>, AppError>` as the return type, consistent with other handlers.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. Use `.route("/compare", get(compare))` pattern.
- Ensure the `/compare` route is registered before `/{id}` to avoid path conflicts with the parameterized route.
- Response content type is `application/json`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function structure, query parameter extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter handling and `PaginatedResults` pattern (though comparison does not paginate)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for handler responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Response matches the expected JSON shape from the Figma design context

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct JSON structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom::compare` — all comparison endpoint tests pass
- `cargo clippy -- -D warnings` — no linting warnings

## Documentation Updates
- `README.md` — add comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Backend comparison model and service
