# Implementation Plan: TC-9203 - Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to the `GET /api/v2/package` endpoint, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add `license` query parameter extraction and filtering to the package list endpoint handler.

**Changes:**
- Add an optional `license: Option<String>` field to the query parameter struct (following the same pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, pass the extracted `license` value to the `PackageService::list` method so it can be applied as a filter.
- No new utility functions are created here; the filtering logic is delegated to the service layer which uses the existing `apply_filter` helper from `common/src/db/query.rs`.

**Reuse:**
- Follow the structural pattern from `modules/fundamental/src/advisory/endpoints/list.rs` for adding the optional query parameter field and passing it to the service. The advisory endpoint's `severity` parameter demonstrates the exact same pattern: an optional string field on the Query struct, extracted and forwarded to the service.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filter logic to the `PackageService::list` method.

**Changes:**
- Accept the optional `license` filter value (passed from the endpoint handler).
- When a `license` value is present, use `common/src/db/query.rs::apply_filter` to parse the comma-separated string into individual values and generate the appropriate SQL `IN` clause.
- Join through the `entity/src/package_license.rs` entity (the `package_license` table) to filter packages by their associated license SPDX identifiers. Use SeaORM's relation/join API with the existing `package_license` entity rather than writing raw SQL.
- When no `license` parameter is provided, the query remains unchanged (no filtering, no regression).
- Add validation: if a `license` value is syntactically invalid (e.g., empty segments from malformed commas), return a 400 Bad Request via `AppError`.

**Reuse:**
- Call `apply_filter` from `common/src/db/query.rs` directly for comma-separated multi-value parsing and SQL IN clause generation. Do NOT create a new parsing or filtering utility.
- Use the `package_license` entity from `entity/src/package_license.rs` for the JOIN query. This entity already maps the package-license relationship and provides SeaORM column/relation definitions needed for the join.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Changes:**
- Create a new test file following the patterns established in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with sibling tests.
- Seed the test database with packages having known license values (e.g., MIT, Apache-2.0, GPL-3.0).

**Test cases:**
1. **`test_list_packages_filter_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Assert on specific package identifiers in the response, not just count.
2. **`test_list_packages_filter_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert on the returned items containing both MIT and Apache-2.0 packages.
3. **`test_list_packages_no_license_filter`** -- Verifies that `GET /api/v2/package` without the license parameter returns all packages unchanged (no regression).
4. **`test_list_packages_invalid_license`** -- Verifies that an invalid license value returns `400 Bad Request`.

**Conventions to follow:**
- Test naming: `test_<endpoint>_<scenario>` pattern.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- Value-based assertions on specific fields (license values, package identifiers), not just length checks.
- Response validation: deserialize body into `PaginatedResults<PackageSummary>` and check `total_count`, `items`, and key fields.

## Files NOT Modified

The following files are explicitly out of scope:
- `modules/fundamental/src/package/model/summary.rs` -- PackageSummary already includes a `license` field; no changes needed.
- `modules/fundamental/src/package/endpoints/mod.rs` -- Route registration does not need changes since the endpoint path stays the same; only the handler's accepted query parameters change.
- `entity/src/package_license.rs` -- Used as-is for the JOIN query; no modifications needed.
- `common/src/db/query.rs` -- The existing `apply_filter` function already handles comma-separated multi-value parsing; no modifications needed.

## Data-Flow Trace

1. **Input:** HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at the Axum router.
2. **Extraction:** `list.rs` endpoint handler deserializes query parameters, extracting `license: Some("MIT,Apache-2.0")`.
3. **Service call:** Handler passes the license filter value to `PackageService::list()`.
4. **Filter application:** `PackageService::list()` calls `apply_filter` from `common/src/db/query.rs` which parses `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]` and generates a SQL `IN` clause.
5. **JOIN:** The service builds a SeaORM query that joins `package` with `package_license` (using `entity/src/package_license.rs`) and applies the filter on the license column.
6. **Output:** The filtered results are wrapped in `PaginatedResults<PackageSummary>` and returned as the HTTP response. The response shape is unchanged.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` -- add license filter logic to the list method.
2. Modify `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter to the Query struct and pass it to the service.
3. Create `tests/api/package_license_filter.rs` -- write integration tests.
4. Run `cargo test` to verify all tests pass.
5. Verify acceptance criteria.
6. Self-verification checks (scope containment, sensitive-pattern check, duplication check).
