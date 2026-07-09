# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing infrastructure throughout -- no new utility functions are needed.

## Step-by-step plan

### 1. Understand the code (Step 4)

#### Files to inspect before modifying

- `modules/fundamental/src/advisory/endpoints/list.rs` -- the severity filter implementation here is the structural template. Inspect the `Query` struct definition to see how optional filter fields are declared, and how they are passed to the service layer.
- `common/src/db/query.rs` -- read the `apply_filter` function signature and behavior. Confirm it accepts a comma-separated string, splits it, and generates a SQL `IN` clause. This is the function we will reuse directly for parsing and SQL generation.
- `entity/src/package_license.rs` -- inspect the SeaORM entity to understand the table schema (columns, relations) for the package-license join table. This entity will be used in the JOIN query.
- `modules/fundamental/src/package/endpoints/list.rs` -- current state of the file to modify. Inspect the existing `Query` struct and handler function.
- `modules/fundamental/src/package/service/mod.rs` -- current `PackageService::list` method signature and query-building logic.
- `modules/fundamental/src/package/model/summary.rs` -- confirm `PackageSummary` struct shape (includes `license` field per repo docs).
- `common/src/model/paginated.rs` -- confirm `PaginatedResults<T>` wrapper (response shape must not change).

#### Sibling files for convention analysis

- `modules/fundamental/src/sbom/endpoints/list.rs` -- sibling list endpoint for convention patterns.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- primary sibling, explicitly referenced as the pattern to follow.
- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- sibling test files for test convention analysis.

#### Documentation files to check

- `docs/api.md` -- REST API reference; may need updating to document the new `license` parameter.
- `CONVENTIONS.md` -- repository root conventions file; read for CI check commands and coding standards.

### 2. Files to Modify

#### `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the `Query` struct**: Following the exact pattern from `modules/fundamental/src/advisory/endpoints/list.rs`, add an `Option<String>` field named `license` to the existing `Query` struct used for deserializing query parameters. The advisory endpoint's `Query` struct has an optional `severity` field that follows this same pattern -- mirror it exactly.

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter. Supports single value or comma-separated list of SPDX identifiers.
       pub license: Option<String>,
   }
   ```

2. **Pass the `license` filter to the service layer**: In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter. Follow the same call pattern used in the advisory list handler when it passes `query.severity` to `AdvisoryService::list()`.

3. **No new utility functions**: Do NOT create any new parsing or filtering helper. The comma-separated string is passed as-is to the service layer, which delegates to `apply_filter` from `common/src/db/query.rs`.

#### `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Update `PackageService::list` method signature**: Add an `license: Option<String>` parameter to the `list` method, mirroring how `AdvisoryService::list` accepts an optional `severity` parameter.

2. **Import and use `apply_filter` from `common/src/db/query.rs`**: This is the critical reuse point. `apply_filter` already handles:
   - Splitting a comma-separated string into individual values
   - Generating a SQL `WHERE ... IN (...)` clause
   - Handling the single-value case (no comma) as a simple equality check
   
   Call `apply_filter` with the `license` value and the appropriate column reference from `entity::package_license`.

3. **Add a JOIN through `entity/src/package_license.rs`**: Use the SeaORM entity `package_license::Entity` to construct a JOIN between the `package` table and the `package_license` table. The `package_license` entity already maps the relationship -- use its `Relation` definitions to build the join rather than writing raw SQL. The join condition links `package.id` to `package_license.package_id`, and the filter is applied on `package_license.license` (the SPDX identifier column).

   ```rust
   // Pseudocode for the query modification:
   use entity::package_license;
   
   let mut query = package::Entity::find();
   
   if let Some(ref license_filter) = license {
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           // apply_filter handles comma-separated parsing and IN clause generation
           .filter(apply_filter(package_license::Column::License, license_filter));
   }
   ```

4. **Validate license values**: Add validation for the license parameter before applying the filter. If the provided value is empty or contains only whitespace after splitting, return a 400 Bad Request error using `AppError` (following the existing error handling pattern with `.context()`).

### 3. Files to Create

#### `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Convention compliance:** Follow the test patterns discovered from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
- Validate `total_count`, `items.len()`, and specific item field values
- Follow `test_<endpoint>_<scenario>` naming pattern
- Add `///` doc comments on every test function
- Use given-when-then section comments for non-trivial tests

**Test functions to implement:**

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: packages with MIT and Apache-2.0 licenses exist in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only MIT-licensed packages are returned
    // Assert on specific package names/identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
    // Assert on specific license values in returned items
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: packages with various licenses exist
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned, response shape is PaginatedResults<PackageSummary>
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // Given: the endpoint is available
    // When: GET /api/v2/package?license= (empty value)
    // Then: 400 Bad Request is returned
}
```

**Module registration:** Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) if the test module system requires explicit registration.

### 4. Files NOT modified (out of scope)

The following files are explicitly NOT modified, confirming scope containment:

- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration does not change; the existing route for `GET /api/v2/package` already dispatches to `list.rs`.
- `modules/fundamental/src/package/model/summary.rs` -- `PackageSummary` struct is unchanged; the response shape is not modified.
- `common/src/db/query.rs` -- `apply_filter` is reused as-is; no modifications needed.
- `entity/src/package_license.rs` -- the entity is used for JOIN queries but not modified.
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper is unchanged.

### 5. Verification checklist

- Acceptance Criteria mapping:
  - `GET /api/v2/package?license=MIT` returns only MIT packages -- covered by `apply_filter` generating `WHERE license = 'MIT'` and tested by `test_list_packages_filter_single_license`
  - `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either -- covered by `apply_filter` generating `WHERE license IN ('MIT', 'Apache-2.0')` and tested by `test_list_packages_filter_multiple_licenses`
  - No license parameter returns all packages -- the `Option<String>` field is `None` when absent, skipping the filter entirely; tested by `test_list_packages_no_license_filter`
  - Response shape `PaginatedResults<PackageSummary>` unchanged -- no modifications to model or response types
  - Invalid license values return 400 -- validation logic in service layer; tested by `test_list_packages_invalid_license_returns_400`

### 6. Data-flow trace

- `GET /api/v2/package?license=MIT` -> Axum deserializes query into `Query` struct (license: `Some("MIT")`) -> handler passes `license` to `PackageService::list()` -> service calls `apply_filter(column, "MIT")` which generates SQL condition -> SeaORM executes query with JOIN on `package_license` table and `WHERE license = 'MIT'` -> results wrapped in `PaginatedResults<PackageSummary>` -> JSON response returned -- **COMPLETE**

### 7. Documentation impact

- `docs/api.md` -- update the `GET /api/v2/package` endpoint documentation to include the new optional `license` query parameter, its type (string), and the comma-separated multi-value behavior.
