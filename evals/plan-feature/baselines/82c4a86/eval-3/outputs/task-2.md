# Task 2 — Add SBOM comparison REST endpoint

## Repository
trustify-backend

## Description
Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The endpoint calls `SbomService::compare` and returns the structured diff as JSON. This endpoint completes the backend API required by the frontend comparison UI.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for GET /api/v2/sbom/compare

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM ID query parameters, returns `SbomComparisonResult` as JSON

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. See `list.rs` and `get.rs` for the handler function structure: extract dependencies from Axum state, call the service, return `Result<Json<T>, AppError>`.
- Register the route in `endpoints/mod.rs` alongside existing SBOM routes. Use `.route("/api/v2/sbom/compare", get(compare))` — register this before the `/{id}` route to avoid path conflicts.
- Extract `left` and `right` as query parameters using Axum's `Query` extractor with a struct (e.g., `CompareQuery { left: Uuid, right: Uuid }`).
- Return 400 Bad Request if either parameter is missing or not a valid UUID.
- Return 404 if either SBOM ID does not exist (propagated from SbomService::compare).
- Per constraints (2.1-2.3): when implementing, commit with Conventional Commits format, reference TC-9003, and include Assisted-by trailer.
- Per constraints (3.1): branch should be named after the Jira issue ID.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler pattern to follow for Axum handler structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction and PaginatedResults usage
- `common/src/error.rs::AppError` — standard error handling, automatically converts to HTTP responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing or invalid `left`/`right` parameters return 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Response JSON shape matches: `{ added_packages: [...], removed_packages: [...], version_changes: [...], new_vulnerabilities: [...], resolved_vulnerabilities: [...], license_changes: [...] }`
- [ ] Endpoint is accessible at the documented path with no auth regressions

## Test Requirements
- [ ] Integration test: call compare endpoint with two valid SBOM IDs, verify 200 response with correct diff structure
- [ ] Integration test: call compare endpoint with missing `left` parameter, verify 400 response
- [ ] Integration test: call compare endpoint with non-existent SBOM ID, verify 404 response
- [ ] Integration test: call compare endpoint with identical SBOM IDs, verify 200 with empty diff lists

## Verification Commands
- `cargo test --package fundamental -- sbom::endpoints::test_compare` — endpoint integration tests pass
- `cargo test -p tests -- api::sbom` — existing SBOM endpoint tests still pass (no regression)

## Documentation Updates
- `README.md` — add the comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and diff service
