# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Target Branch

main

## Dependencies

None.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Contains the `GET /api/v2/package` handler returning `PaginatedResults<PackageSummary>` with existing query parameter extraction (pagination, sorting).

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern established in `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter Query struct), add an `Option<String>` field named `license` to the existing query parameters struct. This mirrors how the advisory endpoint's `severity` optional field is declared.

- **Pass the license parameter to the service layer:** Extract `query.license` and pass it to `PackageService::list()` as an additional parameter. Follow the same calling convention used by the advisory list endpoint when passing its `severity` filter to `AdvisoryService`.

- **No changes to the response shape:** The handler continues to return `PaginatedResults<PackageSummary>` unchanged.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries packages and returns paginated results.

**Changes:**

- **Add `license` parameter to the `list` method signature:** Add an `Option<String>` parameter for the license filter, matching the pattern used by `AdvisoryService` for its severity filter.

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`:** When the `license` parameter is `Some`, call `apply_filter` to handle comma-separated multi-value parsing and SQL `IN` clause generation. This is the same utility used throughout the codebase for query parameter filtering -- reuse it directly rather than writing custom parsing or SQL logic.

- **Join through `entity/src/package_license.rs`:** Use the existing `package_license` SeaORM entity to join the `package` table to the `package_license` table. This entity already maps packages to their declared licenses. Apply the filter condition on the license column of the joined `package_license` table.

- **Return 400 Bad Request for invalid license values:** Add validation for the license parameter. If a license value fails validation, return an `AppError` that maps to HTTP 400, following the existing error handling pattern (all handlers return `Result<T, AppError>` with `.context()` wrapping).

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the `GET /api/v2/package` endpoint.

**Test functions to implement:**

1. **`test_list_packages_filter_by_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Seeds the test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0), sends the request, and asserts that only MIT-licensed packages appear in the response. Asserts on specific package identifiers, not just count.

2. **`test_list_packages_filter_by_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Seeds test data, sends the request, and asserts that both MIT and Apache-2.0 packages appear while GPL-3.0 packages do not. Asserts on specific package identifiers.

3. **`test_list_packages_no_license_filter`** -- Verifies that `GET /api/v2/package` without a license parameter returns all packages unchanged (no regression). Seeds test data, sends the request, asserts the full set is returned.

4. **`test_list_packages_invalid_license`** -- Verifies that an invalid license value returns HTTP 400 Bad Request. Sends a request with an invalid value, asserts `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions to follow (from sibling test files `tests/api/advisory.rs`, `tests/api/sbom.rs`):**

- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for success cases
- Validate `total_count`, `items.len()`, and at least one item's key fields
- Follow `test_<endpoint>_<scenario>` naming pattern
- Add `///` doc comments on every test function
- Use given-when-then section comments for non-trivial tests
- Hit a real PostgreSQL test database (integration test pattern)
- Register the test file in `tests/api/` module (add `mod package_license_filter;` to the test module root)

## Integration Points

- **Module registration:** No new route registration needed -- the existing `modules/fundamental/src/package/endpoints/mod.rs` already registers the list endpoint. The change is additive (new optional query parameter on an existing endpoint).

- **Cargo.toml:** No dependency changes needed -- `common/src/db/query.rs` and `entity/src/package_license.rs` are already dependencies of the `fundamental` module.

## Code Reuse Summary

All three Reuse Candidates from the task description are used:

1. **`common/src/db/query.rs::apply_filter`** -- Called directly in `PackageService::list()` to parse comma-separated license values and generate the SQL `IN` clause. No new parsing or SQL generation code is written.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- The severity filter pattern (optional field in the Query struct, passed to the service layer) is followed structurally for the license filter. Same approach for struct definition, extraction, and service call delegation.

3. **`entity/src/package_license.rs`** -- The existing SeaORM entity is used for the JOIN query in the service layer, rather than writing raw SQL or creating a new entity.

## Data-Flow Trace

- **Input:** HTTP query parameter `license` arrives at the list endpoint handler
- **Extraction:** Axum deserializes the query string into the Query struct, populating the `license: Option<String>` field
- **Delegation:** Handler passes `query.license` to `PackageService::list()`
- **Filtering:** Service calls `apply_filter` to parse comma-separated values and build the SQL `IN` clause, then JOINs through `package_license` entity to filter packages
- **Validation:** Invalid license values cause the service to return an `AppError` which Axum maps to 400 Bad Request
- **Output:** Filtered results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON -- response shape unchanged

## Acceptance Criteria Verification Plan

| Criterion | Verified By |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_filter_by_single_license` + manual trace through `apply_filter` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns either-match | `test_list_packages_filter_by_multiple_licenses` + `apply_filter` handles comma-split |
| No license parameter returns all packages | `test_list_packages_no_license_filter` + `Option::None` skips filter in service |
| Response shape `PaginatedResults<PackageSummary>` unchanged | No changes to response types; only query input changes |
| Invalid license values return 400 | `test_list_packages_invalid_license` + validation in service layer |
