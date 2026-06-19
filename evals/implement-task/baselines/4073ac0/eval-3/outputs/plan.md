# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Project Configuration Validation

- Repository Registry: `trustify-backend` with Serena instance `serena_backend` (rust-analyzer)
- Jira Configuration: Project key TC, Cloud ID present, custom fields configured
- Code Intelligence: Serena instance `serena_backend` available with rust-analyzer

## Target Branch

`main`

## Dependencies

None -- no prerequisite tasks to verify.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Contains the `GET /api/v2/package` handler with a query parameter struct for pagination/sorting but no license filter.

**Changes:**

- **Add `license` field to the query/filter struct**: Following the pattern from `advisory/endpoints/list.rs` where the severity filter uses an `Option<String>` field in the Query struct, add an `Option<String>` field named `license` to the existing query parameter struct used by the package list endpoint.

- **Pass license filter to the service layer**: In the handler function, extract the `license` value from the query struct and pass it to `PackageService::list()`. This follows the same pattern as the advisory list handler passes `severity` to `AdvisoryService::list()`.

- **Validation**: Add validation for the `license` parameter. If present and non-empty, validate that each comma-separated value is a non-empty string. Return `400 Bad Request` (via `AppError`) for invalid values (e.g., empty strings after splitting, malformed input). Follow the existing error handling pattern where all handlers return `Result<T, AppError>` with `.context()` wrapping.

**Reuse:** Follow the exact structural pattern from `advisory/endpoints/list.rs` -- the severity filter implementation is structurally identical. Use the same `Option<String>` query field approach and the same method of forwarding filter values to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries packages with pagination/sorting but no license filtering.

**Changes:**

- **Add `license` parameter to the `list` method signature**: Add an `Option<String>` parameter (or incorporate it into an existing filter/options struct if one exists) for the license filter.

- **Build filter query using `apply_filter`**: When the `license` parameter is `Some`, call `common::db::query::apply_filter` to parse the comma-separated string and generate the appropriate SQL `IN` clause. This function already handles splitting comma-separated values and building `WHERE column IN (...)` clauses -- reuse it directly instead of writing custom parsing logic.

- **JOIN through `package_license` entity**: Use the `entity::package_license` SeaORM entity (from `entity/src/package_license.rs`) to join the `package` table to the `package_license` table when the license filter is active. This follows SeaORM's relation-based join pattern. The join should be:
  - `Package` JOIN `PackageLicense` ON `package.id = package_license.package_id`
  - WHERE `package_license.license` IN (parsed license values)

- **Preserve response shape**: The method must continue returning `PaginatedResults<PackageSummary>`. The license filter only affects which rows are selected, not the response structure. Use `DISTINCT` or equivalent to avoid duplicate packages when a package has multiple licenses matching the filter.

**Reuse:**
  - `common/src/db/query.rs::apply_filter` -- reuse directly for parsing comma-separated license values and generating the SQL IN clause
  - `entity/src/package_license.rs` -- use this existing SeaORM entity for the JOIN query rather than writing raw SQL

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test cases (following conventions from sibling test files like `tests/api/advisory.rs`):**

1. **`test_package_list_filter_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Seeds test packages with different licenses, requests with `?license=MIT`, asserts that all returned items have MIT license. Uses `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into `PaginatedResults<PackageSummary>`. Asserts on specific package identifiers/names, not just count.

2. **`test_package_list_filter_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Seeds packages with MIT, Apache-2.0, and GPL-3.0 licenses. Asserts returned items include MIT and Apache-2.0 packages but exclude GPL-3.0. Validates specific item values.

3. **`test_package_list_no_license_filter`** -- Verifies that `GET /api/v2/package` without the license parameter returns all packages (no regression). Seeds multiple packages with different licenses, requests without filter, asserts all seeded packages are returned.

4. **`test_package_list_filter_invalid_license`** -- Verifies that an invalid license value returns `400 Bad Request`. Sends `GET /api/v2/package?license=` (empty value) and asserts `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.

**Conventions to follow (from sibling test analysis):**
- Test naming: `test_<endpoint>_<scenario>` pattern
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Response validation: validate `total_count`, `items.len()`, and at least one item's key fields
- Error cases: test for expected error status codes
- Each test function gets a `///` doc comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments
- Tests hit a real PostgreSQL test database (integration test pattern)

**Module registration:** Add `mod package_license_filter;` to `tests/api/mod.rs` (or equivalent test module file) so Cargo discovers the test file. If tests are registered via `Cargo.toml` `[[test]]` entries, add the appropriate entry.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` -- add the license filter to the service layer first (data layer changes)
2. Modify `modules/fundamental/src/package/endpoints/list.rs` -- wire the query parameter to the service layer
3. Create `tests/api/package_license_filter.rs` -- write and run integration tests
4. Run `cargo test` to verify all tests pass
5. Run CI checks from `CONVENTIONS.md` if present

## Data-Flow Trace

- **Input**: HTTP query parameter `license` on `GET /api/v2/package` -> extracted by Axum query parameter deserializer in `list.rs`
- **Processing**: `list.rs` handler passes license value to `PackageService::list()` -> service calls `apply_filter` to parse comma-separated values -> SeaORM builds JOIN query through `package_license` entity -> SQL executes against PostgreSQL
- **Output**: Filtered `PaginatedResults<PackageSummary>` returned as JSON response -- same shape as unfiltered response

Path is complete: input (query param) -> processing (parse, filter, query) -> output (JSON response).

## Scope Boundaries

- Only the files listed in Files to Modify and Files to Create are touched
- No changes to the response shape (`PaginatedResults<PackageSummary>`)
- No changes to existing endpoints or other modules
- No new utility functions that duplicate `apply_filter` functionality
- No database migrations needed (the `package_license` table already exists)
