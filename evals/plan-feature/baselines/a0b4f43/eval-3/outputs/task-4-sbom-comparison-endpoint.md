## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured diff as JSON. Register the new route in the SBOM endpoint module and add integration tests that verify the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for GET /api/v2/sbom/compare; extracts left/right query params, calls SbomComparisonService, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router; add `pub mod compare;`
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a JSON object with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `get.rs` for handler function structure, error handling, and response serialization.
- The handler should extract query parameters using Axum's `Query<CompareParams>` extractor where `CompareParams` has `left: String` and `right: String` fields.
- Return `Result<Json<SbomComparisonResult>, AppError>` following the standard error handling pattern.
- Register the route in `endpoints/mod.rs` alongside existing routes (list, get). Use `.route("/compare", get(compare::handler))` or similar pattern matching the existing route registration style.
- Integration tests in `tests/api/sbom.rs` should follow the existing test pattern: set up test data, make HTTP requests, assert on status codes and response bodies. Use `assert_eq!(resp.status(), StatusCode::OK)` as per conventions.
- Test edge cases: invalid SBOM IDs (expect 404), missing query params (expect 400), same ID for both left and right (expect empty diff or valid response).
- The endpoint must return responses within p95 < 1s for SBOMs with up to 2000 packages each (non-functional requirement).
- Validate that both `left` and `right` parameters are provided; return a 400 Bad Request with a descriptive error message if either is missing.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing endpoint handler; follow its pattern for extracting path/query params, calling service, and returning JSON
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern; follow existing `.route()` calls for adding the new compare route
- `common/src/error.rs::AppError` — Standard error type; use for all error returns
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the SbomComparisonResult structure
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Route is registered and accessible at `/api/v2/sbom/compare`
- [ ] Integration tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify the response contains correct added/removed packages, version changes, vulnerabilities, and license changes
- [ ] Integration test: request with missing query parameters returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns an empty diff (all arrays empty)

## Verification Commands
- `cargo test --test api sbom::compare` — All comparison endpoint integration tests pass

## Documentation Updates
- `README.md` — Add the new comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)
- Depends on: Task 3 — Add SBOM comparison model and service (trustify-backend)