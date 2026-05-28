# Task 4 — Add SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Wire the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint into the Axum router. This endpoint accepts two SBOM IDs as query parameters, delegates to the comparison service, and returns the structured diff as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint; parses `left` and `right` query parameters, calls `SbomCompareService::compare`, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route under the existing `/api/v2/sbom` route group
- `server/src/main.rs` — No changes expected (SBOM routes are already mounted), but verify the SBOM module routes are mounted

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a JSON `SbomComparison` response with `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — handler functions take Axum extractors (query params, state), return `Result<Json<T>, AppError>`.
- Define a query parameter struct (e.g., `CompareParams`) with `left: String` and `right: String` fields, using Axum's `Query` extractor.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes — use `.route("/compare", get(compare))` pattern consistent with how `list.rs` and `get.rs` are registered.
- Return `Json(comparison_result)` on success.
- Error handling: the service already returns `AppError` for not-found cases; let it propagate through the `?` operator for automatic HTTP error response per the `IntoResponse` impl in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling endpoint handler demonstrating Axum extractor pattern and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — sibling endpoint demonstrating query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type with `IntoResponse` implementation for HTTP error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with JSON `SbomComparison` body
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Route is registered under the existing `/api/v2/sbom` route group
- [ ] Response Content-Type is `application/json`

## Test Requirements
- [ ] Integration test in `tests/api/sbom.rs`: successful comparison returns 200 with correct JSON shape
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify response contains all six diff category fields

## Dependencies
- Depends on: Task 3 — Add SBOM comparison service logic
