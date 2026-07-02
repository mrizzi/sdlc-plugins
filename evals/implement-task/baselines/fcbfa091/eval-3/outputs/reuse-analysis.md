# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is applied during implementation. The goal is to maximize reuse of existing code and patterns, avoiding any duplication of functionality that already exists in the codebase.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a SeaORM column reference and a string value (which may contain commas), it:
1. Splits the string on commas to extract individual values
2. Generates a SQL `IN (value1, value2, ...)` clause for multi-value input
3. Generates a SQL `= value` clause for single-value input
4. Returns a SeaORM `Condition` that can be applied to any query builder

**How it is reused:** Called directly in the license filter implementation -- no wrapper, no new utility function. The license query parameter value (e.g., `"MIT"` or `"MIT,Apache-2.0"`) is passed to `apply_filter` along with the `package_license::Column::License` column reference. The returned `Condition` is applied to the query builder via `.filter()`.

**Where applied:**
- In `modules/fundamental/src/package/service/mod.rs` (or `endpoints/list.rs`, depending on which layer handles filtering based on the advisory pattern): the `apply_filter` function is imported and called when the `license` query parameter is present.

**Why direct reuse (not a new function):** The `apply_filter` function already encapsulates the exact logic needed -- comma parsing, single vs. multi-value handling, and SQL clause generation. Creating a new function like `parse_license_filter` or `build_license_condition` would duplicate this functionality. The task explicitly states to "reuse directly for the license filter."

**Example usage:**
```rust
use common::db::query::apply_filter;
use entity::package_license;

// In the service or handler:
if let Some(ref license_value) = license {
    let condition = apply_filter(package_license::Column::License, license_value);
    query = query.filter(condition);
}
```

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` -- Severity Filter Pattern

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter using a pattern that is structurally identical to what the license filter requires. The pattern consists of:
1. A `Query` struct with `#[derive(Deserialize)]` containing an optional `severity: Option<String>` field alongside pagination/sorting fields
2. An Axum handler that extracts the `Query` struct from the request
3. A conditional check: `if let Some(ref severity) = query.severity { ... }`
4. A call to `apply_filter` with the appropriate entity column and the filter value
5. Passing the filter to the service layer (either as a raw value or as a constructed condition)

**How it is reused:** The license filter follows this exact same structural pattern. Specifically:

1. **Query struct extension:** Add `license: Option<String>` to the package endpoint's `Query` struct, mirroring how `severity: Option<String>` is declared in the advisory endpoint's `Query` struct.

2. **Conditional filter application:** Use the same `if let Some(ref license) = query.license` pattern to conditionally apply the filter only when the parameter is provided, ensuring that omitting the parameter returns all packages (no regression).

3. **Service layer integration:** Pass the license filter to `PackageService::list` following the same mechanism the advisory endpoint uses to pass the severity filter to `AdvisoryService::list` -- whether that is passing the raw `Option<String>` or a pre-built condition.

4. **Validation pattern:** Follow the same input validation approach used for the severity parameter to validate license values and return 400 Bad Request for invalid input.

**Where applied:**
- `modules/fundamental/src/package/endpoints/list.rs` -- the `Query` struct definition, handler function, and filter application logic all follow the advisory severity filter pattern.

**Why pattern reuse (not copy-paste):** The advisory severity filter is not a reusable library function -- it is an implementation pattern embedded in a specific endpoint. The license filter reuses the pattern (struct shape, conditional logic, function calls) rather than copying code. This ensures consistency across endpoints while keeping each endpoint's code self-contained.

---

## Reuse Candidate 3: `entity/src/package_license.rs` -- Package-License Entity

**Source:** `entity/src/package_license.rs`

**What it provides:** A SeaORM entity definition for the `package_license` database table, which maps packages to their declared licenses. This entity provides:
1. A `Model` struct with fields corresponding to the table columns (likely `package_id` and `license` or `spdx_id`)
2. `Column` enum variants for type-safe column references (e.g., `package_license::Column::License`)
3. `Relation` definitions for SeaORM JOINs (likely a relation to the `package` entity)
4. Standard SeaORM entity traits (`EntityTrait`, `ActiveModelTrait`, etc.)

**How it is reused:** Used as the JOIN target in the database query for license filtering. Instead of writing raw SQL JOINs or creating a new entity, the existing `package_license` entity is used for:

1. **JOIN clause:** The `package_license::Relation::Package` relation (or its reverse) is used to JOIN the `package_license` table to the `package` table in the query builder:
   ```rust
   query = query.join(
       JoinType::InnerJoin,
       package_license::Relation::Package.def().rev()
   );
   ```

2. **Column reference for filtering:** The `package_license::Column::License` enum variant is passed to `apply_filter` to generate the WHERE clause on the correct column:
   ```rust
   apply_filter(package_license::Column::License, &license_value)
   ```

3. **Type safety:** By using the SeaORM entity rather than raw SQL strings, the implementation gets compile-time verification that the column names and relations are correct. If the schema changes, the compiler will catch mismatches.

**Where applied:**
- `modules/fundamental/src/package/service/mod.rs` -- imported and used in the `list` method's query builder for the JOIN and filter condition.
- `modules/fundamental/src/package/endpoints/list.rs` -- may also be imported here if the filter condition is built at the endpoint layer before passing to the service.

**Why entity reuse (not raw SQL):** The `package_license` entity already encodes the table schema, column types, and relations to other entities. Writing raw SQL (e.g., `JOIN package_license ON ...`) would bypass SeaORM's type safety and diverge from the codebase's convention of using entity-based queries throughout.

---

## Summary

All three Reuse Candidates are applied in the implementation:

| # | Reuse Candidate | Reuse Type | Benefit |
|---|---|---|---|
| 1 | `apply_filter` from `query.rs` | Direct function call | Eliminates need for custom comma-parsing or SQL IN clause generation |
| 2 | Severity filter pattern from advisory `list.rs` | Structural pattern replication | Ensures consistency with existing filter endpoints; no new patterns invented |
| 3 | `package_license` entity | Entity import for JOIN and column references | Provides type-safe database access; no raw SQL needed |

No new utility functions are created that duplicate existing functionality. The `apply_filter` function is the single point of responsibility for parsing multi-value filter strings and generating SQL conditions.
