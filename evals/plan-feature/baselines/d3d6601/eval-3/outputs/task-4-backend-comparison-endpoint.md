## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service, and returns the structured diff response. Register the route in the SBOM module's endpoint configuration and add integration tests covering the comparison workflow.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler function for `GET /api/v2/sbom/compare`
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route and add `pub mod compare;`
- `tests/api/mod.rs` — add `mod sbom_compare;` (if test module registration is needed)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparison` JSON response

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` — use Axum extractors for query parameters and return `Result<Json<SbomComparison>, AppError>`.
- Define a query parameter struct with `#[derive(Deserialize)]`: `CompareQuery { left: String, right: String }` and extract it via `Query<CompareQuery>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern (e.g., `.route("/compare", get(compare::handler))`).
- Ensure the `/compare` route is registered before the `/{id}` route to prevent path parameter collision.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test database with two SBOMs containing different packages, call the compare endpoint, and assert the response contains the expected diff sections.
- Test cases to cover: successful comparison, missing left SBOM (404), missing right SBOM (404), identical SBOMs (all diff sections empty).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — follow the same handler function pattern and error handling
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for route registration in mod.rs
- `tests/api/sbom.rs` — follow integration test setup pattern (test database, seed data, HTTP assertions)
- `common/src/error.rs::AppError` — error type for handler return

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Route is registered in the SBOM endpoints module
- [ ] Integration tests pass against test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify response JSON contains correct added, removed, changed packages
- [ ] Integration test: compare with non-existent left SBOM — verify 404 response
- [ ] Integration test: compare with non-existent right SBOM — verify 404 response
- [ ] Integration test: compare identical SBOMs — verify all diff sections are empty arrays
- [ ] Integration test: compare with missing query parameters — verify 400 response

## Verification Commands
- `cargo test -p trustify-tests -- api::sbom_compare` — run comparison endpoint integration tests
- `cargo clippy -p trustify-fundamental` — verify no linting warnings

## Documentation Updates
- `README.md` — add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service with diff logic

[sdlc-workflow] Description digest: sha256:ee76d8f0c19fff8ec2d3e621c996a2b95cff23e8a8047e99e193d9778bff5c36
