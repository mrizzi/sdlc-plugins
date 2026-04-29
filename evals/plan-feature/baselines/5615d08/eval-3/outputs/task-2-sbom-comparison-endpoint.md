## Repository
trustify-backend

## Description
Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This registers the new route in the SBOM endpoint module and wires it to the comparison service method created in Task 1. The endpoint validates the query parameters, invokes the diff computation, and returns the structured JSON response.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` that extracts `left` and `right` query parameters, calls `SbomService::compare()`, and returns the `SbomComparison` as JSON

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Add `pub mod compare;` and register the `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as JSON with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract dependencies from Axum state, parse parameters, call service, return response.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, derived with `Deserialize`, and extract it using Axum's `Query<CompareQuery>` extractor.
- Return `Result<Json<SbomComparison>, AppError>` following the error handling pattern in `common/src/error.rs`. Return a 400 Bad Request if either parameter is missing or invalid; return 404 if either SBOM ID does not exist.
- In `modules/fundamental/src/sbom/endpoints/mod.rs`, look at how existing routes are registered (e.g., the `list.rs` and `get.rs` routes). Add `.route("/compare", get(compare::handler))` to the SBOM router.
- The endpoint does not use `PaginatedResults` from `common/src/model/paginated.rs` because the comparison result is a single structured object, not a list.
- Consider adding cache-control headers for short-lived caching (e.g., 60 seconds) using the `tower-http` caching middleware pattern already in use in the server.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the same handler pattern (state extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Extend the existing route registration
- `common/src/error.rs::AppError` — Reuse for error responses (400, 404)
- `modules/fundamental/src/sbom/service/compare.rs::SbomService::compare()` — The service method from Task 1

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the correct JSON structure
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request with a descriptive error message
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response Content-Type is `application/json`
- [ ] Endpoint is registered and accessible in the Axum router

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with expected diff structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON deserializes to `SbomComparison` struct

## Verification Commands
- `cargo test -p trustify-tests -- api::sbom::compare` — All comparison endpoint integration tests pass

## Dependencies
- Depends on: Task 1 — SBOM comparison model and service
