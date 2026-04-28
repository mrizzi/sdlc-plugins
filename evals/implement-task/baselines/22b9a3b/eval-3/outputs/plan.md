# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the existing advisory severity filter pattern and reuses shared query helpers.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add `license` query parameter extraction and pass it to the service layer.

**Changes**:
- Add an optional `license: Option<String>` field to the `PackageListQuery` struct (or equivalent query extraction struct), mirroring how the advisory `list.rs` defines its `severity` query parameter field.
- In the handler function, extract the `license` value from the query struct and pass it to `PackageService::list()` as a new parameter.
- Add input validation: if `license` is provided but contains empty segments or invalid characters after splitting on commas, return a `400 Bad Request` via `AppError`.
- No changes to the response shape -- the handler continues to return `PaginatedResults<PackageSummary>`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Accept the license filter in `PackageService::list()` and apply it to the database query.

**Changes**:
- Update the `list` method signature to accept an additional `license: Option<String>` parameter.
- When `license` is `Some(value)`, call `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate a SQL `WHERE ... IN (...)` clause.
- The filter joins through the `package_license` entity (`entity/src/package_license.rs`) to match packages whose associated license SPDX identifier is in the provided set.
- Use SeaORM's relation/join API (consistent with how other join-table filters work in the codebase) rather than writing raw SQL.
- When `license` is `None`, no additional filter is applied -- existing behavior is preserved.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license query parameter.

**Changes**:
- Follow the same test structure used in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Set up test data: insert packages with known licenses (e.g., MIT, Apache-2.0, GPL-3.0) into the test PostgreSQL database.
- **Test cases**:
  1. **Single license filter**: `GET /api/v2/package?license=MIT` -- assert response status is 200, assert only MIT-licensed packages are returned.
  2. **Multi-value license filter**: `GET /api/v2/package?license=MIT,Apache-2.0` -- assert response status is 200, assert packages with either MIT or Apache-2.0 are returned, GPL-3.0 packages are excluded.
  3. **No filter (regression)**: `GET /api/v2/package` -- assert response status is 200, assert all packages are returned regardless of license.
  4. **Invalid license value**: `GET /api/v2/package?license=` (empty string) or a value containing invalid characters -- assert response status is 400.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with existing tests.
- Verify the response body deserializes to `PaginatedResults<PackageSummary>` and check the `total` count and individual item licenses.

### 4. Update `tests/Cargo.toml` (minor modification)

- If `package_license_filter.rs` needs to be registered as a test module, add a `[[test]]` entry or ensure the module is included via `mod` declaration in the test harness. This depends on the existing test organization -- if tests are auto-discovered via the `tests/api/` directory convention, no change is needed.

---

## Approach Summary

| Step | Action | Files |
|------|--------|-------|
| 1 | Add `license` field to query extraction struct | `package/endpoints/list.rs` |
| 2 | Add validation for the license parameter | `package/endpoints/list.rs` |
| 3 | Pass license filter to service layer | `package/endpoints/list.rs` |
| 4 | Accept license param and apply filter using `apply_filter` + `package_license` join | `package/service/mod.rs` |
| 5 | Write integration tests | `tests/api/package_license_filter.rs` |
| 6 | Run `cargo test` and `cargo clippy` to verify | -- |

---

## Reuse Strategy

All filtering logic is built on existing infrastructure rather than writing new helpers:

- **`apply_filter`** from `common/src/db/query.rs` handles the comma-separated parsing and SQL IN clause generation -- no custom parsing code needed.
- **Advisory severity filter pattern** from `modules/fundamental/src/advisory/endpoints/list.rs` provides the exact structural template: an optional field on the query struct, extraction in the handler, and delegation to the service layer.
- **`package_license` entity** from `entity/src/package_license.rs` provides the SeaORM entity for the join table, avoiding any raw SQL for the package-to-license relationship.
- **`PaginatedResults<T>`** from `common/src/model/paginated.rs` is already used by the package list endpoint and remains unchanged.
- **`AppError`** from `common/src/error.rs` is used for the 400 Bad Request validation error, consistent with how other endpoints handle input validation.

No new utility functions or helper modules are created. The implementation is purely compositional, assembling existing building blocks.
