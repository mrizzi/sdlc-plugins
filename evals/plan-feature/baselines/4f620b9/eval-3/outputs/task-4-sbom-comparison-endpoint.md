## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff result. Register the new route alongside existing SBOM endpoints. Add integration tests covering the endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route in the SBOM router

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for GET /api/v2/sbom/compare

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Accepts two SBOM UUIDs as query parameters, returns `SbomComparisonResult` JSON

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` — use Axum extractors for query parameters.
- Define a `CompareQuery` struct with `left: Uuid` and `right: Uuid` fields, derive `Deserialize` for Axum query extraction.
- The handler should call `SbomService::compare(left, right, &db)` and return the result as JSON.
- Return `AppError` on failure — follow the `.context()` error wrapping pattern from `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes — add `.route("/compare", get(compare))`.
- Integration tests go in `tests/api/sbom.rs` following the existing test patterns in that file.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list endpoint as template for handler structure
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing get endpoint as template for single-entity retrieval pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — standard error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Returns 400 if either `left` or `right` query parameter is missing
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Route is registered in the SBOM endpoint module
- [ ] Integration tests pass

## Test Requirements
- [ ] Integration test: compare two valid SBOMs — verify 200 response with expected diff structure
- [ ] Integration test: missing query parameter — verify 400 response
- [ ] Integration test: non-existent SBOM ID — verify 404 response
- [ ] Integration test: compare identical SBOMs — verify empty diff categories

## Verification Commands
- `cargo test --test api -- sbom::compare` — run comparison endpoint integration tests

## Documentation Updates
- `README.md` — Add the new comparison endpoint to the API endpoint listing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Implement SBOM comparison service logic

[sdlc-workflow] Description digest: sha256-md:5b4fcfca4d9926426d78867717ff6f6aa9ec69f138290cddd1bab3202deb3f13
