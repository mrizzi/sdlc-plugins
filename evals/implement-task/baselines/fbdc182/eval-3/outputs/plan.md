# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that supports both
single-value and comma-separated multi-value filtering. The response shape
(`PaginatedResults<PackageSummary>`) must remain unchanged.

Implementation follows the severity filter pattern already established in the advisory
list endpoint. No new parsing utilities are needed — `apply_filter` from `common/src/db/query.rs`
handles comma-separated multi-value parameters and SQL IN clause generation.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- Add an optional `license` field to the existing query parameter extraction struct
  (mirroring the `Query` struct pattern used in
  `modules/fundamental/src/advisory/endpoints/list.rs` for `severity`).
- Extract the `license` value from the incoming `axum::extract::Query<…>` extractor.
- Pass the extracted value down to the `PackageService` list method.

**How reuse applies:**

The advisory list endpoint already defines a `Query` struct with an `Option<String>`
field for `severity`, deserializes it via Axum's `Query` extractor, and forwards the
value to the service layer. The same struct-and-extractor pattern is used here verbatim.
No bespoke parsing code is written in this file; all multi-value splitting is delegated
to `apply_filter` inside the service.

**Concrete changes (described, not actual Rust source):**

1. Extend (or add) the handler's query struct:
   ```
   struct ListQuery {
       // ... existing fields (q, offset, limit, sort, etc.) ...
       license: Option<String>,
   }
   ```
2. In the handler function signature, receive `Query(params): Query<ListQuery>`.
3. Forward `params.license` to `PackageService::list(…, license: Option<String>)`.
4. Add a doc comment on the struct field explaining the comma-separated format.

**Scope note:** No changes to route registration (`endpoints/mod.rs`) are required
because Axum's `Query` extractor handles additional optional fields transparently.

---

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- Extend the `list` method (or its equivalent) on `PackageService` to accept a
  `license: Option<String>` parameter.
- When `license` is `Some(…)`, use `apply_filter` from `common/src/db/query.rs` to
  parse the comma-separated string and build an SQL IN clause.
- Perform a JOIN through `entity::package_license` (from `entity/src/package_license.rs`)
  to reach the license identifier column, then apply the generated filter condition.
- When `license` is `None`, the query runs without the JOIN and filter (no regression
  for callers that omit the parameter).

**How reuse applies:**

- `apply_filter` handles the entire parsing-and-filter-building step. The service
  calls it with the raw `Option<String>` value and receives a SeaORM condition
  (or equivalent query fragment) ready to attach to the query builder — no bespoke
  comma-splitting or IN-clause construction is written here.
- The `entity::package_license` SeaORM entity provides the typed column reference for
  the JOIN. The query uses the entity's column definitions directly rather than raw SQL
  strings, consistent with how other modules reference join-table entities
  (e.g., `entity::sbom_advisory`, `entity::sbom_package`).

**Concrete changes (described):**

1. Add `use common::db::query::apply_filter;` and `use entity::package_license;` imports.
2. Update the `list` method signature:
   ```
   pub async fn list(
       &self,
       // ... existing params ...
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError>
   ```
3. Inside the method body, after constructing the base query on `entity::package`:
   ```
   // Conditionally join package_license and apply license filter
   if let Some(ref license_param) = license {
       let filter = apply_filter(package_license::Column::LicenseId, license_param);
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(filter);
   }
   ```
4. Add a doc comment on the updated method explaining the new parameter.

---

## Files to Create

### `tests/api/package_license_filter.rs`

**What this file contains:**

Integration tests that exercise the license filter against a real PostgreSQL test
database, following the assertion and structural conventions established in the sibling
test files `tests/api/sbom.rs` and `tests/api/advisory.rs`.

**Test structure and conventions applied:**

- All tests use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and
  `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for invalid-input cases,
  matching the pattern used in sibling test files.
- List response validation checks `total_count` and asserts on specific item field
  values (not just `.len()`), consistent with the "prefer value-based assertions"
  requirement from the skill.
- Each test function is prefixed with `test_` and carries a `///` doc comment
  explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.

**Tests to implement (one per acceptance criterion / test requirement):**

1. `test_list_packages_single_license_filter`
   — Seeds packages with MIT and Apache-2.0 licenses. Calls
   `GET /api/v2/package?license=MIT`. Asserts status 200 and that every returned
   package has `license == "MIT"`. Asserts `total_count` matches only MIT packages.

2. `test_list_packages_multi_license_filter`
   — Seeds packages with MIT, Apache-2.0, and GPL-3.0. Calls
   `GET /api/v2/package?license=MIT,Apache-2.0`. Asserts status 200 and that every
   returned package has a license in `{MIT, Apache-2.0}`. GPL-3.0 packages must not
   appear.

3. `test_list_packages_no_license_filter_returns_all`
   — Seeds several packages. Calls `GET /api/v2/package` (no `license` param).
   Asserts status 200 and that `total_count` equals the total seeded package count.

4. `test_list_packages_invalid_license_returns_400`
   — Calls `GET /api/v2/package?license=` (empty string) or a value that fails
   server-side validation. Asserts status 400.

**Registration note:** The new test file must be declared in `tests/Cargo.toml` or
the test crate's module root (whichever pattern the existing sibling tests use) so
that Cargo discovers it. This is an in-scope change because it is part of the
"Files to Create" scope.

---

## Data-Flow Trace

```
HTTP request: GET /api/v2/package?license=MIT,Apache-2.0
  └─ Axum Query extractor deserializes `license` into ListQuery.license (Option<String>)
       └─ Handler forwards Option<String> to PackageService::list(…, license)
            └─ Service calls apply_filter(package_license::Column::LicenseId, &license_str)
                 └─ apply_filter returns SeaORM Condition (IN clause)
                      └─ Query builder JOINs package_license, applies Condition
                           └─ DB returns filtered rows
                                └─ Service maps rows → PaginatedResults<PackageSummary>
                                     └─ Handler returns JSON response (shape unchanged)
```

All stages are connected. The response shape `PaginatedResults<PackageSummary>` is
unchanged — only the query inputs differ.

---

## Out-of-Scope

The following are explicitly excluded:

- No changes to `modules/fundamental/src/package/endpoints/mod.rs` (route registration
  is unaffected; Axum handles optional query params transparently).
- No changes to `entity/src/package_license.rs` (the entity is reused as-is).
- No changes to `common/src/db/query.rs` (apply_filter is reused as-is).
- No changes to `modules/fundamental/src/package/model/summary.rs` (response shape
  must not change per acceptance criteria).
- No new utility functions that duplicate apply_filter functionality.
