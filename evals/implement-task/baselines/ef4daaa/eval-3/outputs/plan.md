# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and
comma-separated multi-value filtering by SPDX license identifier. The implementation
reuses existing query helpers, follows the established advisory severity filter pattern,
and joins through the existing `package_license` entity.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Defines the handler for `GET /api/v2/package` with an existing `Query`
struct for extracting query parameters (pagination, sorting, possibly other filters).

**Changes:**

- **Add `license` field to the `Query` struct**: Add an `Option<String>` field named
  `license` to the existing query parameter struct, following the exact same pattern used
  by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`. The
  field should be optional so that omitting it returns all packages (no regression).

- **Pass the license filter to the service layer**: In the handler function, extract
  `query.license` and pass it to `PackageService::list()` as a new parameter (or as part
  of an expanded filter/options struct, depending on how the service method currently
  accepts parameters). This mirrors how the advisory list handler passes its `severity`
  filter to `AdvisoryService`.

- **Validate the license parameter**: If the license value is present but contains invalid
  characters or is empty after splitting on commas, return a `400 Bad Request` using the
  existing `AppError` enum from `common/src/error.rs`. Follow the same validation pattern
  used by the advisory severity filter.

**Reuse:**
- Follow the `Query` struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs`
  (Reuse Candidate 2) -- add the optional `license` field the same way `severity` is defined.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list()` method that queries the
`package` table, applies pagination and sorting, and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Accept a license filter parameter**: Extend the `list()` method signature to accept
  an optional license filter (e.g., `license: Option<String>`). This matches how
  `AdvisoryService` accepts the severity filter.

- **Join through `package_license` entity**: When the `license` filter is present, add a
  JOIN to the `package_license` table using the SeaORM entity defined in
  `entity/src/package_license.rs` (Reuse Candidate 3). This avoids writing raw SQL and
  leverages the existing entity relationship definitions.

- **Apply the filter using `apply_filter`**: Call `common::db::query::apply_filter`
  (Reuse Candidate 1) to handle parsing the comma-separated license string and generating
  the appropriate SQL `IN` clause. The `apply_filter` function already handles both
  single-value and multi-value comma-separated parameters, so no new parsing logic is
  needed.

- **Preserve return type**: The method must continue returning
  `PaginatedResults<PackageSummary>` -- only the query is extended with a conditional
  JOIN and WHERE clause when the license filter is present.

**Reuse:**
- `common/src/db/query.rs::apply_filter` (Reuse Candidate 1) -- called directly to parse
  the comma-separated license values and build the SQL filter condition.
- `entity/src/package_license.rs` (Reuse Candidate 3) -- used as the SeaORM entity for
  the JOIN between `package` and `package_license` tables.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on `GET /api/v2/package`.

**Structure:** Follow the test conventions observed in sibling test files (`tests/api/sbom.rs`,
`tests/api/advisory.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` for successful responses.
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for validation errors.
- Validate `total_count`, `items.len()`, and key fields on returned items.
- Follow the `test_<endpoint>_<scenario>` naming convention.

**Test cases:**

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: packages with MIT and Apache-2.0 licenses exist in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only MIT-licensed packages are returned
    // Assert on specific package identifiers, not just count
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
    // Assert on specific package identifiers in the response
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: packages with various licenses exist
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned unchanged
    // Assert response shape is PaginatedResults<PackageSummary>
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_filter() {
    // Given: the endpoint is available
    // When: GET /api/v2/package?license=<invalid>
    // Then: 400 Bad Request is returned
    // Assert on status code and error response body
}
```

**Test registration:** Ensure the new test file is included in `tests/Cargo.toml` or the
test module tree so `cargo test` discovers it.

---

## API Changes

| Endpoint | Method | Change |
|---|---|---|
| `/api/v2/package` | GET | Add optional `license` query parameter |
| `/api/v2/package?license=MIT` | GET | Filter by single SPDX license identifier |
| `/api/v2/package?license=MIT,Apache-2.0` | GET | Filter by multiple comma-separated licenses (OR semantics) |

The response shape (`PaginatedResults<PackageSummary>`) is unchanged.

---

## Data-Flow Trace

1. **Input**: HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Extraction**: Axum deserializes query parameters into the `Query` struct; `license`
   field is populated as `Some("MIT,Apache-2.0")`
3. **Validation**: Handler validates the license string is non-empty after comma-splitting;
   returns 400 if invalid
4. **Service call**: Handler passes `license` to `PackageService::list()`
5. **Query building**: Service calls `apply_filter` from `common/src/db/query.rs` to parse
   the comma-separated string into individual values and generate an `IN` clause
6. **JOIN**: Service adds a JOIN to the `package_license` table using the entity from
   `entity/src/package_license.rs`
7. **Execution**: SeaORM executes the query against PostgreSQL
8. **Output**: Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON

All stages are connected end-to-end. No incomplete paths.

---

## Conventions to Follow

- **Error handling**: Use `Result<T, AppError>` with `.context()` wrapping (per `common/src/error.rs`)
- **Response types**: Return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Use shared filtering via `common/src/db/query.rs` -- do not create new parsing utilities
- **Module pattern**: Follow the `model/ + service/ + endpoints/` structure
- **Testing**: Integration tests in `tests/api/` with real PostgreSQL test database
- **Naming**: Follow `test_<endpoint>_<scenario>` for test functions

---

## Reuse Summary

| Reuse Candidate | Location | How It Is Reused |
|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Called directly in `PackageService::list()` to parse comma-separated license values and generate SQL IN clause -- no new parsing code written |
| Severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | The `Query` struct pattern with an optional filter field is replicated for the license parameter in the package list handler |
| `package_license` entity | `entity/src/package_license.rs` | Used as the SeaORM entity for the JOIN query between `package` and `package_license` tables in the service layer |
