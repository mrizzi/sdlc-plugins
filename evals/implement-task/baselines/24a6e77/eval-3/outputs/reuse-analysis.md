# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This analysis covers all 3 Reuse Candidates identified in the task description and explains how each is applied in the implementation.

---

## 1. `common/src/db/query.rs::apply_filter`

**What it provides**: A shared utility function that accepts a raw query parameter string (potentially comma-separated), parses it into individual values, and generates a SQL IN clause suitable for SeaORM query conditions. It handles both single-value (`MIT`) and multi-value (`MIT,Apache-2.0`) inputs uniformly.

**How it is reused**: The `PackageService::list` method in `modules/fundamental/src/package/service/mod.rs` calls `apply_filter` directly, passing the raw `license` string from the query parameter. The function returns the appropriate filter condition, which is applied to the SeaORM query builder. This eliminates the need to write any custom parsing logic for comma-separated values or to construct IN clauses manually.

**Why this matters**: Writing a new function to split comma-separated strings and build IN clauses would duplicate `apply_filter`'s existing functionality. Reusing it ensures consistency across all endpoints that support multi-value filtering (advisory severity, package license, and any future filters) and avoids violating the no-duplication constraint.

---

## 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: A working reference implementation of the query-parameter-to-filter pattern. The advisory list endpoint defines a `Query` struct with an optional `severity` field, extracts it from the HTTP request via Axum's `Query` extractor, and passes the value to `AdvisoryService::list` for filtering. This is the established pattern for adding optional filters to list endpoints in this codebase.

**How it is reused**: The package list endpoint in `modules/fundamental/src/package/endpoints/list.rs` follows the identical structural pattern:

1. Add an `Option<String>` field named `license` to the package endpoint's `Query` struct (mirroring how `severity` is defined in the advisory `Query` struct).
2. Extract the value via Axum's `Query` extractor in the handler function (same mechanism).
3. Pass the extracted `Option<String>` to `PackageService::list` (same delegation pattern as advisory passes severity to `AdvisoryService::list`).

No new architectural patterns are introduced. The license filter is structurally identical to the severity filter, just targeting a different entity and field.

---

## 3. `entity/src/package_license.rs`

**What it provides**: A SeaORM entity that maps the `package_license` join table in PostgreSQL. This entity defines the schema columns and the relations between the `package` and license tables, enabling type-safe JOIN queries through SeaORM's relation API.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` filter is present, the service query JOINs through `entity::package_license` to access the license SPDX identifier column. The JOIN uses SeaORM's `find_also_linked` or `join` methods with the relations already defined on the entity, rather than writing raw SQL JOIN statements.

**Why this matters**: The entity already exists and correctly models the package-to-license relationship. Writing raw SQL or creating a new entity for this join would bypass SeaORM's type safety and duplicate the schema definition that `package_license.rs` already provides.

---

## Summary

| Reuse Candidate | Reuse Type | Location of Reuse |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `modules/fundamental/src/package/service/mod.rs` |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern (followed, not imported) | `modules/fundamental/src/package/endpoints/list.rs` |
| `entity/src/package_license.rs` | Entity import for JOIN query | `modules/fundamental/src/package/service/mod.rs` |

All three candidates are reused. No new utilities, entities, or architectural patterns are introduced that duplicate existing functionality.
