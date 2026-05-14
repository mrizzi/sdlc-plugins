## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured comparison diff. This endpoint connects the comparison service to the HTTP API layer, making the diff computation available to the frontend.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` with `left` and `right` query parameters

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the compare route alongside existing SBOM routes
- `server/src/main.rs` — Ensure the SBOM module routes (including the new compare route) are mounted (likely already handled by existing SBOM route registration)

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns `SbomComparisonResult` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Define a query params struct with `#[derive(Deserialize)]` for `left: String` and `right: String` parameters
  - Handler function signature: `async fn compare(Query(params): Query<CompareParams>, ...) -> Result<Json<SbomComparisonResult>, AppError>`
  - Return `Result<Json<T>, AppError>` pattern consistent with other endpoints
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the Axum router builder pattern — add `.route("/compare", get(compare::compare))` to the existing SBOM route group
- Call `compare_sboms()` from `modules/fundamental/src/sbom/service/compare.rs` to perform the diff computation
- Validate that both `left` and `right` parameters are provided — return 400 Bad Request if either is missing
- Return 404 if either SBOM ID does not exist (propagated from the service layer error)
- No caching middleware for this endpoint — comparisons are dynamic and depend on current data

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function signature, error handling, and JSON response pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter deserialization and route registration
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error handling with proper HTTP status codes

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 400 Bad Request when `left` or `right` parameter is missing
- [ ] Returns 404 Not Found when either SBOM ID does not exist
- [ ] Response JSON shape matches the contract defined in the Figma design context (snake_case field names, all six diff sections present)
- [ ] Route is registered under the existing `/api/v2/sbom` route group

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with expected diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparison of two identical SBOMs returns empty diff sections
- [ ] Add tests to `tests/api/sbom.rs` following the existing test pattern with `assert_eq!(resp.status(), StatusCode::OK)`

## Verification Commands
- `cargo test --test api -- sbom::compare` — run comparison endpoint integration tests
- `cargo check` — verify the project compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Implement SBOM comparison service
