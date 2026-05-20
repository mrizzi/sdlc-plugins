# Task 4 — Add SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Wire the `GET /api/v2/sbom/compare?left={id1}&right={id2}` HTTP endpoint that calls the comparison service method and returns the structured diff as JSON. Register the route in the existing SBOM endpoint module.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON. Query parameters `left` and `right` are required SBOM UUIDs. Returns 400 if either parameter is missing, 404 if either SBOM does not exist.

## Implementation Notes
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Use Axum extractors for query parameters
  - Return `Result<Json<SbomComparisonResult>, AppError>` 
  - Use `.context()` error wrapping
- Define a query parameter struct (e.g., `CompareParams`) with `left: Uuid` and `right: Uuid` fields, deriving `Deserialize` and Axum's query extractor traits
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern for `list.rs` and `get.rs` route registration
- The endpoint is a GET since it is a read-only comparison operation with no side effects
- Consider adding `tower-http` caching headers since comparison results are deterministic for the same inputs

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow its handler pattern for parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — follow its route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route mounting logic to extend
- `common/src/error.rs::AppError` — use existing error type for 400/404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 if `left` or `right` query parameter is missing
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoint module
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Integration test: successful comparison returns 200 with expected JSON structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify response JSON shape matches `SbomComparisonResult` schema

## Verification Commands
- `cargo test --package trustify-tests -- api::sbom::compare` — all comparison endpoint tests pass

## Dependencies
- Depends on: Task 3 — Add SBOM comparison service logic
