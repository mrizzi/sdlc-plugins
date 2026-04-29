# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value SPDX license filtering. The implementation follows existing patterns already established in the advisory module's severity filter and reuses shared query helpers.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add `license` query parameter extraction and pass it to the service layer.

**Changes**:

- Add an optional `license: Option<String>` field to the `PackageListQuery` struct (or equivalent query-parameter extraction struct), following the same pattern used by `modules/fundamental/src/advisory/endpoints/list.rs` for its `severity` field.
- In the handler function, extract `query.license` and pass it to `PackageService::list()` as a new parameter.
- If the `license` value is present but contains invalid content (e.g., empty segments after splitting on commas), return a `400 Bad Request` via `AppError`. Follow the existing error-handling pattern using `.context()` wrapping and the `AppError` enum from `common/src/error.rs`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Accept the license filter in `PackageService::list()` and apply it to the database query.

**Changes**:

- Add a `license: Option<String>` parameter to the `PackageService::list()` method signature (or accept it within a query/filter struct if one exists).
- When `license` is `Some(value)`:
  - Call `common::db::query::apply_filter` with the raw license string. `apply_filter` already handles parsing comma-separated values and generating a SQL `IN` clause, so no custom parsing is needed.
  - Build a JOIN through `entity::package_license` (the `package_license` SeaORM entity from `entity/src/package_license.rs`) to reach the license column.
  - Apply the filter condition so that only packages whose associated `package_license` row has an SPDX identifier matching one of the provided values are returned.
- When `license` is `None`, the query remains unchanged (no regression on existing behavior).
- Validate the license values before querying. If any segment is empty or malformed after splitting, return an `AppError` that maps to `400 Bad Request`.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests covering all acceptance criteria for the license filter.

**Changes**:

- Create a new integration test file following the conventions in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Seed the test database with packages that have known license associations (e.g., packages with MIT, Apache-2.0, GPL-3.0).
- Implement the following test cases:

  1. **`test_single_license_filter`** -- `GET /api/v2/package?license=MIT` returns only packages with the MIT license.
  2. **`test_multi_license_filter`** -- `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
  3. **`test_no_license_filter`** -- `GET /api/v2/package` (no `license` param) returns all packages unchanged, verifying no regression.
  4. **`test_invalid_license_returns_400`** -- `GET /api/v2/package?license=` or a malformed value returns `StatusCode::BAD_REQUEST`.

- Each test asserts on response status code using `assert_eq!(resp.status(), StatusCode::OK)` (or `BAD_REQUEST` for the error case) and deserializes the body as `PaginatedResults<PackageSummary>` to verify correct content.
- Register the new test module in `tests/api/mod.rs` or the test crate's `Cargo.toml` if required by the project structure.

---

## Files NOT Modified

The following files are explicitly left untouched:

- `entity/src/package_license.rs` -- Already exists and provides the SeaORM entity needed for the JOIN. No changes required.
- `common/src/db/query.rs` -- `apply_filter` already handles comma-separated multi-value parsing and SQL IN clause generation. No changes required.
- `modules/fundamental/src/package/model/summary.rs` -- `PackageSummary` already includes a license field. The response shape is unchanged.
- `modules/fundamental/src/package/endpoints/mod.rs` -- No new routes are being added; the existing `GET /api/v2/package` route is being enhanced, not replaced.
- `server/src/main.rs` -- No new modules or routes to mount.

---

## Implementation Sequence

1. **Modify the endpoint layer** (`list.rs`) -- Add the query parameter struct field and pass it through.
2. **Modify the service layer** (`service/mod.rs`) -- Add filtering logic using `apply_filter` and the `package_license` entity JOIN.
3. **Create integration tests** (`tests/api/package_license_filter.rs`) -- Write and run all four test cases.
4. **Verify** -- Confirm all tests pass, existing tests remain green, and the response shape for `GET /api/v2/package` is unchanged.

---

## How Existing Code Is Reused

| Reuse Candidate | How It Is Used |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in the service layer to parse the comma-separated `license` string and generate the SQL IN clause. No custom parsing or SQL generation is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | The severity filter's `Query` struct pattern (optional field in the query extraction struct, passed to the service) is replicated exactly for the `license` field. The advisory endpoint serves as the structural template. |
| `entity/src/package_license.rs` | The existing SeaORM entity is used in the service layer to construct the JOIN between `package` and `package_license` tables, avoiding raw SQL. |
| `common/src/model/paginated.rs` | `PaginatedResults<PackageSummary>` continues to be the return type. No new response wrapper is needed. |
| `common/src/error.rs` | `AppError` is used for validation errors (invalid license values) mapped to 400 responses, following the existing error-handling pattern. |
