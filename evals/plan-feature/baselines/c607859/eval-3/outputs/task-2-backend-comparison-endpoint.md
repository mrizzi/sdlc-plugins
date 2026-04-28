# Task 2 -- Backend Comparison Endpoint

## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured diff as `SbomComparisonResult`. This endpoint provides the backend API that the frontend comparison view will consume.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the `/compare` route and add `pub mod compare;`
- `server/src/main.rs` -- no changes expected (SBOM routes are already mounted), but verify

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns SbomComparisonResult JSON with all six diff categories

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure and route registration.
- The endpoint handler should extract `left` and `right` from query parameters, validate both are present, and call `SbomService::compare(left, right)`.
- Return 400 Bad Request if either query parameter is missing.
- Return 404 Not Found if either SBOM ID does not exist (propagated from the service layer).
- The endpoint should be registered in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. Follow the route registration pattern used for `list.rs` and `get.rs`.
- Response content type is `application/json`. The SbomComparisonResult struct derives Serialize so Axum's Json extractor handles serialization.
- Per the non-functional requirements, response time must be p95 < 1s for SBOMs with up to 2000 packages. The service layer handles performance; no caching is needed at the endpoint layer for MVP.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- reference for single-SBOM handler pattern with path parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for handler with query parameters
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow
- `common/src/error.rs::AppError` -- error handling pattern for endpoint handlers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Missing query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response JSON matches the shape specified in the feature requirements (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Endpoint is registered under the existing `/api/v2/sbom` route prefix

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with expected diff structure
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 1 -- Backend Comparison Model and Service
