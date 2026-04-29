# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint. This enables consumers to filter packages by their declared SPDX license identifier, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Defines the handler for `GET /api/v2/package` with an existing query parameter struct (likely named `PackageQuery` or similar) and a handler function that calls the PackageService list method.

**Changes:**

- **Add `license` field to the query struct:** Add an `Option<String>` field named `license` to the existing query parameter struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`). This field receives the raw query string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

- **Pass `license` to service layer:** In the handler function, extract the `license` value from the query struct and pass it to `PackageService::list()` (or the equivalent service method). This is a straightforward addition to the existing parameter list, matching how the advisory endpoint passes its `severity` filter to `AdvisoryService`.

- **No new utility functions:** The comma-separated parsing and SQL IN clause generation is handled entirely by `common/src/db/query.rs::apply_filter` at the service/query-building layer. The endpoint layer only needs to extract the raw string and forward it.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method (or equivalent) that builds a SeaORM query for packages, applies existing filters (pagination, sorting), and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add `license` parameter to the list method signature:** Accept an `Option<String>` (or `Option<&str>`) for the license filter, matching the pattern used in the advisory service for its severity filter.

- **Build a JOIN query using `entity::package_license`:** When the `license` parameter is `Some(value)`, join the `package` table with the `package_license` entity (`entity/src/package_license.rs`) using SeaORM's relation/join API. This reuses the existing `package_license` entity rather than writing raw SQL.

- **Apply the filter using `apply_filter` from `common/src/db/query.rs`:** Call `apply_filter` with the license column from the `package_license` entity and the raw comma-separated string value. `apply_filter` handles:
  - Splitting the comma-separated string into individual values
  - Generating a SQL `IN` clause for multi-value filters
  - Generating a simple equality check for single-value filters
  
  This is the same function used across the codebase for multi-value query parameter filtering. No new parsing or utility code is needed.

- **Validate license values:** Add validation for the license parameter values. If any value is invalid (e.g., empty string after splitting), return an `AppError` that maps to a 400 Bad Request response, using the existing `AppError` enum from `common/src/error.rs` with `.context()` wrapping.

- **Preserve existing behavior:** When `license` is `None`, the query proceeds without the join or filter, ensuring no regression for callers that omit the parameter.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Structure:** Follow the test conventions observed in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
- Deserialize response body and validate both `total_count` and specific item field values (not just length checks)
- Follow `test_<endpoint>_<scenario>` naming convention

**Test cases:**

1. **`test_list_packages_filter_single_license`** — Seed test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0). Request `GET /api/v2/package?license=MIT`. Assert response status is 200, `total_count` matches expected number of MIT packages, and every returned `PackageSummary` has `license == "MIT"`.

2. **`test_list_packages_filter_multiple_licenses`** — Using the same seed data, request `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response status is 200, `total_count` matches the count of MIT + Apache-2.0 packages, and every returned item has a license that is either "MIT" or "Apache-2.0".

3. **`test_list_packages_no_license_filter`** — Request `GET /api/v2/package` without the license parameter. Assert response status is 200 and `total_count` matches the total number of seeded packages (no regression).

4. **`test_list_packages_invalid_license`** — Request `GET /api/v2/package?license=` (empty value) or with a known-invalid value. Assert response status is 400 Bad Request.

Each test function will include:
- A `///` doc comment explaining what it verifies
- `// Given`, `// When`, `// Then` section comments for non-trivial tests

## Files NOT Modified

The following files are explicitly out of scope and will not be touched:

- `entity/src/package_license.rs` — used as-is for the JOIN query; no modifications needed
- `common/src/db/query.rs` — `apply_filter` is reused directly; no modifications needed
- `common/src/model/paginated.rs` — response shape is unchanged
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct is unchanged
- `modules/fundamental/src/package/endpoints/mod.rs` — route registration is unchanged (same endpoint, new optional parameter only)

## API Changes

- `GET /api/v2/package` — MODIFIED: accepts new optional `license` query parameter
  - `?license=MIT` — single-value filter, returns only packages with MIT license
  - `?license=MIT,Apache-2.0` — comma-separated multi-value filter, returns packages matching any listed license
  - Omitting the parameter returns all packages (backward compatible)
  - Response shape (`PaginatedResults<PackageSummary>`) is unchanged

## Data Flow Trace

1. **Input:** HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Extraction:** Axum deserializes query parameters into the `PackageQuery` struct; `license` field receives `Some("MIT,Apache-2.0")`
3. **Handler:** The list handler passes the `license` value to `PackageService::list()`
4. **Service/Query Building:** `PackageService::list()` joins `package` with `package_license` entity, then calls `apply_filter` with the license column and the raw comma-separated string
5. **apply_filter processing:** `apply_filter` splits `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]` and generates a SQL `WHERE license_id IN ('MIT', 'Apache-2.0')` clause
6. **Query execution:** SeaORM executes the query against PostgreSQL
7. **Output:** Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON response

All stages are connected end-to-end. No partial implementation paths exist.

## Conventions Applied

- **Error handling:** `Result<T, AppError>` with `.context()` wrapping (from sibling handlers)
- **Response type:** `PaginatedResults<PackageSummary>` (from `common/src/model/paginated.rs`)
- **Query building:** Shared filter/pagination/sorting via `common/src/db/query.rs`
- **Entity usage:** SeaORM entities from `entity/src/` for all database operations
- **Test pattern:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Test naming:** `test_<endpoint>_<scenario>` pattern
