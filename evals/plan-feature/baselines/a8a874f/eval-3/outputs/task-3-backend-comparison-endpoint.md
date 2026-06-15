# TC-9003-3: Backend comparison endpoint and integration tests

## Repository

trustify-backend

## Target Branch

TC-9003

## Description

Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint validates both SBOM IDs, invokes the comparison service, and returns the structured diff as JSON. Integration tests verify the endpoint against a real PostgreSQL test database using the project's established testing patterns.

## Files to Create

- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare` with `left` and `right` query parameters
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing `/api/v2/sbom` routes
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a module file exists, or ensure the new test file is discovered

## Dependencies

- TC-9003-2 (comparison models and diff service must exist)

## Implementation Notes

- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`: define a handler function that extracts query parameters, calls the service, and returns the result.
- Use Axum's `Query<T>` extractor to parse `left` and `right` SBOM ID parameters from the query string, consistent with how `list.rs` and `get.rs` extract parameters.
- The handler should return `Result<Json<SbomComparison>, AppError>` following the error handling pattern in `common/src/error.rs`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing list and get routes (pattern: `.route("/compare", get(compare_handler))`).
- Integration tests in `tests/api/sbom_compare.rs` should follow the pattern in `tests/api/sbom.rs`: set up test SBOMs with known packages and advisories, call the endpoint, and assert the response structure and diff correctness.
- Test cases should cover: valid comparison, left SBOM not found (404), right SBOM not found (404), same SBOM on both sides (empty diff).
- Validate the p95 < 1s NFR by ensuring the query plan is efficient; consider adding an index hint comment for future optimization if large SBOM comparisons are slow.

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the `SbomComparison` JSON
- [ ] Missing `left` or `right` parameter returns 400
- [ ] Invalid SBOM ID returns 404
- [ ] Response JSON matches the contract specified in the feature requirements
- [ ] Route is registered under the existing `/api/v2/sbom` path namespace

## Test Requirements

- [ ] Integration test: compare two SBOMs with known differences, assert added/removed packages and version changes
- [ ] Integration test: compare two SBOMs with different advisory associations, assert new/resolved vulnerabilities
- [ ] Integration test: request with nonexistent SBOM ID returns 404
- [ ] Integration test: request with missing parameters returns 400
- [ ] Integration test: comparing an SBOM with itself returns empty diff arrays

## Verification Commands

- `cargo test --test api -- sbom_compare` — run comparison endpoint integration tests
- `cargo clippy --all-targets` — verify no lint warnings in new code

## Convention Compliance

- `Applies: task creates modules/fundamental/src/sbom/endpoints/compare.rs matching the convention's endpoint registration scope.`
- `Applies: task creates tests/api/sbom_compare.rs matching the convention's integration testing scope (tests/api/).`
- `Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's route registration scope.`

[Description digest: sha256-md:c5f9e3a1b8d4f0c6a2e7b3d9f5a1c7e3b0d6f2a8c4e0b7d3f9a5c1e8b4d0f6a2]
