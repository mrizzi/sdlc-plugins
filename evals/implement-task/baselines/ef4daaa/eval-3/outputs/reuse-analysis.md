# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description would be
applied during implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**
The `apply_filter` function is a shared query builder helper in the `common` crate that
handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation.
It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas,
and applies the resulting values as a filter condition on a SeaORM query -- producing
either a simple equality condition for single values or an `IN (...)` clause for multiple
values.

**How it would be reused:**
In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method
would call `apply_filter` directly when a `license` filter is provided. The call would
look conceptually like:

```rust
use common::db::query::apply_filter;

// Inside PackageService::list()
if let Some(license) = license_filter {
    query = apply_filter(query, package_license::Column::License, &license)?;
}
```

**Why reuse is critical:**
The `apply_filter` function already handles:
- Splitting comma-separated values
- Trimming whitespace from individual values
- Generating a single `=` condition for one value or an `IN (...)` clause for multiple values
- Returning appropriate errors for malformed input

Writing a new parser for the license parameter would duplicate all of this logic. By
calling `apply_filter` directly, the implementation stays DRY and benefits from any future
improvements or bug fixes to the shared helper.

**No new utility functions needed:** Because `apply_filter` already covers both single-value
and multi-value comma-separated parsing, there is no reason to create a new parsing function,
a new `split_and_filter` helper, or any wrapper around `apply_filter`. It is used as-is.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
The advisory list endpoint already implements a query parameter filter (`severity`) that is
structurally identical to the license filter needed for TC-9203. The implementation
demonstrates the established pattern for adding an optional filter to a list endpoint in
the trustify-backend codebase:

1. A `Query` struct with Axum's `#[serde(default)]` deserialization that includes an
   optional filter field (e.g., `severity: Option<String>`)
2. The handler function extracts the field from the deserialized query struct
3. The handler passes the filter value to the corresponding service method
4. The service method conditionally applies the filter using `apply_filter` from
   `common/src/db/query.rs`

**How it would be reused:**
The pattern is replicated -- not the code itself -- in the package list endpoint. Specifically:

- **In `modules/fundamental/src/package/endpoints/list.rs`**: The existing `Query` struct
  (or equivalent query parameter struct) would gain a new field:
  ```rust
  #[serde(default)]
  pub license: Option<String>,
  ```
  This mirrors how `severity: Option<String>` is defined in the advisory list's Query struct.

- **In the handler function**: The `query.license` value would be extracted and passed to
  `PackageService::list()`, exactly as the advisory handler extracts `query.severity` and
  passes it to `AdvisoryService::list()`.

**Why this pattern matters:**
Following the advisory severity filter pattern ensures:
- Consistency across endpoints -- all list endpoints handle optional filters the same way
- Convention conformance -- the pattern has already been reviewed and accepted in the codebase
- Reduced review friction -- reviewers will recognize the familiar pattern immediately

**What is NOT reused:**
The actual severity filter code is not imported or called -- it is specific to advisories.
Only the structural pattern (Query struct field + handler extraction + service delegation)
is replicated for the license filter on the package endpoint.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**
The `package_license` entity is an existing SeaORM entity definition for the join table
that maps packages to their licenses. It defines the table structure, columns (including
the foreign key to `package` and the `license` identifier column), and the SeaORM
`Relation` definitions that enable type-safe JOINs in query builders.

**How it would be reused:**
In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method
would use the `package_license` entity to construct the JOIN when a license filter is
active:

```rust
use entity::package_license;

// Inside PackageService::list() when license filter is present
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(/* apply_filter on package_license::Column::License */);
```

The exact JOIN syntax follows SeaORM conventions -- using the entity's defined relations
rather than writing raw SQL JOIN clauses. This ensures:
- Type safety: column names and relations are checked at compile time
- Maintainability: if the `package_license` table schema changes, the entity definition
  is the single source of truth and the compiler will flag any mismatches
- Consistency: other service methods in the codebase that JOIN through mapping tables
  (e.g., `sbom_package`, `sbom_advisory`) follow this same entity-based JOIN pattern

**What is NOT done:**
- No new entity is created -- `package_license.rs` already exists and defines everything
  needed for the JOIN
- No raw SQL is written -- the SeaORM entity relations handle the JOIN condition
- No new migration is needed -- the `package_license` table already exists in the database

---

## Summary Table

| # | Reuse Candidate | Type of Reuse | Where Applied |
|---|---|---|---|
| 1 | `common/src/db/query.rs::apply_filter` | Direct function call | `modules/fundamental/src/package/service/mod.rs` -- parsing comma-separated license values and generating SQL filter |
| 2 | `modules/fundamental/src/advisory/endpoints/list.rs` | Pattern replication | `modules/fundamental/src/package/endpoints/list.rs` -- Query struct field, handler extraction, and service delegation follow the same structure |
| 3 | `entity/src/package_license.rs` | Entity-based JOIN | `modules/fundamental/src/package/service/mod.rs` -- JOIN through the existing package-license mapping table using SeaORM relations |

All three candidates are used. No new utility functions are created that would duplicate
the functionality of any existing code.
