## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured comparison result. This endpoint is the API surface for the frontend comparison UI and delegates to the comparison service logic from Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new compare route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns structured diff between two SBOMs as `SbomComparison` JSON

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs`.

The handler function should:
1. Extract `left` and `right` query parameters (both required UUIDs)
2. Validate that both parameters are present — return 400 Bad Request if missing
3. Call `SbomService::compare(left, right)` from Task 3
4. Return the `SbomComparison` result as JSON with 200 OK
5. Return 404 if either SBOM ID does not exist
6. Use `Result<Json<SbomComparison>, AppError>` as the return type, consistent with other endpoints

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (e.g., how `list.rs` and `get.rs` are registered). The route should be mounted at `/api/v2/sbom/compare`.

All handlers in this project return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler demonstrating the project's endpoint pattern (query extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/list.rs` — endpoint showing route registration and PaginatedResults usage
- `common/src/error.rs::AppError` — error type with IntoResponse impl for automatic HTTP status mapping

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query parameters are missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Response JSON shape matches the contract defined in Task 2

## Test Requirements
- [ ] Integration test: call compare endpoint with two valid SBOM IDs — verify 200 response with correct diff structure
- [ ] Integration test: call compare endpoint with missing query parameters — verify 400 response
- [ ] Integration test: call compare endpoint with non-existent SBOM IDs — verify 404 response
- [ ] Integration test: call compare endpoint with identical SBOM IDs — verify empty diff categories

## Verification Commands
- `cargo test --test api -- sbom_compare` — run comparison endpoint integration tests

## Documentation Updates
- `README.md` — add the new comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 3 — Add SBOM comparison service logic
