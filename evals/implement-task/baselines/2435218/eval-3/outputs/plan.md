# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and
comma-separated multi-value filtering by SPDX license identifier. The implementation
reuses existing infrastructure throughout: `apply_filter` for parameter parsing,
the advisory severity-filter pattern for endpoint structure, and the `package_license`
entity for the JOIN query.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Defines the handler for `GET /api/v2/package`. Contains a `Query`
struct for extracting query parameters (pagination, sorting) and a handler function
that calls `PackageService::list`.

**Changes:**

- **Add `license` field to the `Query` struct:** Add an `Option<String>` field named
  `license` to the existing query-parameter extraction struct, following the exact
  pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
  The field is `Option<String>` because `apply_filter` handles the comma-splitting
  internally.

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct Query {
      // ... existing fields (pagination, sort, etc.)
      /// Optional license filter — single SPDX identifier or comma-separated list.
      pub license: Option<String>,
  }
  ```

- **Pass `license` to the service layer:** In the handler function, forward
  `query.license` to `PackageService::list` as an additional parameter. No parsing
  happens here — the raw `Option<String>` is passed down to the service where
  `apply_filter` handles comma-separated splitting and SQL `IN` clause generation.

- **Input validation:** Before forwarding, if `license` is `Some`, validate that
  each comma-separated segment is a non-empty trimmed string (consistent with how
  the advisory severity filter validates its input). Return `400 Bad Request` via
  `AppError` for empty segments or whitespace-only values.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that builds a
SeaORM query against the `package` table, applies pagination and sorting, and
returns `PaginatedResults<PackageSummary>`.

**Changes:**

- **Accept `license` parameter:** Add `license: Option<String>` to the `list`
  method signature.

- **Build the license filter using `apply_filter`:** Import and call
  `common::db::query::apply_filter` to handle the comma-separated `license` value.
  `apply_filter` parses the string, splits on commas, trims whitespace, and generates
  a SQL `WHERE ... IN (...)` clause. This is the same function already used by
  `AdvisoryService` for the severity filter — no new parsing logic is written.

  ```rust
  use common::db::query::apply_filter;

  // Inside the list method, after building the base query:
  if let Some(license_param) = &license {
      let filter = apply_filter(license_param);
      // Join through package_license entity and apply the filter
      query = query
          .join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())
          .filter(entity::package_license::Column::License.is_in(filter));
  }
  ```

- **JOIN through `package_license` entity:** Use the SeaORM relation defined in
  `entity/src/package_license.rs` to join the `package` table to the `package_license`
  table. The entity already defines the relation — no raw SQL is needed. The join is
  only added when the `license` parameter is present, so unfiltered queries are
  unaffected.

- **Deduplication:** Since a package may have multiple licenses, the JOIN could
  produce duplicate rows. Add `.distinct()` to the query when the license filter is
  active, following the same pattern used elsewhere in the codebase for join-based
  filters.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on `GET /api/v2/package`.

**Structure:** Follows the same patterns found in sibling test files
(`tests/api/advisory.rs`, `tests/api/sbom.rs`):
- Uses `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Uses `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for validation errors
- Follows `test_<endpoint>_<scenario>` naming convention
- Hits a real PostgreSQL test database with seeded test data

**Test functions:**

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: packages with MIT and Apache-2.0 licenses in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only MIT-licensed packages are returned
    // Assert: response status is 200, items contain only MIT packages,
    //         verify specific package names/identifiers (value-based assertion)
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_comma_separated_licenses() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
    // Assert: response status is 200, verify specific returned packages by name
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: packages with various licenses in the database
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned (no regression)
    // Assert: response status is 200, total_count matches expected full count
}

/// Verifies that an invalid (empty) license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_filter() {
    // Given: a running server
    // When: GET /api/v2/package?license=
    // Then: 400 Bad Request is returned
    // Assert: response status is 400
}
```

**Registration:** The new test file must be declared as a module in `tests/api/`
(e.g., added to a `mod.rs` or declared in `Cargo.toml` test targets, depending on
the existing test organization).

---

## Files NOT Modified

The following files are intentionally left unchanged:

- `common/src/db/query.rs` — `apply_filter` is reused as-is; no modifications needed
- `entity/src/package_license.rs` — the entity and its relations are reused as-is
- `modules/fundamental/src/advisory/endpoints/list.rs` — used only as a reference pattern
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` response struct is unchanged
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper is unchanged
- `modules/fundamental/src/package/endpoints/mod.rs` — route registration unchanged (the existing route for `list.rs` already handles query parameters)
- `server/src/main.rs` — no new routes or modules to mount

---

## How Existing Code Is Reused

1. **`common/src/db/query.rs::apply_filter`** — Called directly in `PackageService::list`
   to parse the comma-separated license string into individual values for SQL `IN`
   clause generation. No wrapper, no duplication — the existing function handles all
   the parsing and clause construction.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** — The severity filter
   pattern is followed structurally: same `Query` struct approach with an
   `Option<String>` field, same forwarding to the service layer, same validation
   flow. No code is copied — the pattern is replicated in the package endpoint.

3. **`entity/src/package_license.rs`** — The existing SeaORM entity and its defined
   relations are used for the JOIN query in `PackageService::list`. No raw SQL is
   written; the entity's `Relation::Package` definition handles the join semantics.

---

## Data-Flow Trace

```
GET /api/v2/package?license=MIT,Apache-2.0
  -> list.rs: extract Query { license: Some("MIT,Apache-2.0"), ... }
  -> list.rs: validate license segments (non-empty, trimmed)
  -> list.rs: call PackageService::list(..., license: Some("MIT,Apache-2.0"))
  -> service/mod.rs: call apply_filter("MIT,Apache-2.0") -> ["MIT", "Apache-2.0"]
  -> service/mod.rs: JOIN package_license, WHERE license IN ("MIT", "Apache-2.0")
  -> service/mod.rs: .distinct() to deduplicate
  -> service/mod.rs: apply pagination and sorting
  -> service/mod.rs: return PaginatedResults<PackageSummary>
  -> list.rs: return JSON response (200 OK)
```

All stages are connected. The response shape (`PaginatedResults<PackageSummary>`) is unchanged.

---

## Acceptance Criteria Verification Plan

| Criterion | How Verified |
|---|---|
| `?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| `?license=MIT,Apache-2.0` returns matching packages | `test_list_packages_filter_comma_separated_licenses` |
| No `license` param returns all packages | `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests deserialize into `PaginatedResults<PackageSummary>` |
| Invalid license returns 400 | `test_list_packages_invalid_license_filter` |
