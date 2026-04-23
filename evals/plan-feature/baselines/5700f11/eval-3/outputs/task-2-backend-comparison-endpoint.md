## Repository
trustify-backend

## Description
Create the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service via the REST API. This endpoint accepts two SBOM IDs as query parameters and returns the structured diff computed by the comparison service from Task 1.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route in the SBOM endpoint router alongside the existing list and get routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that extracts query parameters, calls the comparison service, and returns the JSON response

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs including added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — handlers are async functions that accept Axum extractors and return `Result<Json<T>, AppError>`.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, extracted via Axum's `Query` extractor, following the same pattern used in `common/src/db/query.rs` for query parameter handling.
- The handler should call `SbomService::compare(left_id, right_id, &db)` from the service created in Task 1 and return the `SbomComparison` as `Json<SbomComparison>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the same `.route()` pattern as the existing `list.rs` and `get.rs` routes. The compare route should be registered before the `/{id}` route to avoid path conflicts.
- Return `AppError` (from `common/src/error.rs`) with a 400 status if either `left` or `right` query parameter is missing, and 404 if either SBOM ID is not found.
- Add `#[utoipa::path(...)]` annotation for OpenAPI documentation, following the pattern in existing endpoint files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for single-resource endpoint handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error response type
- `modules/fundamental/src/sbom/service/compare.rs::SbomService::compare` — The service method created in Task 1

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the `SbomComparison` schema
- [ ] Returns 400 if either `left` or `right` query parameter is missing
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] The response JSON has the correct shape: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] The endpoint is registered at the correct path under `/api/v2/sbom/compare`
- [ ] p95 response time is under 1 second for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: successful comparison of two valid SBOMs returns 200 with expected diff structure
- [ ] Integration test: missing `left` query parameter returns 400
- [ ] Integration test: missing `right` query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: same SBOM ID for both `left` and `right` returns 200 with empty diff sections

## Verification Commands
- `cargo test --test api sbom_compare` — All integration tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>"` — Returns 200 with structured diff JSON

## Dependencies
- Depends on: Task 1 — Backend comparison model and service
