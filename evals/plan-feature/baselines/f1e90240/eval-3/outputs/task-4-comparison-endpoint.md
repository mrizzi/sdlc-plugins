# Task 4: Add SBOM comparison endpoint and integration tests

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 3

## Repository

trustify-backend

## Target Branch

TC-9003

## Description

Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. Register the route in the SBOM module's endpoint configuration. Add integration tests that verify the endpoint returns correct diff results against a real test database.

## Files to Create

- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Axum handler: extracts `left` and `right` query parameters, calls `SbomComparisonService::compare()`, returns JSON response
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/compare` route under the existing `/api/v2/sbom` prefix
- `tests/api/mod.rs` or test harness -- Add `mod sbom_compare;` if tests use a module structure

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response JSON shape matches the contract: top-level object with six array fields
- [ ] Integration tests pass against the PostgreSQL test database
- [ ] Route is registered within the SBOM module's router (not as a standalone mount)

## Test Requirements

- Integration test: create two SBOMs with overlapping and differing packages, call the compare endpoint, assert all six diff categories contain expected items.
- Integration test: call with non-existent left ID, assert 404.
- Integration test: call with missing query params, assert 400.
- Integration test: compare an SBOM with itself, assert all diff categories are empty arrays.

## Implementation Notes

Create the handler in `modules/fundamental/src/sbom/endpoints/compare.rs` following the pattern of `list.rs` and `get.rs` in the same directory. Use Axum's `Query` extractor for the `left` and `right` parameters:

```rust
#[derive(Deserialize)]
pub struct CompareQuery {
    left: Uuid,
    right: Uuid,
}
```

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding `.route("/compare", get(compare::compare))` to the existing router builder.

For integration tests, follow the pattern in `tests/api/sbom.rs`: set up test data by ingesting two SBOMs with known package lists, then call the endpoint and assert the response body.

## Applicable Conventions

- **Module pattern** (model/ + service/ + endpoints/): Applies: task modifies `modules/fundamental/src/sbom/endpoints/` matching the convention's module structure scope.
- **Error handling** (Result<T, AppError> with .context()): Applies: task creates endpoint handler in `compare.rs` matching the convention's error handling scope.
- **Endpoint registration** (endpoints/mod.rs registers routes): Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.
- **Testing** (integration tests in tests/api/ with real PostgreSQL): Applies: task creates `tests/api/sbom_compare.rs` matching the convention's integration test scope.
