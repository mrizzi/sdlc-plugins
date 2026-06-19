# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What to change:**

- Add an optional `license: Option<String>` field to the query parameters struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, extract the `license` query parameter and pass it to the `PackageService::list` method.
- Reuse `common/src/db/query.rs::apply_filter` to parse the comma-separated license string into individual values and generate the appropriate SQL `IN` clause. Do NOT write custom parsing or splitting logic -- `apply_filter` already handles comma-separated multi-value parameters.
- Add validation: if the `license` parameter is present but contains empty or invalid values, return a `400 Bad Request` using the existing `AppError` pattern from `common/src/error.rs`.

**Reuse applied:**
- Follow the filter pattern from `modules/fundamental/src/advisory/endpoints/list.rs` -- the advisory list endpoint's `severity` query parameter uses the identical Query struct pattern with an optional filter field, and the same `apply_filter` invocation approach.
- Call `apply_filter` from `common/src/db/query.rs` directly for comma-separated parsing and SQL IN clause generation.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What to change:**

- Add a `license: Option<String>` parameter (or embed it in an existing filter/query struct) to the `PackageService::list` method signature.
- When the `license` filter is present, build a JOIN query through `entity/src/package_license.rs` (the `package_license` entity/table) to filter packages by their associated license SPDX identifiers.
- Use SeaORM's query builder with the `package_license` entity for the JOIN, rather than writing raw SQL. The `package_license` entity already maps the package-to-license relationship and provides the column definitions needed for the join condition and filter.
- Apply `apply_filter` from `common/src/db/query.rs` to handle the comma-separated license values, generating an `IN` clause against the license identifier column in the `package_license` table.
- When no `license` parameter is provided, the query remains unchanged (no JOIN, no filter) to avoid regression.

**Reuse applied:**
- Use `entity/src/package_license.rs` for the JOIN query -- this entity already defines the package-license join table schema, columns, and relations. No new entity or raw SQL is needed.
- Use `apply_filter` from `common/src/db/query.rs` for the filter clause generation.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**What to create:**

Integration tests for the license filter feature. Following the test conventions observed in sibling test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`):

- **`test_list_packages_filter_single_license`**: Seed test packages with different licenses. Call `GET /api/v2/package?license=MIT`. Assert response status is `200 OK`. Assert that all returned packages have the MIT license. Assert on specific package values, not just count.
- **`test_list_packages_filter_multi_license`**: Seed packages with MIT, Apache-2.0, and GPL-3.0 licenses. Call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert that returned packages match either MIT or Apache-2.0. Assert that GPL-3.0 packages are excluded.
- **`test_list_packages_no_license_filter`**: Call `GET /api/v2/package` without the license parameter. Assert that all seeded packages are returned unchanged (no regression).
- **`test_list_packages_invalid_license`**: Call `GET /api/v2/package?license=` (empty value) or with an invalid format. Assert response status is `400 Bad Request`.

Each test function will have a `///` doc comment explaining what it verifies, and non-trivial tests will use `// Given`, `// When`, `// Then` section comments.

Tests will use `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with sibling tests, and will validate specific field values in the response body rather than just collection lengths.

**Additional integration:**
- Register the new test file in `tests/Cargo.toml` or the test module root as needed, following the pattern used by existing test files.

## Changes NOT Made

- **No new utility functions** for parsing comma-separated values. The existing `apply_filter` in `common/src/db/query.rs` already handles this. Creating a new parser would duplicate its functionality.
- **No changes to the response shape**. `PaginatedResults<PackageSummary>` remains unchanged.
- **No changes to other endpoints**. Only the package list endpoint is modified.
- **No new entity files**. The existing `entity/src/package_license.rs` provides everything needed for the JOIN.

## Data Flow

1. **Input**: HTTP request arrives at `GET /api/v2/package?license=MIT,Apache-2.0`
2. **Parameter extraction**: `list.rs` handler extracts the optional `license` query parameter from the request
3. **Parsing**: `apply_filter` from `common/src/db/query.rs` parses the comma-separated string into individual license values
4. **Query building**: `PackageService::list` in `service/mod.rs` builds a SeaORM query that JOINs `package` with `package_license` (using `entity/src/package_license.rs`) and applies an `IN` clause on the license identifier column
5. **Execution**: Query executes against PostgreSQL, returning only matching packages
6. **Response**: Results are wrapped in `PaginatedResults<PackageSummary>` and returned -- same shape as before
