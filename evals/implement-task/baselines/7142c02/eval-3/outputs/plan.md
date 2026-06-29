# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value
and comma-separated multi-value filtering by SPDX license identifier. The implementation
reuses existing filtering infrastructure throughout.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with pagination and sorting but no
license filtering.

**Changes:**

- Add an optional `license: Option<String>` field to the `Query` struct (the query
  parameter extraction struct for the list endpoint). This follows the exact same
  pattern used by the `severity` field in the advisory list endpoint's Query struct
  at `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, after extracting query parameters, pass the `license`
  value to `PackageService::list()` (modified below).
- Use `common::db::query::apply_filter` to convert the `license` parameter
  (which may be a comma-separated string like `"MIT,Apache-2.0"`) into the
  appropriate SQL filtering clause. Do NOT write custom parsing logic for splitting
  comma-separated values -- `apply_filter` already handles this.
- Add input validation: if the `license` parameter is present but contains empty
  segments after splitting (e.g., `license=,` or `license=MIT,,Apache-2.0`),
  return 400 Bad Request.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries packages with
pagination and sorting but no license filtering.

**Changes:**

- Add an optional `license` parameter (e.g., `license: Option<String>`) to the
  `list` method signature.
- When `license` is `Some`, construct a JOIN against the `package_license` entity
  (`entity::package_license`) to filter packages by their associated license SPDX
  identifier. Use the `package_license` SeaORM entity from
  `entity/src/package_license.rs` for this JOIN rather than writing raw SQL.
- Apply the filter using `apply_filter` from `common/src/db/query.rs`, which
  handles the comma-separated multi-value case (generates a SQL `IN` clause for
  multiple values and a simple equality check for a single value).
- When `license` is `None`, skip the JOIN and filter entirely, preserving the
  existing behavior (return all packages).

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Structure:** Follow the test conventions observed in sibling test files
(`tests/api/advisory.rs`, `tests/api/sbom.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases.
- Deserialize response body into `PaginatedResults<PackageSummary>`.
- Assert on specific field values (not just counts).
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases.

**Test cases:**

1. **`test_list_packages_filter_single_license`** -- Seed packages with various
   licenses; request `?license=MIT`; assert only MIT-licensed packages are returned;
   verify specific package names/identifiers in the response items.

2. **`test_list_packages_filter_multi_license`** -- Seed packages with MIT,
   Apache-2.0, and GPL-3.0 licenses; request `?license=MIT,Apache-2.0`; assert
   packages with either MIT or Apache-2.0 are returned; verify GPL-3.0 packages
   are excluded.

3. **`test_list_packages_no_license_filter`** -- Seed packages with various
   licenses; request `/api/v2/package` with no `license` parameter; assert all
   packages are returned; verify count matches total seeded.

4. **`test_list_packages_invalid_license`** -- Request `?license=` (empty value);
   assert 400 Bad Request response.

Each test function will have a `///` doc comment explaining what it verifies and
use `// Given`, `// When`, `// Then` section comments for non-trivial tests.

**Registration:** Add `mod package_license_filter;` to the test module's `mod.rs`
or `main.rs` in `tests/api/` so the test file is included in the test suite.

---

## API Changes

### `GET /api/v2/package`

- **New parameter:** `license` (optional, query string)
  - Type: `String`
  - Behavior: Filters packages by SPDX license identifier
  - Single value: `?license=MIT` -- exact match
  - Multi-value: `?license=MIT,Apache-2.0` -- matches any listed license (OR semantics)
  - Absent: returns all packages (no regression)
- **Response shape:** Unchanged -- `PaginatedResults<PackageSummary>`

---

## Code Reuse Strategy

All three Reuse Candidates from the task description are used directly:

1. **`common/src/db/query.rs::apply_filter`** -- Reused directly for parsing the
   comma-separated `license` query parameter and generating the SQL `IN` clause.
   No new parsing logic is written. This function already handles splitting on commas,
   trimming whitespace, and generating either a single equality condition or a
   multi-value `IN` clause.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Used as the structural
   blueprint. The advisory list endpoint's `Query` struct with its optional `severity`
   field and the way it passes that field through to the service layer is exactly the
   pattern replicated for the `license` field in the package list endpoint. The handler
   function structure (extract query params, call service, return paginated result) is
   followed identically.

3. **`entity/src/package_license.rs`** -- Used as the SeaORM entity for constructing
   the JOIN query between `package` and `package_license` tables. The entity's
   `Relation` definitions and column mappings are used directly in the service layer
   query builder rather than writing raw SQL joins.

---

## Data-Flow Trace

```
HTTP Request (GET /api/v2/package?license=MIT,Apache-2.0)
  -> Axum extracts Query struct (license: Option<String>)
  -> Handler passes license to PackageService::list()
  -> PackageService builds SeaORM query:
     - JOINs package_license entity when license is Some
     - Calls apply_filter to generate IN clause from comma-separated value
  -> SeaORM executes query against PostgreSQL
  -> Results mapped to Vec<PackageSummary>
  -> Wrapped in PaginatedResults<PackageSummary>
  -> Serialized as JSON response
```

All stages are connected; no incomplete paths.

---

## Scope Boundaries

All changes are strictly within the files specified by "Files to Modify" and
"Files to Create":

- `modules/fundamental/src/package/endpoints/list.rs` (modify)
- `modules/fundamental/src/package/service/mod.rs` (modify)
- `tests/api/package_license_filter.rs` (create)

No other files are modified. No new utility functions are created -- existing
infrastructure (`apply_filter`, `package_license` entity, advisory list pattern)
covers all needs.
