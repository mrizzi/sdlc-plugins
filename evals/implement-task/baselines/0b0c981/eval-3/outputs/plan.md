# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Supports single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the identical pattern used by the advisory severity filter.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint's query struct and wire it into the service call.

**Changes**:

1. **Add `license` field to the `Query` struct** (or equivalent query-parameters struct used for deserialization):
   - Add `pub license: Option<String>` field, following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
   - Apply the same `#[serde(default)]` attribute to make it optional.

2. **Pass the license filter to the service layer**:
   - In the handler function for `GET /api/v2/package`, extract `query.license` and pass it to `PackageService::list()` (or the equivalent service method).
   - This mirrors how the advisory list endpoint passes its `severity` filter to the advisory service.

3. **Validation**: If the endpoint pattern validates query parameters before passing them to the service, add validation for the `license` parameter. Invalid/empty segments after splitting on commas should result in a 400 Bad Request response. If validation is handled downstream (in `apply_filter` or the service), no additional validation code is needed here — follow whichever pattern the advisory severity filter uses.

**Conventions to follow**:
- Match the exact struct field ordering and serde attribute style from the advisory `Query` struct.
- Use the same `Option<String>` type (not `Vec<String>`) since `apply_filter` in `common/src/db/query.rs` handles the comma-separated parsing internally.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService` list method.

**Changes**:

1. **Add `license` parameter to the `list` method signature**:
   - Add an `Option<String>` parameter (or add a field to an existing filter/options struct if the method uses one) for the license filter.
   - Follow the same parameter pattern used by the advisory service's list method for the severity filter.

2. **Apply the license filter to the database query**:
   - Import `entity::package_license` (the entity from `entity/src/package_license.rs`).
   - When `license` is `Some(value)`:
     - Join the main package query with the `package_license` table using the package ID foreign key.
     - Call `apply_filter` from `common/src/db/query.rs` to handle parsing the comma-separated values and generating the appropriate SQL `IN` clause (or equality check for single values) against the license SPDX identifier column in the `package_license` entity.
   - When `license` is `None`: skip the join and filter entirely (existing behavior, no regression).

3. **Error handling**:
   - If `apply_filter` returns an error for invalid license values, propagate it as `AppError::BadRequest` (or the equivalent error type used in the codebase) so the endpoint returns 400.

**Conventions to follow**:
- Use SeaORM/Diesel query builder methods consistent with the rest of the service layer (whichever ORM the project uses).
- Do not write raw SQL — use the entity and `apply_filter` helper.
- Ensure the join does not produce duplicate results; apply `.distinct()` if the advisory severity filter does the same when joining through a many-to-many table.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests verifying the license filter behavior end-to-end.

**Changes**:

1. **Test: single license filter** (`test_single_license_filter`):
   - Seed the test database with packages having different licenses (e.g., MIT, Apache-2.0, GPL-3.0).
   - Call `GET /api/v2/package?license=MIT`.
   - Assert response status is 200.
   - Assert every returned `PackageSummary` has license == "MIT".
   - Assert packages with other licenses are not included.

2. **Test: comma-separated license filter** (`test_multi_license_filter`):
   - Seed the test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - Call `GET /api/v2/package?license=MIT,Apache-2.0`.
   - Assert response status is 200.
   - Assert returned packages have licenses that are either MIT or Apache-2.0.
   - Assert GPL-3.0 packages are excluded.

3. **Test: no license filter (no regression)** (`test_no_license_filter`):
   - Seed the test database with packages having various licenses.
   - Call `GET /api/v2/package` (no license parameter).
   - Assert response status is 200.
   - Assert all seeded packages are returned (same behavior as before the change).

4. **Test: invalid license value returns 400** (`test_invalid_license_value`):
   - Call `GET /api/v2/package?license=` (empty value) or with a clearly invalid value (depending on how validation is implemented).
   - Assert response status is 400 Bad Request.

**Conventions to follow**:
- Follow the test setup and teardown patterns in `tests/api/advisory.rs` (database seeding, HTTP client setup, assertion style).
- Use the same test helper infrastructure (test server, fixtures) used by existing API tests.
- Register the new test file in `tests/api/mod.rs` (if a module declaration is required).

## Additional file that may need modification

### 4. `tests/api/mod.rs` (if it exists)

If the test directory uses a `mod.rs` to declare submodules, add `mod package_license_filter;` to register the new test file. Follow the existing pattern for how `advisory.rs` and `search.rs` are declared.

## Execution Order

1. Modify `modules/fundamental/src/package/service/mod.rs` — add the license filter logic to the service layer first (this is the core change).
2. Modify `modules/fundamental/src/package/endpoints/list.rs` — add the query parameter and wire it to the service.
3. Create `tests/api/package_license_filter.rs` — write integration tests.
4. Update `tests/api/mod.rs` if needed — register the test module.

## Response Shape Verification

The `PaginatedResults<PackageSummary>` response type is not modified. The filter is applied at the query level before results are paginated and serialized. The only change to the API contract is the addition of an optional input parameter.

## Risk Assessment

- **Low risk**: The change adds an optional parameter; omitting it preserves existing behavior.
- **Distinct results**: The join through `package_license` could produce duplicates if a package has multiple license entries. The implementation must use `.distinct()` or equivalent deduplication.
- **Performance**: The join is on indexed foreign keys (package ID) and the license column should be indexed. No performance concern for typical dataset sizes.
