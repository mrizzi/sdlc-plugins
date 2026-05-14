# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document analyzes all three Reuse Candidates identified in the task description and explains how each would be applied during implementation.

---

## 1. common/src/db/query.rs::apply_filter

**What it provides:** The `apply_filter` function is a shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. When given a raw query string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces the appropriate SeaORM filter condition — an `IN` clause for multiple values or an equality check for a single value.

**How it would be applied:** In `modules/fundamental/src/package/service/mod.rs`, the `PackageService` list method would call `apply_filter` directly, passing in the raw `license` query parameter string and the target column from the `package_license` entity. This handles all parsing and filter construction in one call.

**Why reuse instead of writing new code:** Writing custom comma-splitting or filter-building logic would duplicate the exact functionality that `apply_filter` already provides. Per constraint 5.4, no new utility functions should be created that duplicate `apply_filter`. The function is already battle-tested by other endpoints (e.g., the advisory severity filter) and handles edge cases like empty strings, trailing commas, and whitespace consistently across the codebase.

**Specific usage:**
- Input: the raw `Option<String>` from the query parameter (e.g., `Some("MIT,Apache-2.0")`)
- Output: a SeaORM `Condition` that filters the `package_license` table's license column using `IN ('MIT', 'Apache-2.0')`
- No intermediate parsing step is needed — `apply_filter` handles the full pipeline from raw string to SQL condition

---

## 2. modules/fundamental/src/advisory/endpoints/list.rs

**What it provides:** The advisory list endpoint implements a severity filter that is structurally identical to the license filter needed for TC-9203. It demonstrates the full pattern: declaring an optional filter field on the `Query` struct, extracting it from the request, and passing it to the service layer for application.

**How it would be applied:** The advisory endpoint's severity filter serves as the structural guide for implementing the license filter:

1. **Query struct pattern:** The advisory endpoint defines a `Query` struct (or equivalent) with an optional `severity: Option<String>` field that Axum deserializes from query parameters. The package endpoint's `Query` struct would add `license: Option<String>` following the same pattern.

2. **Endpoint wiring:** The advisory endpoint passes the severity value from the `Query` struct to its service method. The package endpoint would do the same — passing `query.license` to `PackageService::list`.

3. **Service integration:** The advisory service shows how to conditionally apply a filter only when the parameter is `Some(value)`, and how to call `apply_filter` with the appropriate entity column. The package service would follow this same conditional pattern.

**Why follow this pattern:** Using an established, working pattern ensures consistency across the codebase and reduces the risk of missing edge cases. The advisory severity filter has already been reviewed and tested, making it a reliable template.

---

## 3. entity/src/package_license.rs

**What it provides:** This is the existing SeaORM entity definition for the package-license join table. It maps the many-to-many relationship between packages and their declared licenses, with columns for the package ID foreign key and the license SPDX identifier.

**How it would be applied:** When the license filter is active, the `PackageService` list method needs to JOIN the main package query with the `package_license` table to filter by license values. The existing entity in `entity/src/package_license.rs` provides:

1. **The `Entity` type** — used in SeaORM's `.join()` or `.find_also_related()` methods to construct the SQL JOIN without writing raw SQL.
2. **The `Column` enum** — specifically `Column::License` (or equivalent) is passed to `apply_filter` as the target column for the filter condition.
3. **The `Relation` definitions** — the entity already defines its relationship to the package entity, so SeaORM can automatically generate the correct JOIN ON clause.

**Why use the existing entity:** Writing raw SQL for the JOIN would bypass SeaORM's type safety and relationship management. Creating a new entity would duplicate what already exists. The `package_license` entity is purpose-built for exactly this kind of query — joining packages to their licenses — and using it keeps the implementation consistent with how other entity relationships are queried throughout the codebase.

**Specific usage:**
- Join: `query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())` (or equivalent SeaORM join syntax using the entity's defined relations)
- Filter column: `package_license::Column::License` passed to `apply_filter`
- The JOIN is only added when `license.is_some()` to avoid unnecessary joins when no filter is requested
