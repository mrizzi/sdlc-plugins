# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description
is used in the implementation. All three candidates are reused; no functionality
is duplicated.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Task description says:** "handles comma-separated multi-value query parameter
parsing and SQL IN clause generation; reuse directly for the license filter"

**How it is reused:**

`apply_filter` is called directly in `modules/fundamental/src/package/service/mod.rs`
inside the `PackageService::list` method. When the `license` query parameter is
present, the raw `Option<String>` value (e.g., `"MIT,Apache-2.0"`) is passed to
`apply_filter`, which:

1. Splits the string on commas
2. Trims whitespace from each segment
3. Returns a collection suitable for use in a SeaORM `.is_in()` filter (SQL `IN` clause)

**No new parsing logic is written.** The endpoint handler (`list.rs`) passes the raw
string to the service layer, and the service layer delegates all parsing to
`apply_filter`. This avoids duplicating the comma-splitting and trimming logic that
`apply_filter` already provides.

**Integration point:**
```rust
// In modules/fundamental/src/package/service/mod.rs
use common::db::query::apply_filter;

if let Some(license_param) = &license {
    let filter = apply_filter(license_param);
    query = query
        .join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())
        .filter(entity::package_license::Column::License.is_in(filter));
}
```

**Why direct reuse works:** `apply_filter` is a generic utility — it operates on any
comma-separated string and returns parsed values. It does not contain advisory-specific
or severity-specific logic. The license filter has the exact same parsing needs
(single or comma-separated values), so `apply_filter` is used without modification.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Task description says:** "the severity filter implementation is structurally
identical to the license filter needed here; follow the same Query struct pattern
with an optional field"

**How it is reused:**

The advisory list endpoint serves as the **structural template** for the package
license filter. The following patterns are replicated in
`modules/fundamental/src/package/endpoints/list.rs`:

1. **Query struct pattern:** The advisory endpoint defines a `Query` struct with
   `#[derive(Debug, Deserialize)]` containing an `Option<String>` field for the
   severity filter. The package endpoint follows the identical pattern, adding
   `pub license: Option<String>` to its existing `Query` struct.

2. **Handler forwarding pattern:** The advisory handler extracts `query.severity`
   and passes it to `AdvisoryService::list` as a parameter. The package handler
   follows the same pattern: extract `query.license` and pass it to
   `PackageService::list`.

3. **Validation pattern:** The advisory endpoint validates filter values before
   forwarding (non-empty segments, trimmed strings). The package endpoint applies
   the same validation logic for the license parameter.

**No code is copied from the advisory module.** The advisory file is used solely
as a reference for the structural pattern — how to wire an optional filter parameter
from the HTTP layer through to the service layer. The actual implementation is
written fresh in the package module, following the same conventions.

**Pattern correspondence:**

| Advisory (reference) | Package (new) |
|---|---|
| `Query { severity: Option<String> }` | `Query { license: Option<String> }` |
| `query.severity` forwarded to `AdvisoryService::list` | `query.license` forwarded to `PackageService::list` |
| Validation of severity segments | Validation of license segments |
| `apply_filter` call in advisory service | `apply_filter` call in package service |

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Task description says:** "existing entity for the package-license join table;
use for the JOIN query rather than writing raw SQL"

**How it is reused:**

The `package_license` entity is a SeaORM entity that maps the `package_license`
database table — the join table between packages and their declared licenses. It
defines:

- Column definitions (including `License` and `PackageId` columns)
- Relation definitions (e.g., `Relation::Package` linking back to the `package` table)

In `modules/fundamental/src/package/service/mod.rs`, when the license filter is
active, the query is extended with:

```rust
query = query
    .join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())
    .filter(entity::package_license::Column::License.is_in(filter));
```

This uses the entity in two ways:

1. **`Relation::Package.def().rev()`** — Uses the entity's defined relation to
   construct the JOIN clause. The `.rev()` reverses the direction (from package to
   package_license) so the join is `package INNER JOIN package_license ON ...`.
   No raw SQL join condition is written.

2. **`Column::License`** — Uses the entity's column enum to reference the `license`
   column in the filter clause. This provides compile-time safety — if the column
   name changes, the code will fail to compile rather than silently producing wrong
   SQL.

**Why entity reuse matters:** Without the entity, the implementation would need to
write raw SQL for the join and filter (`JOIN package_license ON ... WHERE license IN ...`).
Using the entity provides type safety, consistency with the rest of the codebase
(all modules use SeaORM entities for joins), and automatic adaptation if the schema
changes.

---

## Summary

| Reuse Candidate | Reuse Type | Location of Reuse |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `modules/fundamental/src/package/service/mod.rs` |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern (template) | `modules/fundamental/src/package/endpoints/list.rs` |
| `entity/src/package_license.rs` | Entity and relation usage for JOIN | `modules/fundamental/src/package/service/mod.rs` |

**No functionality is duplicated.** The comma-separated parsing is handled by
`apply_filter` (not reimplemented). The JOIN is handled by the SeaORM entity (not
raw SQL). The endpoint structure follows the advisory pattern (not a novel approach).
