# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering by SPDX license identifier.

## Repository

trustify-backend

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** This file implements the `GET /api/v2/package` list endpoint handler. It accepts query parameters for pagination and possibly sorting, but does not currently accept a `license` filter parameter.

**Changes:**

1. **Add `license` field to the Query struct:** Following the pattern established in `modules/fundamental/src/advisory/endpoints/list.rs` (the advisory severity filter), add an optional `license` field to the endpoint's `Query` struct:
   ```rust
   /// Optional license filter. Supports single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Extract and validate the license parameter:** In the handler function, extract the `license` value from the query parameters. If the value is present but empty or contains invalid characters, return a `400 Bad Request` response using the `AppError` enum from `common/src/error.rs`.

3. **Pass the license filter to the service layer:** After extraction and validation, pass the `license` parameter to `PackageService::list()` so the service layer can apply the database filter. This mirrors how the advisory endpoint passes its `severity` filter to `AdvisoryService::list()`.

4. **Reuse `apply_filter` from `common/src/db/query.rs`:** Call the `apply_filter` function to handle comma-separated multi-value parsing and SQL `IN` clause generation. This function already handles the pattern of splitting comma-separated strings and building the appropriate query condition.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** This file contains `PackageService` with `fetch` and `list` methods. The `list` method queries the `package` table and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` filter parameter to the `list` method signature:** Add an `Option<String>` parameter (or a dedicated filter struct) to the `list` method:
   ```rust
   /// List packages, optionally filtered by license SPDX identifier(s).
   pub async fn list(
       &self,
       // ... existing params (pagination, sorting, etc.)
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Build the JOIN query:** When the `license` parameter is present, join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their declared license. Use SeaORM's query builder to construct the join:
   ```rust
   // When license filter is provided:
   // JOIN package_license ON package.id = package_license.package_id
   // WHERE package_license.license IN (parsed_values)
   ```

3. **Apply the filter using `apply_filter`:** Use the `apply_filter` function from `common/src/db/query.rs` to parse the comma-separated license string and generate the SQL `IN` clause against the `package_license` table's license column.

4. **Preserve response shape:** Ensure the return type remains `PaginatedResults<PackageSummary>` -- the license filter only constrains which packages are returned, it does not change the response structure.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on `GET /api/v2/package`.

**Structure:** Follow the conventions established in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
- Deserialize response body and validate `PaginatedResults<PackageSummary>` fields
- Use the naming convention `test_<endpoint>_<scenario>`

**Test functions:**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200, only MIT-licensed packages are returned, assert on specific package names/identifiers (not just count)

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200, packages with MIT or Apache-2.0 licenses are returned, GPL-3.0 packages are excluded, assert on specific package identifiers

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200, all packages are returned, total count matches expected, response shape is `PaginatedResults<PackageSummary>`

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Test database with packages
   - When: `GET /api/v2/package?license=` (empty value or invalid characters)
   - Then: Response status is 400 Bad Request

**Additional considerations:**
- Each test with distinct setup/action/assertion phases includes `// Given`, `// When`, `// Then` section comments
- Register the new test file in `tests/Cargo.toml` if the test harness requires explicit module registration

## Module Registration

The new test file `tests/api/package_license_filter.rs` may need to be registered in `tests/Cargo.toml` or a `tests/api/mod.rs` file (depending on how the test harness discovers test files). Check the existing test module structure to determine the registration pattern.

## API Changes

| Endpoint | Change Type | Description |
|---|---|---|
| `GET /api/v2/package?license=MIT` | MODIFY | Add optional `license` query parameter for single-value filtering |
| `GET /api/v2/package?license=MIT,Apache-2.0` | MODIFY | Support comma-separated license values for multi-value filtering |

The response shape (`PaginatedResults<PackageSummary>`) remains unchanged. Only the input accepts a new optional parameter.

## Conventions to Follow

Based on the repository's key conventions:
- **Framework:** Axum for HTTP, SeaORM for database
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types:** List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers:** Shared filtering via `common/src/db/query.rs` -- use `apply_filter` rather than writing custom parsing
- **Testing:** Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` -> extract `license` query param in endpoint handler (list.rs) -> validate parameter -> pass to `PackageService::list()` (service/mod.rs) -> build SeaORM query with JOIN on `package_license` table -> apply `apply_filter` for IN clause -> execute query -> return `PaginatedResults<PackageSummary>` -> serialize response -- **COMPLETE**

## Verification Steps

1. Run `cargo test` to ensure all new and existing tests pass
2. Run `cargo build` to verify compilation
3. Run any CI checks specified in `CONVENTIONS.md` (if present)
4. Verify `git diff --name-only` matches the expected file list
5. Check for no sensitive patterns in staged diff
