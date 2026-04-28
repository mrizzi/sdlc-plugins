# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate listed in the task description is used in the implementation, following the implement-task skill's constraint (SKILL.md Section 5.4 / Step 6) to prefer code reuse over duplication.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`) and a SeaORM column reference, then produces the appropriate filter condition -- a single equality check for one value, or an `IN (...)` clause for multiple comma-separated values.

**How it is reused**: This function is called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to build the license filter condition. Instead of writing custom parsing logic to split comma-separated license values and construct SQL conditions, the implementation delegates entirely to `apply_filter`:

```rust
// In PackageService::list()
if let Some(license_value) = &license {
    let filter = apply_filter(package_license::Column::License, license_value);
    query = query.filter(filter);
}
```

**What is NOT duplicated**: No new comma-parsing logic, no new SQL `IN` clause construction, no new single-vs-multi-value branching. All of this already exists in `apply_filter` and is reused as-is.

**Reuse type**: Direct invocation -- no modification or extension needed. The function's existing signature and behavior exactly match the requirements of the license filter.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter using a Query struct pattern. The advisory endpoint's `AdvisoryListQuery` struct has an `Option<String>` field for severity, which is extracted by Axum from query parameters and passed through to `AdvisoryService::list()`. This is structurally identical to what the license filter needs.

**How it is reused**: The advisory endpoint's pattern serves as the structural template for the license filter implementation. Specifically:

1. **Query struct pattern**: The `PackageListQuery` struct in `modules/fundamental/src/package/endpoints/list.rs` adds an `Option<String>` field named `license`, mirroring how `AdvisoryListQuery` has an `Option<String>` field for `severity`.

2. **Handler-to-service flow**: The advisory list handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package list handler follows the same pattern: extract `query.license` and pass it to `PackageService::list()`.

3. **Validation pattern**: If the advisory endpoint validates the severity parameter before passing it to the service, the license filter follows the same validation approach and error handling.

**What is NOT duplicated**: The architectural pattern (how to wire a filter from HTTP query parameter through to database query) is not reinvented. The existing advisory severity filter is used as a proven blueprint, ensuring the license filter integrates consistently with the rest of the codebase.

**Reuse type**: Structural pattern reuse -- the advisory endpoint's code is not called directly, but its design pattern is followed precisely to maintain consistency across the codebase. This is the approach recommended in the task's Implementation Notes.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`

**What it provides**: This is an existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. It defines the table schema, column enum, and relation definitions that SeaORM uses for type-safe queries and joins.

**How it is reused**: The `package_license` entity is used in `PackageService::list()` to perform the JOIN between the `package` table and the `package_license` table when filtering by license. Instead of writing raw SQL joins, the implementation uses SeaORM's relation-based join API with the existing entity:

```rust
use entity::package_license;

// Join through the existing package_license entity
query = query.join(
    JoinType::InnerJoin,
    package_license::Relation::Package.def().rev()
);
```

**What is NOT duplicated**: No raw SQL `JOIN` statements, no manual table/column name strings, no duplicate entity definition. The existing `package_license` entity provides type-safe column references (e.g., `package_license::Column::License`) that are used with `apply_filter` for the `WHERE` clause.

**Reuse type**: Direct usage of an existing entity -- the entity is imported and its columns and relations are used for query construction. No modification to the entity itself is needed.

---

## Summary of Reuse Impact

| Reuse Candidate | Reuse Type | What It Eliminates |
|---|---|---|
| `apply_filter` | Direct invocation | Custom comma-parsing logic, SQL `IN` clause construction, single-vs-multi-value branching |
| Advisory list endpoint | Structural pattern | Architectural guesswork for wiring a filter parameter from HTTP to database |
| `package_license` entity | Direct usage | Raw SQL joins, manual table/column name strings, duplicate entity definitions |

By reusing all three candidates, the implementation requires only the minimal glue code to connect these existing pieces:

1. A new `Option<String>` field on the query struct (following advisory pattern)
2. A validation check on the license value
3. A conditional JOIN + filter call using `package_license` entity + `apply_filter`
4. Passing the parameter from handler to service

No new utility functions, no new entity definitions, and no new query-building logic are introduced. The implementation is composed almost entirely from existing, proven components.
