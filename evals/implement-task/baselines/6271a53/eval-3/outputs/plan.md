# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation follows the existing severity filter pattern from the advisory list endpoint and reuses shared query infrastructure.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add `license` query parameter extraction and pass it to the service layer.

**Changes**:

- **Add `license` field to the `Query` struct** (or equivalent query-params struct used for deserialization). Follow the exact pattern used in `modules/fundamental/src/advisory/endpoints/list.rs` where the `severity` field is declared as an `Option<String>` in the advisory Query struct. Add:
  ```rust
  /// Filter by SPDX license identifier. Supports comma-separated values.
  pub license: Option<String>,
  ```

- **Pass the `license` parameter to the service method**. In the handler function that processes `GET /api/v2/package`, extract `query.license` and forward it to `PackageService::list()` (or the equivalent list/fetch method). This mirrors how the advisory endpoint extracts `query.severity` and passes it to its service method.

- **No changes to the response shape**. The return type (`PaginatedResults<PackageSummary>`) remains unchanged; only the input query parameters are extended.

**Reuse**: Follow the identical Query struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate 2). The field declaration, deserialization, and forwarding to the service layer should be structurally identical to how `severity` is handled there.

---

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the PackageService list method.

**Changes**:

- **Add a `license` parameter** to the list method signature (e.g., `license: Option<String>`) or extend whatever filter/options struct is passed to it, consistent with how the advisory service accepts `severity`.

- **Apply the filter using `apply_filter` from `common/src/db/query.rs`**. When the `license` parameter is `Some(value)`:
  1. Call `apply_filter` with the license string value. This function already handles parsing comma-separated values and generating the appropriate SQL `IN` clause. Do NOT write custom parsing or filtering logic -- `apply_filter` handles both single and multi-value cases.
  2. The filter should target the license column via a JOIN to the `package_license` entity table (`entity/src/package_license.rs`). Use the existing SeaORM/entity relationship defined in `package_license.rs` to perform the join rather than writing raw SQL.

- **Validate input**. If the `license` parameter contains invalid values (empty segments after splitting, or characters that are clearly not valid SPDX identifiers), return a 400 Bad Request via the existing `AppError` enum from `common/src/error.rs`.

- **Preserve existing behavior**. When `license` is `None`, the query must not be modified -- all packages are returned as before (no regression).

**Reuse**:
  - `common/src/db/query.rs::apply_filter` (Reuse Candidate 1) -- called directly to handle comma-separated parsing and SQL IN clause generation.
  - `entity/src/package_license.rs` (Reuse Candidate 3) -- used as the join entity to connect packages to their licenses in the filter query.
  - The overall structure mirrors the advisory service's severity filtering logic (Reuse Candidate 2).

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license query parameter.

**Changes**:

- **Follow the existing test patterns** from `tests/api/advisory.rs` for test setup, HTTP client construction, and assertion style.

- **Test cases** (one test function per acceptance criterion):

  1. **`test_single_license_filter`** -- Seed test data with packages having different licenses (e.g., MIT, Apache-2.0, GPL-3.0). Call `GET /api/v2/package?license=MIT`. Assert the response contains only MIT-licensed packages. Assert the response shape is `PaginatedResults<PackageSummary>`.

  2. **`test_comma_separated_license_filter`** -- Using the same seed data, call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert the response contains packages with either MIT or Apache-2.0 licenses but not GPL-3.0.

  3. **`test_no_license_filter_returns_all`** -- Call `GET /api/v2/package` without the `license` parameter. Assert all seeded packages are returned (no regression).

  4. **`test_invalid_license_returns_400`** -- Call `GET /api/v2/package?license=` (empty value) or with a clearly invalid value. Assert a 400 Bad Request response.

- **No new utility functions**. Test helpers should reuse whatever test infrastructure already exists in `tests/api/` (e.g., shared setup, test database fixtures, HTTP client wrappers).

---

## Change Summary

| File | Action | Lines (est.) |
|---|---|---|
| `modules/fundamental/src/package/endpoints/list.rs` | Modify | ~5-10 |
| `modules/fundamental/src/package/service/mod.rs` | Modify | ~15-25 |
| `tests/api/package_license_filter.rs` | Create | ~80-120 |

## Scope Boundary

No other files are modified. The changes are strictly limited to the files listed in the task's "Files to Modify" and "Files to Create" sections. No new utility functions are created -- all filtering logic is delegated to the existing `apply_filter` function.
