## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), calls the comparison service, and returns the structured diff as JSON. Add integration tests for the endpoint covering success, missing parameters, and invalid SBOM ID cases.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare` with query parameter extraction and response serialization
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint module
- `server/src/main.rs` — Ensure the SBOM module routes are mounted (already mounted, but verify compare route is included via module registration)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `list.rs` and `get.rs` for the established handler patterns. Handlers return `Result<Json<T>, AppError>` using the error handling from `common/src/error.rs`.

Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` where routes are added to the router. Add the `/compare` route alongside existing routes.

For query parameter extraction, use Axum's `Query` extractor. Define a `CompareQuery` struct with `left: String` and `right: String` fields.

Integration tests should follow the pattern in `tests/api/sbom.rs` — use a real PostgreSQL test database and assert on `resp.status()` with `StatusCode::OK`.

The endpoint response time must meet the p95 < 1s NFR for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for single-entity GET handler pattern with path parameter extraction
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for handler returning JSON with query parameters
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `tests/api/sbom.rs` — Integration test patterns using real PostgreSQL test database

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON body
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response JSON contains all six diff categories matching the expected response shape
- [ ] Endpoint is accessible at the registered route under `/api/v2/sbom/compare`

## Test Requirements
- [ ] Integration test: compare two valid SBOMs returns 200 with correct diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: compare two identical SBOMs returns 200 with empty diff arrays

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model and service

[sdlc-workflow] Description digest: sha256-md:40bc30537881472500ccbf508b443550f8cbd86052afcea7f5e86ad84617d8ec
