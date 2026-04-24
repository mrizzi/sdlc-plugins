# Task 2 — Backend SBOM comparison endpoint

## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that accepts two SBOM IDs as query parameters and returns the structured comparison diff computed by the service layer. This endpoint wires up the comparison service from Task 1 to an HTTP handler and registers it within the existing SBOM route group.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` as JSON with fields `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. See `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for the handler function conventions (extractors, return types, error handling).
- The handler should extract `left` and `right` query parameters as UUIDs. Return 400 Bad Request if either is missing or not a valid UUID.
- Return 404 Not Found if either SBOM ID does not exist (propagate from the service layer's error).
- Call `SbomService::compare(left_id, right_id)` and serialize the result as JSON.
- Route registration: add the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs`. The route should be `GET /compare` within the `/api/v2/sbom` scope.
- Error handling: all handlers return `Result<T, AppError>`, consistent with `common/src/error.rs`. Use `.context()` wrapping for meaningful error messages.
- Integration tests in `tests/api/sbom_compare.rs` should follow the pattern in `tests/api/sbom.rs` — hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function structure, extractors, and error responses
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `common/src/error.rs::AppError` — existing error handling type
- `tests/api/sbom.rs` — reference for integration test conventions

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the `SbomComparisonResult` schema
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 400 when `left` or `right` is not a valid UUID
- [ ] Returns 404 when either SBOM ID does not exist in the database
- [ ] Response time p95 < 1s for SBOMs with up to 2000 packages each
- [ ] Route is registered at the correct path within the `/api/v2/sbom` scope

## Test Requirements
- [ ] Integration test: valid comparison of two existing SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing `left` query parameter returns 400
- [ ] Integration test: missing `right` query parameter returns 400
- [ ] Integration test: non-existent left SBOM ID returns 404
- [ ] Integration test: non-existent right SBOM ID returns 404
- [ ] Integration test: identical SBOM IDs returns 200 with empty diff arrays

## Dependencies
- Depends on: Task 1 — Backend SBOM comparison diff model and service
