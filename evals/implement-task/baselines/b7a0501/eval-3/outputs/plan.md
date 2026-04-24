# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support single-value and comma-separated multi-value filtering. The implementation follows the existing severity filter pattern from the advisory list endpoint and reuses the shared `apply_filter` helper from `common/src/db/query.rs`.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests, extracts query parameters, calls `PackageService::list`, returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Add `license` field to the `Query` struct**: Following the same pattern used by the advisory list endpoint's `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`, add an `Option<String>` field named `license` to the existing `Query` struct (or equivalent query-parameter extraction struct). This field captures the raw query string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

- **Pass the license filter to the service layer**: When calling `PackageService::list`, pass the extracted `license` value (the `Option<String>`) down to the service method. This mirrors how the advisory endpoint passes the `severity` parameter to `AdvisoryService::list`.

- **Validation**: Add validation that checks the license value is non-empty when present. If the `license` parameter is present but contains an empty or whitespace-only string, return a `400 Bad Request` using `AppError`. Follow the existing error-handling convention of `Result<T, AppError>` with `.context()` wrapping.

**Reuse:**
- Structurally mirror the `Query` struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate #2).
- No new query-parameter parsing logic needed; the raw string is passed to the service layer where `apply_filter` handles parsing.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with `fetch` and `list` methods. The `list` method builds a database query, applies existing filters (pagination, sorting), and returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Accept `license` parameter**: Add an `Option<String>` parameter named `license` to the `list` method signature (or to an existing query/filter struct if the service uses one).

- **Join with `package_license` entity**: When the `license` filter is `Some`, add a JOIN to the `package_license` table using the `package_license` SeaORM entity from `entity/src/package_license.rs` (Reuse Candidate #3). Use SeaORM's `.join()` or `.find_also_related()` to join `package` to `package_license` on the foreign key relationship defined in the entity.

- **Apply the filter using `apply_filter`**: Call `apply_filter` from `common/src/db/query.rs` (Reuse Candidate #1), passing the raw license string value and the `package_license` column that stores the SPDX identifier. `apply_filter` handles:
  - Splitting comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
  - Generating the appropriate SQL `IN` clause for multi-value filtering
  - Generating a simple `=` clause for single-value filtering

- **Preserve response shape**: The return type `PaginatedResults<PackageSummary>` remains unchanged. The JOIN is only used for filtering; the SELECT projection stays the same.

**Reuse:**
- `common/src/db/query.rs::apply_filter` (Reuse Candidate #1) -- reused directly, no wrapper or new utility needed.
- `entity/src/package_license.rs` (Reuse Candidate #3) -- the existing SeaORM entity provides the table/column definitions for the JOIN and WHERE clause.
- The overall pattern of conditionally joining and filtering follows the advisory severity filter pattern (Reuse Candidate #2).

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license query parameter on `GET /api/v2/package`.

**Structure:** Follow the existing test conventions from sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases.
- Test naming follows `test_<endpoint>_<scenario>` pattern.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

**Test cases:**

1. **`test_list_packages_filter_single_license`**
   - Seed test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0).
   - `GET /api/v2/package?license=MIT`
   - Assert response status is 200.
   - Assert returned items all have `license == "MIT"`.
   - Assert specific expected packages are present (value-based assertion, not just count).

2. **`test_list_packages_filter_comma_separated_licenses`**
   - Seed test database with packages having different licenses.
   - `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert response status is 200.
   - Assert returned items have license matching either `"MIT"` or `"Apache-2.0"`.
   - Assert GPL-3.0 packages are excluded.

3. **`test_list_packages_no_license_filter`**
   - Seed test database with packages having different licenses.
   - `GET /api/v2/package` (no license parameter).
   - Assert response status is 200.
   - Assert all seeded packages are returned (no regression).
   - Assert response shape is `PaginatedResults<PackageSummary>`.

4. **`test_list_packages_invalid_license_returns_400`**
   - `GET /api/v2/package?license=` (empty value) or with invalid characters.
   - Assert response status is 400.

**Module registration:** The new test file needs to be registered in `tests/api/mod.rs` (or `tests/Cargo.toml` depending on the test harness configuration). If `tests/api/` uses a `mod.rs` file, add `mod package_license_filter;`.

---

## Integration Points

- **Route registration**: No changes needed to `modules/fundamental/src/package/endpoints/mod.rs` -- the route for `GET /api/v2/package` already exists and points to `list.rs`. The handler signature change (accepting the new query parameter) is transparent to the router since Axum extracts query parameters via the `Query` extractor struct.

- **Entity imports**: `modules/fundamental/src/package/service/mod.rs` needs to import `entity::package_license` to use it in the JOIN clause.

- **Common imports**: `modules/fundamental/src/package/service/mod.rs` needs to import `common::db::query::apply_filter` for the filter application.

---

## What is NOT changed

- Response shape (`PaginatedResults<PackageSummary>`) -- unchanged.
- Existing query parameters (pagination, sorting) -- unchanged.
- Other endpoints (`GET /api/v2/package/{id}`) -- unchanged.
- Entity definitions -- no new entities or migrations required.
- `common/src/db/query.rs` -- not modified, only consumed.
