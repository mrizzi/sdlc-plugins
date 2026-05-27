## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured comparison result from `SbomService::compare`. This endpoint enables the frontend comparison page to fetch diff data between two SBOM versions.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare` with query parameter extraction and response serialization

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing `/api/v2/sbom` routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the existing endpoint pattern in the `sbom/endpoints/` directory:
- The handler file structure mirrors `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. Create `compare.rs` with an async handler function.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `Deserialize`, to extract query parameters via Axum's `Query` extractor.
- The handler should call `SbomService::compare(left, right)` (implemented in Task 3) and return `Json(result)`.
- Return type: `Result<Json<SbomComparisonResult>, AppError>` matching the error handling pattern in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (e.g., `.route("/compare", get(compare::handler))`). Ensure the `/compare` route is registered before the `/{id}` route to avoid path conflicts.
- The endpoint path must be exactly `/api/v2/sbom/compare` to match the frontend API contract.
- Route mounting follows `server/src/main.rs` patterns — the sbom module's routes are already mounted, so only `endpoints/mod.rs` needs updating.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler showing the handler function signature, error handling, and response pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for handler return values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing or invalid `left`/`right` query parameters return 400 Bad Request
- [ ] Non-existent SBOM IDs return 404 Not Found
- [ ] Response JSON shape matches the contract specified in the feature requirements
- [ ] Endpoint is accessible under the existing `/api/v2/sbom` route prefix

## Test Requirements
- [ ] Integration test: call `GET /api/v2/sbom/compare?left={id1}&right={id2}` with valid IDs and verify 200 response with correct diff structure
- [ ] Integration test: call with missing `left` parameter and verify 400 response
- [ ] Integration test: call with non-existent SBOM ID and verify 404 response
- [ ] Integration test: verify response time is under 1s for SBOMs with representative package counts

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)
- Depends on: Task 3 — Add SBOM comparison diff model and service

[sdlc-workflow] Description digest: sha256:c6cf5efe9551661abdc1d6a8aa47891bf1fba0bf5ec94b154c312684be755492
