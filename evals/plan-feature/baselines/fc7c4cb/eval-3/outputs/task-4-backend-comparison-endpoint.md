## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service method, and returns the structured diff as JSON. This endpoint is consumed by the frontend comparison page.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for GET /api/v2/sbom/compare with left/right query parameters

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the compare route alongside existing /api/v2/sbom routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as `SbomComparisonResult` JSON. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if either parameter is missing, 404 if either SBOM does not exist.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — handlers are async functions that take Axum extractors and return `Result<Json<T>, AppError>`.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, using Axum's `Query` extractor to parse the query parameters.
- Call `SbomService::compare(left_id, right_id)` from the handler and return the result as `Json<SbomComparisonResult>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for route registration. The compare route should be registered before the `/{id}` route to avoid path conflicts (Axum matches routes in order).
- Return HTTP 400 (Bad Request) if either `left` or `right` parameter is missing or empty. Return HTTP 404 if the service returns a not-found error for either SBOM.
- Reference `common/src/error.rs::AppError` for error response mapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler function pattern, Axum extractor usage, and error handling for SBOM endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction and response wrapping pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — demonstrates route registration pattern for adding new routes

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Response JSON shape matches the contract: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Endpoint is registered and accessible at the correct path

## Test Requirements
- [ ] Integration test in `tests/api/sbom.rs`: call `GET /api/v2/sbom/compare?left={id1}&right={id2}` with valid IDs and verify 200 response with correct diff structure
- [ ] Integration test: call without `left` parameter and verify 400 response
- [ ] Integration test: call without `right` parameter and verify 400 response
- [ ] Integration test: call with non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify response Content-Type is application/json

## Documentation Updates
- `README.md` — Add the comparison endpoint to any API endpoint listing or reference section

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service method

[sdlc-workflow] Description digest: sha256:551daf929d7b6d55b16f52e7128c8c892aae27653b434613bb24f98521a9e3c5
