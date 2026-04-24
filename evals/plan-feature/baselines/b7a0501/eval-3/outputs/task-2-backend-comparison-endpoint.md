## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare?left={id}&right={id}` HTTP endpoint that exposes the SBOM comparison service (created in Task 1) via the REST API. The endpoint accepts two SBOM IDs as query parameters, delegates to `SbomService::compare()`, and returns the structured diff as JSON. This endpoint enables the frontend comparison UI and provides a shareable, URL-encodable comparison.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing SBOM routes (GET list, GET by ID)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Endpoint handler for `GET /api/v2/sbom/compare` that extracts `left` and `right` query parameters and calls `SbomService::compare()`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as `SbomComparison` JSON response. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if either parameter is missing, 404 if either SBOM is not found.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — the handler is an async function that extracts parameters, calls the service, and returns `Result<Json<T>, AppError>`.
- Use Axum's `Query` extractor to parse `left` and `right` as query parameters. Define a `CompareQuery` struct with `left: String` and `right: String` fields.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` using the `.route("/compare", get(compare))` pattern, consistent with how `list` and `get` routes are registered.
- Return `AppError` with appropriate HTTP status codes: 400 for missing parameters, 404 for non-existent SBOMs (propagated from the service layer).
- Use `utoipa` annotations on the handler for OpenAPI documentation generation, consistent with existing endpoint handlers.
- The route must be registered before the `/{id}` route to avoid path conflicts where `compare` is interpreted as an SBOM ID.
- Per the non-functional requirement, the endpoint must achieve p95 < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for handler structure, error handling, and response pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for handler with query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error type for response error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON when both SBOMs exist
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON shape matches the contract defined in the feature spec (six diff section arrays)
- [ ] Route is registered in the SBOM endpoint module without breaking existing routes
- [ ] Endpoint is documented with `utoipa` annotations for OpenAPI spec

## Test Requirements
- [ ] Integration test: successful comparison returns 200 with correct response shape
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: existing SBOM list and detail endpoints still work after route registration

## Dependencies
- Depends on: Task 1 — Backend comparison model and service
