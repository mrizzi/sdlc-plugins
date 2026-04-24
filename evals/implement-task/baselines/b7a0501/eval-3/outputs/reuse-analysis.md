# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description would be applied during implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** A shared utility function that handles comma-separated multi-value query parameter parsing and SQL IN clause generation. When given a raw query string like `"MIT,Apache-2.0"`, it splits the value on commas, trims whitespace, and produces either a single `column = value` condition (for single values) or a `column IN (value1, value2, ...)` condition (for multiple values).

**How it would be reused:**

In `modules/fundamental/src/package/service/mod.rs`, the `list` method would call `apply_filter` directly, passing:
- The raw `license` string from the query parameter (e.g., `"MIT"` or `"MIT,Apache-2.0"`)
- The SeaORM column reference for the license SPDX identifier in the `package_license` entity

This completely eliminates the need to write any custom comma-splitting, value-parsing, or SQL condition-building logic. The function is called as-is with no modifications or wrappers.

**Why reuse instead of writing new code:** Writing a new function to split comma-separated values and build IN clauses would be a direct duplication of `apply_filter`. The existing function already handles edge cases (trimming whitespace, single vs. multi-value) and is used by other modules (e.g., the advisory severity filter), so reusing it ensures consistent behavior and reduces maintenance burden.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A reference implementation of the exact filtering pattern needed for the license filter. The advisory list endpoint supports a `severity` query parameter that:
1. Defines an optional `severity: Option<String>` field in the `Query` struct used with Axum's `Query` extractor
2. Passes the extracted value to the service layer's `list` method
3. The service layer conditionally applies the filter only when the value is `Some`

This is structurally identical to the license filter: an optional query parameter that filters list results by matching a related field.

**How it would be reused:**

The advisory severity filter is not called as code -- it serves as a structural template. The implementation would replicate its pattern in the package module:

1. **In `modules/fundamental/src/package/endpoints/list.rs`**: Add `license: Option<String>` to the `Query` struct, mirroring how the advisory list's `Query` struct defines `severity: Option<String>`. The field uses the same Axum deserialization attributes (e.g., `#[serde(default)]`).

2. **In `modules/fundamental/src/package/service/mod.rs`**: Accept the optional license parameter and conditionally apply the filter, mirroring how `AdvisoryService::list` conditionally applies the severity filter. The conditional pattern is:
   ```rust
   if let Some(license) = license {
       // join package_license table and apply_filter
   }
   ```
   This matches the advisory's `if let Some(severity) = severity { ... }` pattern.

**Why follow this pattern:** The advisory severity filter has been validated in production and follows the module's established conventions. Inventing a different approach for the license filter would introduce inconsistency and make the codebase harder to maintain. Following the same pattern ensures that developers familiar with one filter implementation can immediately understand the other.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** An existing SeaORM entity definition for the `package_license` database table, which serves as a join table mapping packages to their declared licenses. The entity includes:
- Table name definition
- Column definitions (including the package foreign key and the license SPDX identifier column)
- Relation definitions linking `package_license` to `package` and potentially to a `license` table

**How it would be reused:**

In `modules/fundamental/src/package/service/mod.rs`, the `list` method would use this entity in two ways:

1. **JOIN clause**: Use `package_license::Entity` (or its `Relation` to `package`) to construct a SeaORM join from the `package` table to the `package_license` table. For example:
   ```rust
   query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
   ```
   This leverages the entity's pre-defined relation rather than writing raw SQL joins.

2. **WHERE clause column reference**: Use `package_license::Column::LicenseId` (or the equivalent SPDX identifier column) as the target column for `apply_filter`. This ensures the filter condition is applied to the correct column in the joined table.

**Why reuse instead of raw SQL:** The `package_license` entity already encodes the table schema, column names, and foreign key relationships. Using it provides:
- Compile-time type checking via SeaORM's typed column references
- Automatic handling of column naming conventions (snake_case to database naming)
- Consistency with how other modules perform joins in the codebase
- Protection against schema drift -- if the table is renamed or columns change, the entity definition is updated in one place

---

## Summary

| Reuse Candidate | Type | Usage |
|---|---|---|
| `apply_filter` from `query.rs` | Direct function call | Called in `PackageService::list` to parse comma-separated license values and generate SQL filter conditions |
| Severity filter pattern from advisory `list.rs` | Structural template | Replicated in package `list.rs` (Query struct) and `service/mod.rs` (conditional filter application) |
| `package_license` entity | SeaORM entity import | Used in `PackageService::list` for the JOIN clause and column reference in the WHERE condition |

No new utility functions, helpers, or abstractions need to be created. All required functionality is covered by existing code through direct reuse (Candidate 1 and 3) or pattern replication (Candidate 2).
