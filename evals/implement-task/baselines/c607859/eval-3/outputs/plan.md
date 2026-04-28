# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

---

## Project Configuration Validation

- **Repository Registry**: `trustify-backend` mapped to Serena instance `serena_backend` at `./`
- **Jira Configuration**: Project key `TC`, Cloud ID present, Feature issue type ID present
- **Code Intelligence**: `serena_backend` instance with `rust-analyzer`

All required sections present. Proceed.

---

## Dependencies

No dependencies listed. Proceed.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: This file implements `GET /api/v2/package`. It contains a query parameter extraction struct and a handler function that calls `PackageService::list()`.

**Changes**:

- **Add `license` field to the Query struct**: Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter's Query struct), add an `Option<String>` field named `license` to the existing `PackageListQuery` struct (or whatever the query extraction struct is named). This field will capture the raw `?license=` query parameter value.

  ```rust
  /// Optional license filter; supports single SPDX identifier or comma-separated list.
  pub license: Option<String>,
  ```

- **Pass the license filter to the service layer**: In the handler function, pass `query.license` to the `PackageService::list()` call. This follows the same pattern as how the advisory list handler passes `query.severity` to `AdvisoryService::list()`.

- **Input validation**: Before passing to the service layer, validate that the license parameter (if present) contains only valid characters for SPDX identifiers (alphanumeric, hyphens, dots, plus signs). If invalid, return a `400 Bad Request` using the existing `AppError` pattern from `common/src/error.rs`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: This file contains `PackageService` with a `list()` method that queries the database for packages and returns `PaginatedResults<PackageSummary>`.

**Changes**:

- **Add `license` parameter to `list()` method**: Add an `Option<String>` parameter (or extend an existing query/filter struct parameter) to accept the license filter value.

- **Apply the license filter using `apply_filter` from `common/src/db/query.rs`**: This is the key reuse point. The `apply_filter` function already handles:
  - Parsing comma-separated values into a `Vec<String>`
  - Generating a SQL `IN` clause for multi-value filtering
  - Handling the single-value case as a degenerate multi-value case

  Call `apply_filter` with the license parameter and the appropriate column reference.

- **JOIN through `entity/src/package_license.rs`**: Use the existing `package_license` SeaORM entity to join the `package` table to the `package_license` table. This reuses the existing entity definition rather than writing raw SQL. The join would look like:

  ```rust
  // Reuse the existing package_license entity for the JOIN
  use entity::package_license;

  if let Some(license_value) = &license {
      query = query
          .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
          .filter(apply_filter(package_license::Column::License, license_value));
  }
  ```

  The exact column name on `package_license` will be confirmed by inspecting the entity with Serena, but the pattern follows SeaORM's standard relation-based joins.

- **Ensure DISTINCT**: When joining through a many-to-many relationship (package to license), add `.distinct()` to the query to prevent duplicate packages in the results when a package matches multiple license values.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter on `GET /api/v2/package`.

**Structure**: Follow the test conventions observed in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Validate `PaginatedResults` structure: check `total_count`, `items.len()`, and key fields of returned items
- Use `test_<endpoint>_<scenario>` naming convention
- Include given-when-then section comments inside each test body
- Add a doc comment (`///`) before every test function

**Test cases**:

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[test]
fn test_list_packages_single_license_filter() {
    // Given packages with different licenses exist in the database
    // (seed MIT-licensed and Apache-2.0-licensed packages)

    // When requesting packages filtered by MIT license
    // GET /api/v2/package?license=MIT

    // Then only MIT-licensed packages are returned
    // assert on specific package identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[test]
fn test_list_packages_multi_license_filter() {
    // Given packages with MIT, Apache-2.0, and GPL-3.0 licenses exist

    // When requesting packages filtered by MIT,Apache-2.0
    // GET /api/v2/package?license=MIT,Apache-2.0

    // Then packages with MIT or Apache-2.0 are returned, but not GPL-3.0
    // assert on specific package identifiers
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[test]
fn test_list_packages_no_license_filter() {
    // Given packages with various licenses exist

    // When requesting packages without a license filter
    // GET /api/v2/package

    // Then all packages are returned (no regression)
    // assert total_count matches expected total
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[test]
fn test_list_packages_invalid_license_filter() {
    // Given the API is available

    // When requesting packages with an invalid license value
    // GET /api/v2/package?license=<invalid>

    // Then a 400 Bad Request is returned
    // assert_eq!(resp.status(), StatusCode::BAD_REQUEST)
}
```

**Module registration**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test runner entry point) so the new test file is compiled and executed as part of the integration test suite.

---

## Additional Files Potentially Affected (Out-of-Scope Check)

- `modules/fundamental/src/package/endpoints/mod.rs` -- May need a minor update if route registration references the query struct from `list.rs` by name, but likely no change needed since the route handler function signature stays the same.
- `tests/api/mod.rs` (or equivalent) -- Needs `mod package_license_filter;` added to register the new test file. This is a necessary out-of-scope file that would require user approval during Step 9.

---

## API Changes

- `GET /api/v2/package` -- **MODIFY**: Add optional `license` query parameter
  - `?license=MIT` -- single-value exact match on SPDX identifier
  - `?license=MIT,Apache-2.0` -- comma-separated multi-value; returns packages matching ANY listed license
  - Omitting the parameter returns all packages (backward compatible)
  - Invalid license values return `400 Bad Request`
  - Response shape (`PaginatedResults<PackageSummary>`) remains unchanged

---

## Convention Conformance

Based on the repository conventions documented in `repo-backend.md`:

- **Framework**: Axum for HTTP, SeaORM for database -- all new code uses these
- **Module pattern**: The package module already follows `model/ + service/ + endpoints/` -- changes stay within this structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping -- the license validation error follows this pattern
- **Response types**: List endpoints return `PaginatedResults<T>` -- no change to response type
- **Query helpers**: Shared filtering via `common/src/db/query.rs` -- reusing `apply_filter` directly
- **Testing**: Integration tests in `tests/api/` using real PostgreSQL -- new test file follows this pattern

---

## Data-Flow Trace

1. **Input**: HTTP request `GET /api/v2/package?license=MIT` arrives at Axum router
2. **Extraction**: Axum deserializes query parameters into the `PackageListQuery` struct, populating `license: Some("MIT")`
3. **Validation**: Handler validates the license string format; returns 400 if invalid
4. **Processing**: Handler calls `PackageService::list()` passing the license filter
5. **Query building**: Service uses `apply_filter` from `common/src/db/query.rs` to parse comma-separated values and build SQL `IN` clause
6. **JOIN**: Service joins through `package_license` entity to filter packages by license
7. **Execution**: SeaORM executes the query against PostgreSQL
8. **Response**: Results wrapped in `PaginatedResults<PackageSummary>` and returned as JSON

All stages connected. **COMPLETE**.

---

## Acceptance Criteria Verification Plan

| Criterion | How Verified |
|---|---|
| `?license=MIT` returns only MIT packages | `test_list_packages_single_license_filter` |
| `?license=MIT,Apache-2.0` returns matching packages | `test_list_packages_multi_license_filter` |
| No `license` parameter returns all packages | `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` |
| Invalid license returns 400 | `test_list_packages_invalid_license_filter` |
