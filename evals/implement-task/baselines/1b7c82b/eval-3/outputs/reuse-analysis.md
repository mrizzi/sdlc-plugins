# Reuse Analysis — TC-9203: Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are directly applicable
to this implementation and should be used. No new utility code needs to be written —
the implementation composes existing infrastructure.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`  
**Symbol**: `apply_filter` function  
**Reuse Type**: Direct invocation (no modification needed)

### What it provides

The `apply_filter` function handles:
- Parsing a comma-separated string into individual values (e.g., `"MIT,Apache-2.0"` -> `["MIT", "Apache-2.0"]`)
- Generating a SQL `IN` clause for multi-value filters
- Generating a SQL `=` clause for single-value filters
- Integration with SeaORM query builders

### How it will be used

In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method
will call `apply_filter` when the `license` parameter is `Some`:

```rust
if let Some(license_value) = license {
    query = apply_filter(
        query,
        package_license::Column::License,
        license_value,
    )?;
}
```

This is the same usage pattern as the advisory severity filter (Reuse Candidate 2).

### Why reuse over writing new code

- **Exact match**: `apply_filter` already implements the exact comma-separated multi-value
  parsing and SQL clause generation logic needed.
- **Consistency**: Using the shared helper ensures the license filter behaves identically
  to all other filters in the system (same parsing rules, same SQL generation, same
  error handling).
- **Zero new code**: No new parsing or SQL generation logic needs to be written.
- **Tested**: The shared helper is already tested and used by other endpoints.

### Validation needed

Before using, confirm via Serena (`find_symbol` with `include_body=true`) or Read:
- The function signature accepts a SeaORM `Select` query, a `Column` reference, and
  a `&str` filter value.
- The function returns a `Result` wrapping the modified query.
- The function handles empty string or invalid input gracefully (or verify that
  validation must happen before calling it).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`  
**Symbol**: Query struct and handler function  
**Reuse Type**: Structural pattern (follow the same architecture, adapt for license)

### What it provides

The advisory list endpoint implements a filter that is structurally identical to the
license filter:
- A `Query` struct with an `Option<String>` field for the filter parameter
- Axum query parameter extraction via `Query<T>` extractor
- Passing the extracted filter value to the service layer
- The service layer calling `apply_filter` with the appropriate column

### How it will be used

The advisory severity filter serves as the implementation template. Each structural
element will be replicated in the package module:

| Advisory (template) | Package (implementation) |
|---|---|
| `severity: Option<String>` in Query struct | `license: Option<String>` in Query struct |
| `query.severity.as_deref()` passed to service | `query.license.as_deref()` passed to service |
| `AdvisoryService::list(..., severity)` | `PackageService::list(..., license)` |
| `apply_filter(query, advisory_col, severity)` | `apply_filter(query, package_license::Column::License, license)` |

### Why reuse over writing new code

- **Proven pattern**: The severity filter is production-tested and follows all project
  conventions.
- **Consistency**: Following the identical pattern ensures the package license filter
  is architecturally consistent with other filters in the system.
- **Reduced risk**: Mimicking a working implementation reduces the chance of subtle
  bugs in handler setup, error propagation, or query construction.

### Differences from the template

One structural difference: the severity filter likely operates on a column within the
advisory entity itself, while the license filter requires a JOIN through the
`package_license` entity. This means the package service method must add an `InnerJoin`
to `package_license` before calling `apply_filter`. This is an extension of the pattern,
not a deviation — the `apply_filter` function works on any column in the active query,
including joined columns.

### Validation needed

Before implementing, inspect via Serena:
- The exact structure of the advisory Query struct (field names, derives, attributes)
- How the handler passes the filter to the service
- How the service method calls `apply_filter`
- Whether the advisory service does any pre-validation of the filter value (e.g., empty
  string rejection)

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`  
**Symbol**: Package-License SeaORM entity (Model, Entity, Relation, Column enums)  
**Reuse Type**: Direct use of existing entity for JOIN queries

### What it provides

The `package_license` entity defines:
- The SeaORM `Model` struct mapping to the `package_license` database table
- A `Column` enum with variants for each column (including `License` or similar SPDX
  identifier column)
- `Relation` definitions connecting the package_license table to the `package` table
  (and potentially to a `license` table)
- `Entity` and `ActiveModel` for ORM operations

### How it will be used

In `modules/fundamental/src/package/service/mod.rs`, the entity will be used to:

1. **Define the JOIN**: Use the entity's `Relation` to join `package` to `package_license`
   when the license filter is active:
   ```rust
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```

2. **Reference the filter column**: Pass `package_license::Column::License` (or the
   appropriate column variant) to `apply_filter` as the column to filter on:
   ```rust
   apply_filter(query, package_license::Column::License, license_value)
   ```

### Why reuse over writing new code

- **Existing schema mapping**: The entity already maps to the database table — no raw
  SQL, no manual column references, no risk of column name typos.
- **Relation integrity**: The SeaORM relation definitions ensure the JOIN is correct
  and matches the database foreign key constraints.
- **Compile-time safety**: Using the `Column` enum for the filter ensures type safety
  and catches errors at compile time rather than runtime.

### Validation needed

Before using, confirm via Serena or Read:
- The exact column name for the SPDX license identifier (likely `License` or `SpdxId`
  as a Column enum variant)
- That a `Relation` exists from `package` to `package_license` (or vice versa) to
  support the JOIN
- The join cardinality (one-to-many from package to package_license, meaning DISTINCT
  may be needed to avoid duplicate packages when a package has multiple licenses)

---

## Additional Reuse Opportunities Discovered

### `common/src/model/paginated.rs::PaginatedResults<T>`

While not listed as a Reuse Candidate (because it is already in use), this struct is
critical to the implementation: the response type must remain `PaginatedResults<PackageSummary>`.
No changes to this struct are needed.

### `common/src/error.rs::AppError`

The existing error type will be reused for returning `400 Bad Request` when invalid
license values are provided. Follow the same `AppError` construction pattern used in
the advisory endpoint for validation errors.

---

## Reuse Summary

| Candidate | Reuse Type | Modifications Needed | Risk |
|---|---|---|---|
| `apply_filter` | Direct call | None — use as-is | Low |
| Advisory severity filter pattern | Structural template | Adapt field names, add JOIN | Low |
| `package_license` entity | Direct use for JOIN/column ref | None — use existing entity | Low |
| `PaginatedResults<T>` | Already in use | None | None |
| `AppError` | Already in use | None | None |

**Key insight**: This task is essentially "replicate the advisory severity filter pattern
for the package license domain, substituting the target column and adding a table JOIN."
All three listed Reuse Candidates are used, and no new utility or helper code needs to
be created. The only net-new code is:
1. One new field in the Query struct
2. One new parameter threaded through the handler to the service
3. A conditional JOIN + filter call in the service method
4. Input validation for the license parameter
5. Integration tests
