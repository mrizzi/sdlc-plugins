## Repository
trustify-backend

## Description
Expose the SBOM comparison logic as a REST endpoint at `GET /api/v2/sbom/compare?left={id}&right={id}`. This wires the comparison service into an Axum handler, registers the route, and adds integration tests that exercise the full HTTP path. After this task, the frontend can call the comparison API.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Axum handler for `GET /api/v2/sbom/compare` that extracts `left` and `right` query parameters, calls the comparison service, and returns the `SbomComparison` as JSON
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/compare` route in the SBOM router
- `server/src/main.rs` -- No changes expected if SBOM routes are already mounted (verify)

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` -- NEW: Returns JSON `SbomComparison` with six diff categories. Returns 400 if either query param is missing. Returns 404 if either SBOM ID does not exist.

## Implementation Notes
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Define an Axum handler function with signature like `async fn compare(Query(params): Query<CompareParams>, State(service): State<...>) -> Result<Json<SbomComparison>, AppError>`
  - Define a `CompareParams` struct with `left: String` and `right: String` fields, deriving `Deserialize`
  - Return `Json(comparison)` on success
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing routes. Use `.route("/compare", get(compare))` before the `/{id}` route to avoid path conflicts.
- Error handling:
  - If `left` or `right` query param is missing, Axum's `Query` extractor returns 400 automatically
  - If an SBOM is not found, the comparison service should return an error that maps to 404 via `AppError`
- For OpenAPI documentation, annotate the handler with `#[utoipa::path(...)]` following the pattern in existing endpoint files.
- Integration tests should follow the pattern in `tests/api/sbom.rs`:
  - Set up test database with two SBOMs containing known packages and advisories
  - Call `GET /api/v2/sbom/compare?left={id1}&right={id2}` and assert response status is 200
  - Deserialize response body and verify diff categories contain expected entries
  - Test error cases: missing params (400), non-existent SBOM (404)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Handler pattern, Axum state extraction, error mapping
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern
- `tests/api/sbom.rs` -- Integration test setup, test database helpers, assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Response JSON shape matches the contract: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Route is registered and does not conflict with existing `GET /api/v2/sbom/{id}`
- [ ] Endpoint is documented with `#[utoipa::path]` for OpenAPI generation

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify all six diff categories in the response
- [ ] Integration test: compare identical SBOMs and verify all diff categories are empty arrays
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test -p trustify-integration sbom_compare` -- should pass all integration tests
- `cargo build` -- full project builds successfully

## Dependencies
- Depends on: Task 2 -- Implement SBOM comparison service logic
