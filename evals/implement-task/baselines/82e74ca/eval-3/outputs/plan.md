# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value exact matching on the SPDX license identifier. The implementation reuses the existing `apply_filter` helper and follows the advisory severity filter pattern.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests, extracts query parameters, and calls `PackageService::list`.

**Changes:**

- **Add `license` field to the query parameter struct:** Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` where the advisory list endpoint has an optional `severity` field in its `Query` struct, add an `Option<String>` field named `license` to the package list endpoint's Query struct.

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct PackageListQuery {
      // ... existing fields (pagination, sorting) ...
      pub license: Option<String>,
  }
  ```

- **Pass the license parameter to the service layer:** After extracting the query parameters, pass `query.license` to the `PackageService::list` method call. This mirrors how the advisory endpoint passes its `severity` parameter to `AdvisoryService::list`.

- **Add input validation:** Validate that if `license` is provided, its values are non-empty strings. Return `400 Bad Request` (via `AppError`) for empty or malformed values. Use the same error-handling pattern as the advisory endpoint (`.context()` wrapping with `Result<T, AppError>`).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries packages from the database and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add `license` parameter to the `list` method signature:** Add an `Option<String>` parameter for the license filter, matching the advisory service pattern where `AdvisoryService::list` accepts an optional severity filter parameter.

  ```rust
  pub async fn list(
      &self,
      // ... existing params (pagination, sorting) ...
      license: Option<String>,
  ) -> Result<PaginatedResults<PackageSummary>, AppError> {
  ```

- **Apply license filter using `apply_filter`:** When `license` is `Some`, use the `apply_filter` function from `common/src/db/query.rs` to parse the comma-separated values and generate the SQL `IN` clause. This is the same function used throughout the codebase for multi-value filtering.

  ```rust
  use common::db::query::apply_filter;

  // Inside the list method, after building the base query:
  if let Some(ref license_param) = license {
      query = apply_filter(query, "package_license", "license", license_param)?;
  }
  ```

- **Join with `package_license` entity:** Add a JOIN to the `package_license` table (defined in `entity/src/package_license.rs`) so the filter can match against the license column. Use SeaORM's join API, following the same join pattern used elsewhere in the fundamental module.

  ```rust
  use entity::package_license;

  // Add join to query builder
  query = query.join(
      JoinType::InnerJoin,
      package_license::Entity,
      package_license::Column::PackageId.eq(package::Column::Id),
  );
  ```

- **Ensure no-filter case is unchanged:** When `license` is `None`, the join and filter are skipped entirely, preserving the existing behavior for `GET /api/v2/package` without the license parameter.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Follows test conventions from:** `tests/api/advisory.rs` and `tests/api/sbom.rs` (sibling test files using the `assert_eq!(resp.status(), StatusCode::OK)` pattern and real PostgreSQL test database).

**Test functions:**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200, response body contains only packages with MIT license, each returned package's license field equals "MIT"

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200, response body contains packages with MIT and Apache-2.0 but not GPL-3.0, assert on specific license values (not just count)

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200, all packages are returned, total count matches expected count

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Test database is available
   - When: `GET /api/v2/package?license=` (empty value)
   - Then: Response status is 400 Bad Request

**Structure conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions (from sibling tests)
- Use given-when-then section comments inside each test body
- Validate specific field values, not just collection lengths
- Deserialize response body into `PaginatedResults<PackageSummary>` for type-safe assertions
- Follow `test_<endpoint>_<scenario>` naming pattern

## Files NOT Modified (confirming scope)

- `entity/src/package_license.rs` -- Already exists with the package-license mapping; used as-is for the JOIN, no modifications needed.
- `common/src/db/query.rs` -- The `apply_filter` function already supports comma-separated multi-value parsing; reused directly, no modifications needed.
- `common/src/model/paginated.rs` -- `PaginatedResults<PackageSummary>` response shape is unchanged.
- `modules/fundamental/src/package/endpoints/mod.rs` -- Route registration does not change; the existing route for `GET /api/v2/package` will pick up the new optional query parameter automatically.
- `modules/fundamental/src/package/model/summary.rs` -- `PackageSummary` struct is unchanged.

## Data-Flow Trace

```
GET /api/v2/package?license=MIT,Apache-2.0
  -> Axum extracts PackageListQuery (endpoints/list.rs) [INPUT]
  -> Handler validates license parameter [PROCESSING - validation]
  -> Handler calls PackageService::list(license: Some("MIT,Apache-2.0")) [PROCESSING - delegation]
  -> PackageService builds query, JOINs package_license table [PROCESSING - query building]
  -> apply_filter() parses "MIT,Apache-2.0" into ["MIT", "Apache-2.0"] [PROCESSING - filter]
  -> apply_filter() generates SQL WHERE ... IN ('MIT', 'Apache-2.0') [PROCESSING - SQL]
  -> SeaORM executes query against PostgreSQL [PROCESSING - execution]
  -> Results wrapped in PaginatedResults<PackageSummary> [OUTPUT]
  -> JSON response returned to client [OUTPUT]
```

All stages are connected -- the data flows from HTTP request through validation, filtering, query execution, and back to the response.

## Convention Conformance

The implementation follows these established patterns:

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping (same as all `endpoints/` files)
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Filtering uses `common/src/db/query.rs` shared utilities
- **Module structure:** `model/ + service/ + endpoints/` pattern is maintained
- **Testing:** Integration tests use real PostgreSQL with `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Framework:** Axum for HTTP routing, SeaORM for database queries
