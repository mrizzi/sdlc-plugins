# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details which Reuse Candidates from the task description are used in the implementation and how each one is applied.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function is a shared query-builder helper that accepts a raw query parameter string (potentially comma-separated) and a column name. It parses the comma-separated values, validates them, and generates a SQL `WHERE column IN (...)` clause with parameterized values. This handles both single-value and multi-value filtering in a consistent, injection-safe way.

**How it is reused**: The `PackageService::list()` method in `modules/fundamental/src/package/service/mod.rs` calls `apply_filter` directly to apply the license filter to the query. Specifically:

```rust
use common::db::query::apply_filter;

if let Some(license_value) = license {
    query = apply_filter(query, "package_license.license", license_value)?;
}
```

This is a direct reuse -- no wrapper, no reimplementation. The function already handles:
- Splitting on commas to support `?license=MIT,Apache-2.0`
- Generating parameterized `IN` clauses for safety
- Returning errors for malformed input (empty segments, etc.)

**Why reuse instead of writing new code**: Writing custom comma-parsing and SQL generation would duplicate logic that already exists, is tested, and is used by other endpoints. Using `apply_filter` ensures consistent filtering behavior across the entire API (advisory severity, package license, and any future filters).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint already implements a query-parameter-based filter (the `severity` field). Its implementation demonstrates the established pattern for:
1. Defining a `Query` struct with `#[derive(Deserialize)]` that includes optional filter fields
2. Extracting the filter value from the Axum `Query` extractor
3. Passing the filter value through to the corresponding service method
4. Using `apply_filter` in the service layer to build the database query

**How it is reused**: The advisory list endpoint is used as a **structural template** -- not called directly, but its pattern is replicated exactly for the package license filter. Specifically:

| Advisory severity filter pattern | Package license filter (follows same pattern) |
|---|---|
| `Query` struct has `severity: Option<String>` | `Query` struct gets `license: Option<String>` |
| Handler extracts `query.severity` and passes to `AdvisoryService::list()` | Handler extracts `query.license` and passes to `PackageService::list()` |
| Service calls `apply_filter(query, "advisory.severity", severity_value)` | Service calls `apply_filter(query, "package_license.license", license_value)` |
| Error handling uses `.context("Failed to list advisories")` | Error handling uses `.context("Failed to list packages")` |

This is pattern reuse -- the advisory implementation serves as the proven blueprint, ensuring the new filter is consistent with existing API conventions. No new architectural patterns are introduced.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`

**What it provides**: A SeaORM entity definition for the `package_license` database table, which is a join table mapping packages to their declared licenses. It includes:
- The `Model` struct with columns (likely `package_id`, `license`, and possibly an `id`)
- `Relation` enum defining the foreign-key relationship back to the `package` table
- SeaORM derive macros for query building

**How it is reused**: The `PackageService::list()` method uses this entity to perform a JOIN when the license filter is active:

```rust
use entity::package_license;

if license.is_some() {
    query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
}
```

This is a direct reuse of the existing entity definition. The entity's `Relation::Package` already defines the foreign-key relationship, so the JOIN can be expressed declaratively through SeaORM rather than writing raw SQL. The `.rev()` call reverses the relation direction (from package_license to package) to perform the join from the package query side.

**Why reuse instead of writing raw SQL**: The entity already encodes the table structure and relationships. Using it for the JOIN ensures the query stays in sync with the schema and benefits from SeaORM's type checking and migration tracking.

---

## Summary

| Reuse Candidate | Reuse Type | Location Used |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs` |
| `advisory/endpoints/list.rs` severity filter | Structural pattern (template) | `modules/fundamental/src/package/endpoints/list.rs` Query struct and handler |
| `entity/src/package_license.rs` | Direct entity import for JOIN | `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs` |

All three reuse candidates are used. No new filtering, parsing, or query-building logic is written from scratch. The implementation composes existing components following the established patterns in the codebase.
