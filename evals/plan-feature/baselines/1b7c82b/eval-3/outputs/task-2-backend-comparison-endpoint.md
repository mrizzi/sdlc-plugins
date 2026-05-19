## Repository
trustify-backend

## Target Branch
main

## Description
Expose the SBOM comparison service as an HTTP endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This task adds the Axum handler, registers the route, and provides integration tests that hit the real database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Axum handler for the comparison endpoint
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `GET /compare` route under the existing `/api/v2/sbom` router
- `tests/api/mod.rs` -- Add `mod sbom_compare;` if a mod file exists, or ensure the new test is discovered

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Returns a JSON `SbomComparison` response with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: extract query params, call the service method, return JSON.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, extracting via Axum's `Query<CompareQuery>`.
- Call `SbomService::compare(left, right)` (implemented in Task 1) and return the `SbomComparison` as JSON.
- Return `400 Bad Request` if either query param is missing; return `404 Not Found` if either SBOM ID does not exist (propagated from the service layer's `AppError`).
- In `modules/fundamental/src/sbom/endpoints/mod.rs`, add the new route alongside the existing list and get routes. Follow the existing `.route()` pattern used for `/api/v2/sbom` and `/api/v2/sbom/{id}`.
- For integration tests, follow the patterns in `tests/api/sbom.rs`: set up test data (ingest two SBOMs with known packages), call the endpoint, and assert on the response body structure.
- Ensure the endpoint meets the p95 < 1s performance requirement for SBOMs with up to 2000 packages.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Pattern for Axum handler extracting path/query params and returning JSON
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern to follow
- `common/src/error.rs::AppError` -- Implements `IntoResponse` for automatic error-to-HTTP-status mapping
- `tests/api/sbom.rs` -- Integration test patterns: database setup, HTTP assertions

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct JSON structure
- [ ] Missing query params return 400 Bad Request
- [ ] Nonexistent SBOM IDs return 404 Not Found
- [ ] Response JSON contains all six diff category fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Endpoint is registered under the `/api/v2/sbom` route namespace

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify response body
- [ ] Integration test: compare identical SBOMs and verify all diff arrays are empty
- [ ] Integration test: missing `left` query param returns 400
- [ ] Integration test: missing `right` query param returns 400
- [ ] Integration test: nonexistent left SBOM ID returns 404
- [ ] Integration test: nonexistent right SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom_compare` -- All integration tests pass
- `cargo check --workspace` -- No compilation errors across workspace

## Dependencies
- Depends on: Task 1 -- Backend comparison model and service
