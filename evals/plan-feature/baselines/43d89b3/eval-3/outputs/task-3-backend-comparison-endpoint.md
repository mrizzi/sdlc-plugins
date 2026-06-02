## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured diff using the comparison service method created in Task 2. Register the new endpoint in the SBOM module's route configuration and add integration tests.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for GET /api/v2/sbom/compare that parses query params, calls SbomService::compare_sboms, and returns the SbomComparisonResult as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod compare;` and register the `/compare` route in the SBOM router
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff between two SBOMs as SbomComparisonResult JSON

## Implementation Notes
Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function structure:
- Use Axum extractors for query parameters (`Query<CompareParams>`)
- Return `Result<Json<SbomComparisonResult>, AppError>`
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes

Define a `CompareParams` struct with `left: String` and `right: String` fields, deriving `Deserialize`.

Error handling:
- Return 400 Bad Request if either `left` or `right` parameter is missing
- Return 404 Not Found if either SBOM ID does not exist
- Use `.context()` wrapping per the pattern in `common/src/error.rs`

For integration tests, follow the test pattern in `tests/api/sbom.rs` which uses `assert_eq!(resp.status(), StatusCode::OK)`. Test against a real PostgreSQL test database per the established convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing GET handler; follow the same Axum extractor and response pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Existing list handler; reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration file; add the new compare route here
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON body
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response JSON matches the expected shape with all six diff category fields
- [ ] Endpoint is registered under the `/api/v2/sbom` route group
- [ ] p95 response time < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: call compare endpoint with two valid SBOM IDs that have known differences — verify response contains correct added/removed packages
- [ ] Integration test: call compare endpoint with missing query parameters — verify 400 response
- [ ] Integration test: call compare endpoint with non-existent SBOM ID — verify 404 response
- [ ] Integration test: call compare endpoint with identical SBOMs — verify all diff categories are empty arrays

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
