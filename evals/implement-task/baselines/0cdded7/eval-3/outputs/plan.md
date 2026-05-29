# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that supports single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering of packages by their declared SPDX license identifier.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter extraction and pass it through to the service layer.

**Changes**:

- **Add a `license` field to the query parameter struct**: Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` where the advisory list endpoint defines a Query struct with optional filter fields (e.g., `severity`), add an `Option<String>` field named `license` to the existing query parameters struct for the package list endpoint. This field will capture the raw query string value (e.g., `"MIT"` or `"MIT,Apache-2.0"`).

- **Pass the license filter to the service method**: In the handler function, pass `query.license` to `PackageService::list()` as an additional parameter. No parsing of the comma-separated string is done here -- that responsibility belongs to `apply_filter` in the service/query layer.

- **Validation**: If the `license` parameter is present but empty (e.g., `?license=`), return a `400 Bad Request` using the existing `AppError` enum from `common/src/error.rs`. Follow the same validation pattern used for the severity parameter in the advisory list endpoint.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService::list` method.

**Changes**:

- **Accept a new `license` filter parameter**: Add an `Option<String>` parameter (or extend the existing filter/query struct if one is used) to the `list` method signature to receive the license filter value.

- **Join to the `package_license` table using the existing entity**: Use `entity::package_license` (from `entity/src/package_license.rs`) to construct a SeaORM JOIN between the `package` table and the `package_license` table. This is the existing entity for the package-license relationship -- no raw SQL or new entity is needed.

- **Apply the filter using `common/src/db/query.rs::apply_filter`**: Call `apply_filter` with the license parameter value. `apply_filter` already handles:
  - Splitting comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
  - Generating the appropriate SQL `IN` clause for multi-value filters
  - Returning the correct single-value `=` condition for single values
  - This avoids writing any new parsing or SQL generation logic.

- **Conditional application**: Only apply the license filter when the `license` parameter is `Some`. When `None`, the query returns all packages unchanged (no regression).

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests verifying the license filter behavior.

**Test cases**:

1. **Single license filter** (`GET /api/v2/package?license=MIT`):
   - Seed the test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0).
   - Assert the response status is 200.
   - Assert the returned `PaginatedResults<PackageSummary>` contains only packages with MIT license.
   - Assert the response shape (pagination fields, summary structure) is unchanged.

2. **Comma-separated multi-value filter** (`GET /api/v2/package?license=MIT,Apache-2.0`):
   - Using the same seeded data, request with two license values.
   - Assert the response contains packages matching either MIT or Apache-2.0.
   - Assert GPL-3.0 packages are excluded.

3. **No license filter** (`GET /api/v2/package`):
   - Request without the `license` parameter.
   - Assert all seeded packages are returned (no regression).
   - Assert response shape is unchanged from baseline.

4. **Invalid license value** (`GET /api/v2/package?license=`):
   - Request with an empty license parameter.
   - Assert 400 Bad Request is returned.

**Test conventions**: Follow the existing integration test pattern from `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Use a real PostgreSQL test database.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns.
- Deserialize response bodies into `PaginatedResults<PackageSummary>` for assertion.

## Files NOT modified

The following files are explicitly out of scope per the task definition:

- `entity/src/package_license.rs` -- used as-is; no modifications needed.
- `common/src/db/query.rs` -- used as-is; `apply_filter` already provides the needed functionality.
- `modules/fundamental/src/package/endpoints/mod.rs` -- no route registration changes needed since the endpoint path (`GET /api/v2/package`) is unchanged; only its accepted query parameters change.
- `modules/fundamental/src/package/model/summary.rs` -- the `PackageSummary` response struct already includes a `license` field; no changes needed.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` -- add the license filter to the service layer first since the endpoint depends on it.
2. Modify `modules/fundamental/src/package/endpoints/list.rs` -- add the query parameter and wire it to the service.
3. Create `tests/api/package_license_filter.rs` -- write and run integration tests to validate behavior.
