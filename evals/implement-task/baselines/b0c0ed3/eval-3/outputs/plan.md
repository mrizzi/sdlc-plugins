# Implementation Plan -- TC-9203: Add package license filter to list endpoint

## Scope

Add an optional `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add the `license` query parameter extraction and pass it to the service layer.

**Changes**:

- **Add or extend the query parameter struct**: Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate 2), add an `Option<String>` field named `license` to the query parameter struct used by the list handler. If a `PackageListQuery` struct already exists, add the field to it. If the handler currently only uses pagination/sorting parameters, create a `PackageListQuery` struct following the same shape as the advisory module's query struct, incorporating existing pagination fields alongside the new `license` field.

  ```rust
  #[derive(Debug, Deserialize)]
  pub struct PackageListQuery {
      // ... existing pagination/sorting fields ...
      pub license: Option<String>,
  }
  ```

- **Update the handler function**: Modify the handler to extract `Query<PackageListQuery>` (if not already doing so) and pass `query.license` to the `PackageService::list()` call. This mirrors how the advisory list handler passes `severity` to `AdvisoryService::list()`.

- **Add validation**: If the `license` parameter is present but contains empty or invalid values after comma-splitting, return a `400 Bad Request` using the existing `AppError` enum from `common/src/error.rs`. Follow the same validation pattern used in the advisory endpoint.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Add license filtering logic to the `PackageService::list()` method.

**Changes**:

- **Update method signature**: Add an `Option<String>` parameter (or equivalent) for the license filter to the `list()` method signature.

- **Build the filter using `apply_filter`** (Reuse Candidate 1): When the `license` parameter is `Some`, call `common::db::query::apply_filter` with the raw license string and the appropriate column from the `package_license` entity. `apply_filter` handles comma-separated parsing and generates the SQL `IN` clause, so no custom parsing logic is needed.

- **JOIN through `package_license` entity** (Reuse Candidate 3): Use SeaORM's join capabilities with the existing `entity::package_license` entity to join the `package` table to the `package_license` table. The entity already defines the necessary `Relation`, so the join is:

  ```rust
  use entity::package_license;

  // Within the query builder:
  query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
  ```

  Then apply the filter condition on `package_license::Column::License` using `apply_filter`.

- **Preserve existing behavior**: When `license` is `None`, skip the join and filter entirely so that the unfiltered query returns all packages (no regression).

- **Error propagation**: Use `.context()` wrapping on any fallible operations, consistent with the project's error handling convention.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter feature.

**Changes**:

- **Follow existing test patterns**: Model the test file after `tests/api/advisory.rs` and `tests/api/sbom.rs`, which hit a real PostgreSQL test database and assert on response status codes and body content.

- **Register in test module**: Add `mod package_license_filter;` to the test module's root (likely `tests/api/mod.rs` or via Cargo test configuration).

- **Test cases**:

  1. **Single license filter**: Seed test data with packages having different licenses. Send `GET /api/v2/package?license=MIT`. Assert response status is 200, assert the returned `PaginatedResults<PackageSummary>` contains only packages with MIT license, assert count matches expected.

  2. **Comma-separated multi-value filter**: Send `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response contains packages matching either license, assert no packages with other licenses appear.

  3. **No license filter (regression)**: Send `GET /api/v2/package` without the `license` parameter. Assert all packages are returned, assert response shape is unchanged.

  4. **Invalid license value returns 400**: Send `GET /api/v2/package?license=` (empty value) or a clearly malformed value. Assert response status is 400 Bad Request.

- **Test data setup**: Use the same test fixture/seeding approach as sibling test files. Insert packages via the ingestion path or direct database seeding, associating them with known SPDX license identifiers through the `package_license` join table.

---

## Reuse Summary

| What | Reuse Candidate | How |
|---|---|---|
| Comma-separated parsing and SQL IN clause | `common/src/db/query.rs::apply_filter` | Called directly in `PackageService::list()` -- no new parsing logic |
| Query struct pattern and handler flow | `advisory/endpoints/list.rs` severity filter | Replicate the same struct + extraction + delegation pattern in the package endpoint |
| Package-to-license JOIN | `entity/src/package_license.rs` | Use existing SeaORM entity and its Relations for the JOIN -- no raw SQL |

No new utility functions, helpers, or shared modules are created. All filtering infrastructure already exists in the codebase.

---

## Files NOT Modified

The following files are explicitly out of scope:

- `entity/src/package_license.rs` -- used as-is, not modified
- `common/src/db/query.rs` -- `apply_filter` is called, not changed
- `modules/fundamental/src/advisory/endpoints/list.rs` -- referenced as a pattern template only
- `modules/fundamental/src/package/model/summary.rs` -- `PackageSummary` already includes a `license` field; the response shape is unchanged
- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration for `GET /api/v2/package` already exists; no new routes are added
- `server/main.rs` -- no new modules or routes to mount

---

## Commit Plan

A single commit scoped to TC-9203:

```
feat(package): add license filter to GET /api/v2/package

Support single-value and comma-separated multi-value filtering by SPDX
license identifier. Reuses apply_filter from common/src/db/query.rs and
joins through the existing package_license entity.

TC-9203
```
