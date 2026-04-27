# Task 2 — SBOM comparison REST endpoint

## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service logic from Task 1, and returns the structured diff as JSON. This endpoint follows the existing endpoint registration pattern and is mounted alongside the existing SBOM routes.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route in the SBOM router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as `SbomComparisonResult` JSON. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if either parameter is missing. Returns 404 if either SBOM does not exist. Returns 200 with the comparison result on success.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler function structure, error handling, and response type conventions.
- Route registration pattern: in `modules/fundamental/src/sbom/endpoints/mod.rs`, existing routes are registered using Axum's router builder. Add the `/compare` route at the same level as `/{id}` and the list route. Ensure `/compare` is registered before `/{id}` to avoid path conflicts (Axum matches routes in registration order).
- The handler function signature should accept query parameters via Axum's `Query<CompareParams>` extractor, where `CompareParams` is a struct with `left: String` and `right: String` fields.
- Call `SbomService::compare(left, right)` and return the result as JSON with `Json(result)`.
- Error handling: use `Result<Json<SbomComparisonResult>, AppError>` as the return type, consistent with `common/src/error.rs`.
- Validate that `left` and `right` are not the same ID — return a 400 Bad Request with a descriptive message if they are equal.
- Non-functional: the endpoint should not add any caching headers (diff is computed on-the-fly and may change as underlying data is updated).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference implementation for single-SBOM handler with path parameter extraction and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation for query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error enum for consistent error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the comparison JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Same ID for both `left` and `right` returns 400 with descriptive error message
- [ ] Response Content-Type is `application/json`
- [ ] Response shape matches the `SbomComparisonResult` contract from Task 1
- [ ] Endpoint is accessible at the correct path under the SBOM route prefix

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct diff structure
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: non-existent SBOM IDs return 404
- [ ] Integration test: identical left and right IDs return 400

## Verification Commands
- `cargo build -p trustify-server` — must compile without errors
- `cargo test -p trustify-tests` — integration tests pass

## Dependencies
- Depends on: Task 1 — SBOM comparison diff model and service logic
