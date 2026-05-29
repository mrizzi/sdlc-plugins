# Task 4 — Add SBOM comparison REST endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff as JSON. This endpoint is consumed by the frontend comparison page.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for the comparison endpoint with query parameter extraction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM ID query parameters, returns `SbomComparisonResult` JSON. Returns 404 if either SBOM ID is not found, 400 if parameters are missing.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function signature, Axum extractor usage, and error response handling.
- Use Axum `Query` extractor for the `left` and `right` query parameters. Define a `CompareQuery` struct with `left: String` and `right: String` fields.
- The handler should call the comparison service from Task 3 and return the `SbomComparisonResult` as JSON via `axum::Json`.
- Return `Result<Json<SbomComparisonResult>, AppError>` following the established error handling pattern.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. The route should be `.route("/compare", get(compare::handler))` or similar, matching the existing registration pattern.
- Consider adding `tower-http` caching headers to the response since comparison results for the same pair of SBOMs are deterministic. Follow the caching middleware pattern noted in the backend conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — endpoint handler pattern with Axum extractors and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — list endpoint pattern, useful for query parameter extraction style
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparisonResult` JSON body
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON field names match the expected shape (snake_case: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)
- [ ] Endpoint is registered and accessible under the `/api/v2/sbom` route prefix

## Test Requirements
- [ ] Integration test: call endpoint with two valid SBOM IDs, verify 200 response with correct diff structure
- [ ] Integration test: call endpoint with missing query parameters, verify 400 response
- [ ] Integration test: call endpoint with non-existent SBOM ID, verify 404 response
- [ ] Integration test: verify response JSON shape matches `SbomComparisonResult` serialization

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison diff service logic

[sdlc-workflow] Description digest: sha256:de5aeaff38298ff78ba1f7cc7a5b8eed9d02f4fccb25590e903efa7054932e87
