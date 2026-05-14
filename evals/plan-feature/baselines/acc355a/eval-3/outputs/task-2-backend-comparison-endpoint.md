# Task 2 — Add SBOM comparison REST endpoint and integration tests

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured diff computed by `SbomService::compare`. Also add integration tests that exercise the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that parses query parameters, calls `SbomService::compare`, and returns the JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router
- `server/src/main.rs` — No changes expected (SBOM module routes are already mounted), but verify the SBOM router is mounted
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as JSON. Response shape: `{ added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function conventions.
- The handler should:
  1. Extract `left` and `right` from query parameters (both required)
  2. Return 400 Bad Request if either parameter is missing
  3. Call `SbomService::compare(left, right)`
  4. Return 404 Not Found if either SBOM does not exist (propagate from service layer `AppError`)
  5. Return 200 OK with JSON-serialized `SbomComparisonResult`
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes. Use `.route("/compare", get(compare_handler))` pattern.
- For integration tests, follow the pattern established in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)` and asserting on the JSON response body structure.
- No caching headers are needed for comparison results (they are computed on-the-fly and depend on mutable data).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the handler pattern for extracting path/query params and calling service methods
- `modules/fundamental/src/sbom/endpoints/mod.rs` — follow the route registration pattern
- `common/src/error.rs::AppError` — reuse `IntoResponse` implementation for automatic error-to-HTTP mapping
- `tests/api/sbom.rs` — follow the existing integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid JSON diff
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape with all six diff sections
- [ ] Endpoint is registered under the existing `/api/v2/sbom` router

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences returns correct diff
- [ ] Integration test: compare identical SBOMs returns empty diff sections
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON deserializes to `SbomComparisonResult` correctly

## Dependencies
- Depends on: Task 1 — Add SBOM comparison diff model and service logic
