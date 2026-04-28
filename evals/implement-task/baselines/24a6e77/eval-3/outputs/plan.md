# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering, following the established filter pattern already used by the advisory module.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter to the package list endpoint handler.

**Changes**:

- Add an optional `license: Option<String>` field to the `Query` struct used for parameter extraction (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, pass the extracted `license` value through to `PackageService::list()` so the service layer can apply the filter.
- No new parsing logic is written here. The raw `Option<String>` is forwarded to the service layer, which delegates to `apply_filter` from `common/src/db/query.rs` for comma-separated parsing and SQL IN clause generation.
- Return `400 Bad Request` (via `AppError`) if the license value fails validation, consistent with existing error handling conventions.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Apply the license filter in the `PackageService::list` method's database query.

**Changes**:

- Update the `list` method signature to accept an additional `license: Option<String>` parameter.
- When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate the appropriate SQL IN clause condition. This reuses the exact same function that other modules (e.g., advisory severity filtering) already rely on -- no new parsing or filtering utility is created.
- JOIN through the `entity::package_license` entity (from `entity/src/package_license.rs`) to connect the `package` table to the license data. Use SeaORM's relation definitions already present on the entity rather than writing raw SQL.
- Apply the filter condition to the existing query builder chain so it composes with pagination and sorting that are already handled.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests verifying the license filter behavior end-to-end.

**Test cases**:

1. **Single license filter**: `GET /api/v2/package?license=MIT` -- assert the response contains only packages with the MIT license and the response shape is `PaginatedResults<PackageSummary>`.
2. **Comma-separated multi-value filter**: `GET /api/v2/package?license=MIT,Apache-2.0` -- assert the response contains packages matching either license.
3. **No license filter (regression)**: `GET /api/v2/package` with no `license` parameter -- assert all packages are returned unchanged, confirming no regression.
4. **Invalid license value**: `GET /api/v2/package?license=` or with an otherwise invalid value -- assert a `400 Bad Request` response.

**Conventions followed**:

- Tests hit a real PostgreSQL test database, consistent with existing tests in `tests/api/`.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in sibling test files (`sbom.rs`, `advisory.rs`).

---

## Reuse Strategy Summary

| Reuse Candidate | How It Is Applied |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in `PackageService::list` to parse comma-separated license values and generate the SQL IN clause. No new parsing or filter utility is created. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as the structural template for adding the `license` field to the package `Query` struct and wiring it through to the service layer. |
| `entity/src/package_license.rs` | Used for the SeaORM JOIN between `package` and the license data, avoiding raw SQL. |

---

## Scope Containment

All modifications and new files fall strictly within the boundaries declared by the task:

- **Modified**: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs`
- **Created**: `tests/api/package_license_filter.rs`

No other files are touched. No new utility functions, helper modules, or shared code is introduced -- existing shared infrastructure (`apply_filter`, `package_license` entity) is reused as-is.
