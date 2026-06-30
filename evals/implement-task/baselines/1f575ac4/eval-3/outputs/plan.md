# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses existing query infrastructure and follows established patterns from the advisory module.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint.

**Changes**:
- Add an optional `license: Option<String>` field to the `PackageListQuery` struct (or equivalent query parameters struct), following the same pattern used for the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, when the `license` parameter is present, pass it through to `PackageService::list()` as a filter argument.
- No new parsing logic is needed here — the raw query parameter string (e.g., `"MIT,Apache-2.0"`) is passed to the service layer, which delegates comma-separated parsing to `apply_filter` from `common/src/db/query.rs`.
- Return `400 Bad Request` via `AppError` when the license value is present but contains invalid/empty segments, consistent with existing error handling conventions.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService::list` method.

**Changes**:
- Update the `list` method signature to accept an optional license filter parameter (e.g., `license_filter: Option<&str>`).
- When the license filter is provided, use `common::db::query::apply_filter` to parse the comma-separated string and generate the SQL `IN` clause condition. This reuses the exact same mechanism the advisory module uses for severity filtering — `apply_filter` already handles splitting on commas, trimming whitespace, and producing the appropriate SeaORM condition.
- Join through the `entity::package_license` entity (from `entity/src/package_license.rs`) to connect packages to their license records. Use the existing SeaORM entity relation rather than writing raw SQL or creating a new entity. The join uses `PackageLicense`'s defined `Relation` to `Package` to build the query with `.join()` or `.find_also_related()`.
- Apply the filter condition produced by `apply_filter` to the `license` column of the `package_license` table within the joined query.
- When no license filter is provided, skip the join and filter entirely, preserving the existing behavior (no regression).

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license filter functionality.

**Changes**:
- Follow the same test structure used in `tests/api/advisory.rs` for consistency.
- Seed the test database with packages associated with known licenses (e.g., MIT, Apache-2.0, GPL-3.0).
- Test cases:
  1. **Single license filter**: `GET /api/v2/package?license=MIT` returns only MIT-licensed packages. Assert response status is 200 and the returned `PaginatedResults<PackageSummary>` contains only matching entries.
  2. **Comma-separated multi-value filter**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license. Verify the union semantics (OR, not AND).
  3. **No license filter (regression)**: `GET /api/v2/package` without the `license` parameter returns all packages, confirming no behavioral change to the existing endpoint.
  4. **Invalid license value**: `GET /api/v2/package?license=` (empty) or malformed value returns `400 Bad Request`.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with existing API tests.

## Reuse Strategy

This implementation creates **no new utility functions** for query parameter parsing or SQL clause generation. All parsing and filtering logic is handled by existing infrastructure:

| Need | Reused From | How |
|---|---|---|
| Comma-separated parameter parsing and SQL IN clause | `common/src/db/query.rs::apply_filter` | Called directly with the raw `license` query string |
| Endpoint/query struct pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Followed as structural template for adding the optional field |
| Package-to-license JOIN | `entity/src/package_license.rs` | Used as SeaORM entity for the join rather than raw SQL |

## Scope Verification

All files listed above are within the scope defined by the task:
- **Files to Modify**: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` (both listed in task)
- **Files to Create**: `tests/api/package_license_filter.rs` (listed in task)

No out-of-scope files are modified or created.
