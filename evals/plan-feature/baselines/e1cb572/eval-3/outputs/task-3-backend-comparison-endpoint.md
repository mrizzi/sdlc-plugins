# Task 3: Implement SBOM comparison endpoint handler and route

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the HTTP endpoint handler for the SBOM comparison API and register it in the router. The endpoint accepts two SBOM IDs as query parameters, delegates to the comparison service from Task 2, and returns the structured diff as JSON. Integration tests verify the endpoint returns correct responses for valid comparisons, missing SBOMs, and malformed input.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler that extracts query parameters, calls `SbomComparisonService::compare()`, and returns the `SbomComparison` response
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route in the SBOM router alongside the existing list and get routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff between two SBOMs as JSON. Query parameters `left` and `right` are required SBOM IDs. Returns 200 with `SbomComparison` body on success, 404 if either SBOM not found, 400 if parameters missing.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler signature and error handling.
- The handler should extract `left` and `right` query parameters using Axum's `Query` extractor. Return `AppError::BadRequest` if either parameter is missing.
- The handler returns `Result<Json<SbomComparison>, AppError>`, consistent with other endpoints in this module.
- Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should follow the existing pattern of chaining `.route()` calls on the router builder.
- Integration tests should follow the pattern in `tests/api/sbom.rs`:
  1. Set up test database with two SBOMs containing known package and advisory differences.
  2. Call `GET /api/v2/sbom/compare?left={id1}&right={id2}` and assert response status is `200 OK`.
  3. Deserialize the response body and verify diff counts match expected values.
  4. Test error cases: missing SBOM ID returns `404`, missing query parameter returns `400`.
- All errors should use `Result<T, AppError>` with `.context()` wrapping, consistent with `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — endpoint handler pattern (Axum handler, error handling, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `modules/fundamental/src/sbom/service/compare.rs::SbomComparisonService` — the service layer created in Task 2
- `common/src/error.rs::AppError` — error variants for 400/404 responses
- `tests/api/sbom.rs` — integration test structure and fixture setup pattern

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200 OK` with the comparison JSON
- [ ] Missing query parameter (`left` or `right`) returns `400 Bad Request`
- [ ] Non-existent SBOM ID returns `404 Not Found`
- [ ] Route is registered in the SBOM endpoint module and accessible from the server
- [ ] Response content type is `application/json`

## Test Requirements
- [ ] Integration test: valid comparison request returns `200` with correct diff structure
- [ ] Integration test: missing `left` query parameter returns `400`
- [ ] Integration test: missing `right` query parameter returns `400`
- [ ] Integration test: non-existent SBOM ID returns `404`
- [ ] Integration test: identical SBOM IDs returns `200` with empty diff arrays

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Implement SBOM comparison model and service layer

`[sdlc-workflow] Description digest: sha256-md:c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5`
