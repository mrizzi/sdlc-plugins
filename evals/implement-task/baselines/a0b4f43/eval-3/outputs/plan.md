# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing patterns and utilities throughout -- no new parsing or filtering utility code is written.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter extraction and wire it into the service call.

**Changes**:

- Add an `Option<String>` field named `license` to the query parameters struct (the `Query` extractor struct used by the list handler). This follows the exact same pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs` -- an optional string field on the query struct that Axum deserializes from the query string automatically.
- In the handler function, pass the extracted `license` value through to `PackageService::list()` as an additional parameter.
- No new parsing logic is written here. The raw `Option<String>` value is passed directly to the service layer, which delegates parsing to `apply_filter` from `common/src/db/query.rs`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Accept the license filter in `PackageService::list()` and apply it to the database query.

**Changes**:

- Extend the `list` method signature to accept an additional parameter: `license: Option<String>`.
- When `license` is `Some(value)`, use `common::db::query::apply_filter` to parse the comma-separated string and generate the appropriate SQL `IN` clause condition. `apply_filter` already handles both single values (`MIT`) and multi-value comma-separated inputs (`MIT,Apache-2.0`) -- reuse it directly rather than writing any new parsing logic.
- Use the `entity::package_license::Entity` (from `entity/src/package_license.rs`) to construct a JOIN from the `package` table to the `package_license` table. This leverages SeaORM's relation definitions already present on the `package_license` entity rather than writing raw SQL joins.
- Apply the filter condition produced by `apply_filter` to the `package_license` table's license identifier column within the JOIN.
- When `license` is `None`, skip the JOIN and filter entirely, preserving the existing behavior (no regression).
- Return a `400 Bad Request` (via `AppError`) if the license value is present but contains invalid/empty segments after parsing.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests validating the license filter behavior against a real PostgreSQL test database.

**Test cases** (following the existing pattern in `tests/api/advisory.rs` and `tests/api/sbom.rs`):

1. **Single license filter**: `GET /api/v2/package?license=MIT` -- assert response status is 200, assert all returned `PackageSummary` items have license `MIT`, assert packages with other licenses are excluded.
2. **Comma-separated multi-value filter**: `GET /api/v2/package?license=MIT,Apache-2.0` -- assert response status is 200, assert returned packages have license matching either `MIT` or `Apache-2.0`.
3. **No filter (regression test)**: `GET /api/v2/package` without a `license` parameter -- assert response status is 200, assert all packages are returned, assert response shape (`PaginatedResults<PackageSummary>`) is unchanged.
4. **Invalid license value**: `GET /api/v2/package?license=` (empty string) -- assert response status is 400 Bad Request.

---

## Reuse Strategy

This plan does not introduce any new utility functions for parsing or filtering. All filtering logic is delegated to existing code:

| Existing Code | How It Is Reused |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in `PackageService::list()` to parse the comma-separated `license` string and generate the SQL `IN` clause. No new parsing logic is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as the structural template: the `severity` optional field on the advisory Query struct is mirrored by adding a `license` optional field on the package Query struct. The handler-to-service parameter passing follows the same pattern. |
| `entity/src/package_license.rs` | The existing `package_license` SeaORM entity is used to construct the JOIN between the `package` table and the `package_license` table, using SeaORM relation definitions rather than raw SQL. |

No files outside the scope defined above are modified or created.
