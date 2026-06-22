# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, enabling consumers to filter packages by their declared SPDX license identifier. Support both single-value and comma-separated multi-value filtering.

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests. Contains a query parameter struct and a handler function that delegates to `PackageService::list`.

**Changes:**

- **Add `license` field to the query parameter struct:** Following the pattern established in `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter), add an `Option<String>` field named `license` to the existing query/filter struct used by this endpoint. This mirrors how the advisory list endpoint declares its `severity` query parameter as an optional string field in its Query struct.

- **Pass the license filter to the service layer:** In the handler function, extract the `license` value from the query struct and pass it to `PackageService::list`. This follows the same data-flow pattern as the advisory endpoint, where the severity filter value is extracted from the query struct and forwarded to the service method.

- **Validate the license parameter:** Add validation to return `400 Bad Request` for invalid license values (e.g., empty strings after splitting on commas). Use the existing `AppError` enum from `common/src/error.rs` to produce the error response, matching the error handling convention used throughout the codebase (`Result<T, AppError>` with `.context()` wrapping).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries packages from the database and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add `license` parameter to the `list` method signature:** Accept an `Option<String>` parameter for the license filter, matching how `AdvisoryService::list` accepts its severity filter parameter.

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`:** This is the key reuse point. The `apply_filter` function already handles:
  - Parsing comma-separated multi-value strings into individual values
  - Generating SQL `IN` clause conditions for multi-value filters
  - Handling single-value filters as equality conditions
  
  Call `apply_filter` with the license value and the appropriate column reference from the `package_license` entity. Do NOT write custom comma-splitting or SQL generation logic -- `apply_filter` already provides this exact functionality.

- **Join through the `package_license` entity:** Use `entity/src/package_license.rs` (the existing SeaORM entity for the package-license join table) to join the `package` table with the `package_license` table when the license filter is present. This follows SeaORM's relation-based join patterns already used elsewhere in the codebase. The join should only be added when the license filter is actually provided, to avoid unnecessary JOINs on unfiltered queries.

- **Preserve response shape:** Ensure the return type remains `PaginatedResults<PackageSummary>` -- only the query is modified, not the response structure.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the `GET /api/v2/package` endpoint.

**Test cases (following the conventions from sibling test files like `tests/api/advisory.rs` and `tests/api/sbom.rs`):**

1. **`test_filter_packages_by_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Asserts on specific package identifiers in the response, not just count.

2. **`test_filter_packages_by_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Asserts that both MIT and Apache-2.0 licensed packages appear in results, and packages with other licenses do not.

3. **`test_list_packages_without_license_filter`** -- Verifies that `GET /api/v2/package` (no license parameter) returns all packages unchanged, confirming no regression to the existing behavior.

4. **`test_invalid_license_value_returns_400`** -- Verifies that an invalid license value returns `400 Bad Request`. Uses `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.

**Conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Deserialize response body and validate `total_count`, `items.len()`, and key fields
- Follow `test_<endpoint>_<scenario>` naming pattern
- Tests hit a real PostgreSQL test database (integration test pattern used in `tests/api/`)
- Add `///` doc comments to every test function explaining what it verifies
- Use `// Given`, `// When`, `// Then` section comments in test bodies

## Module Registration

The new test file `tests/api/package_license_filter.rs` needs to be registered in `tests/Cargo.toml` (or `tests/api/mod.rs` if one exists) so the test runner discovers it. This follows the same pattern used by the existing test files (`sbom.rs`, `advisory.rs`, `search.rs`).

## API Changes

- `GET /api/v2/package` -- MODIFIED: accepts new optional `license` query parameter
  - `?license=MIT` -- filters to packages with MIT license (single value)
  - `?license=MIT,Apache-2.0` -- filters to packages with MIT OR Apache-2.0 license (comma-separated multi-value)
  - No `license` parameter -- returns all packages (existing behavior preserved)
  - Invalid license values -- returns `400 Bad Request`
- Response shape (`PaginatedResults<PackageSummary>`) is NOT changed

## Data-Flow Trace

1. **Input:** HTTP request `GET /api/v2/package?license=MIT,Apache-2.0` arrives at the endpoint handler in `list.rs`
2. **Extraction:** The `license` field is extracted from the query struct as `Option<String>`
3. **Validation:** If present, the license string is validated (non-empty values after comma-split)
4. **Service call:** The handler calls `PackageService::list(...)` passing the license filter
5. **Query building:** The service method calls `apply_filter` (from `common/src/db/query.rs`) to generate the SQL filter condition, joining through `package_license` entity
6. **Database query:** SeaORM executes the query with the license filter applied via JOIN + IN clause
7. **Output:** Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON

All stages are connected -- no gaps in the data flow.

## Scope Boundary

All changes are strictly within the files listed in "Files to Modify" and "Files to Create" in the task description. No other files will be modified. The response shape is preserved, and no existing behavior is altered for requests without the `license` parameter.
