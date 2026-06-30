## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}` and register it in the SBOM route module. This endpoint extracts the `left` and `right` query parameters, calls the comparison service, and returns the structured diff result as JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route alongside existing `/` and `/{id}` routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM UUIDs as query parameters, returns `SbomComparisonResult` JSON

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure, extraction, and error handling.
- Define a `CompareQuery` struct with `left: Uuid` and `right: Uuid` fields, using Axum's `Query<CompareQuery>` extractor.
- The handler should validate that `left` and `right` are both present and are valid UUIDs (Axum's extractor handles this automatically with a 400 response for malformed UUIDs).
- Add validation that `left != right` — return a 400 Bad Request if both IDs are the same.
- Call `SbomService::compare(left, right)` and return the result as JSON.
- Return appropriate HTTP status codes: 200 for success, 400 for invalid parameters, 404 if either SBOM is not found.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` as `.route("/compare", get(compare::handler))` — ensure it is registered BEFORE the `/{id}` route to avoid path conflicts.
- All handlers must return `Result<Json<SbomComparisonResult>, AppError>` per the project's error handling convention.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler structure (extract ID, call service, return JSON)
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction patterns
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type for handler return

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct diff JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 400 when `left` or `right` is not a valid UUID
- [ ] Returns 400 when `left` and `right` are the same ID
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoint module

## Test Requirements
- [ ] Integration test: call comparison endpoint with two valid SBOM IDs and verify 200 response with expected diff structure
- [ ] Integration test: call with missing query parameters and verify 400 response
- [ ] Integration test: call with non-existent SBOM ID and verify 404 response
- [ ] Integration test: call with identical left and right IDs and verify 400 response
- [ ] Follow the existing test patterns in `tests/api/sbom.rs`

## Verification Commands
- `cargo test --test api sbom::compare` — run comparison endpoint integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 2 — Backend comparison response model
- Depends on: Task 3 — Backend comparison service logic
