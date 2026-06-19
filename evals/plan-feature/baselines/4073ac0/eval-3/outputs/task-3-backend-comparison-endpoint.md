## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This task adds the HTTP handler, registers the route, and creates integration tests that exercise the full comparison flow against a test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` that parses `left` and `right` query params, calls `SbomCompareService::compare()`, and returns the JSON response
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs including added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract query params using Axum's `Query<T>` extractor, call the service, return `Json<SbomComparison>`.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `Deserialize`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern as `list.rs` and `get.rs` route registration.
- Return `400 Bad Request` if either `left` or `right` query param is missing.
- Return `404 Not Found` if either SBOM ID does not exist (propagated from `SbomCompareService`).
- Integration tests should follow the pattern in `tests/api/sbom.rs` — set up test data (two SBOMs with known packages/advisories), call the endpoint, assert on response status and body fields.
- Test with SBOMs that have overlapping and non-overlapping packages to verify all diff categories.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern with `Result<Json<T>, AppError>` return type
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `tests/api/sbom.rs` — integration test setup and assertion patterns
- `common/src/error.rs::AppError` — error handling, automatic `IntoResponse` conversion

## Dependencies
- Depends on: Task 2 — Backend comparison model and diff service

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200 OK` with the structured diff JSON
- [ ] Missing `left` or `right` query param returns `400 Bad Request`
- [ ] Non-existent SBOM ID returns `404 Not Found`
- [ ] Response JSON shape matches the contract: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] p95 response time under 1 second for SBOMs with up to 2000 packages (non-functional requirement)

## Test Requirements
- [ ] Integration test: create two SBOMs with different package sets, call comparison endpoint, verify response contains correct added/removed/changed packages
- [ ] Integration test: call comparison endpoint with missing query params, verify 400 response
- [ ] Integration test: call comparison endpoint with non-existent SBOM ID, verify 404 response
- [ ] Integration test: compare SBOMs with different advisories, verify new_vulnerabilities and resolved_vulnerabilities are correct
- [ ] Integration test: compare SBOMs where a package changed license, verify license_changes is populated

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint tests pass
