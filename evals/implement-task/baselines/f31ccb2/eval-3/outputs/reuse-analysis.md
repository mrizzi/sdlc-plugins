# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Overview

This task has three identified Reuse Candidates. All three are reused directly in the implementation, eliminating the need to write new utility functions, entity definitions, or filter patterns from scratch. Below is a detailed analysis of each.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Location**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function is a shared query-building helper that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a raw string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace from each value, and produces the appropriate database filter expression (e.g., `column IN ('MIT', 'Apache-2.0')`). For single values, it produces a simple equality check.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, the service method calls `apply_filter` directly, passing the raw license string and the target column (the SPDX identifier column from the `package_license` entity). This handles both the single-value case (`?license=MIT`) and the multi-value case (`?license=MIT,Apache-2.0`) without any new parsing code.

**Why direct reuse is correct**: Writing custom comma-splitting or `IN` clause generation logic would duplicate exactly what `apply_filter` already does. The function's interface matches the need precisely: it takes an optional string parameter and a column reference, and returns a filter condition. No adaptation or wrapping is required.

**What is NOT done**: No new helper function is created for parsing comma-separated license values. No manual `split(',')` or custom SQL builder logic is written anywhere in the package module.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Location**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a severity filter that is structurally identical to the license filter needed for packages. It demonstrates the established pattern for adding an optional filter parameter to a list endpoint:

1. **Query struct**: An `Option<String>` field on the request/query parameter struct captures the filter value from the URL query string.
2. **Handler function**: The handler extracts the filter value from the deserialized query struct and passes it to the corresponding service method.
3. **Service delegation**: The handler does not contain filtering logic itself — it delegates to the service layer, which applies the filter using `apply_filter`.

**How its pattern is followed**: The package license filter implementation mirrors this pattern step-by-step:

- A `license: Option<String>` field is added to the query parameter struct in `modules/fundamental/src/package/endpoints/list.rs`, exactly as the advisory module declares its severity field.
- The handler extracts `query.license` and passes it to `PackageService::list()`, exactly as the advisory handler passes its severity value to `AdvisoryService::list()`.
- The service method in `modules/fundamental/src/package/service/mod.rs` receives the license parameter and applies `apply_filter` to the query, matching how the advisory service applies its severity filter.

**Why pattern-following is correct**: Consistency across modules is a key maintainability concern. By following the advisory filter pattern, the new code is immediately recognizable to anyone familiar with the codebase. It also ensures the same error handling, pagination, and query-building conventions are respected.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Location**: `entity/src/package_license.rs`

**What it provides**: This is the existing Sea-ORM (or equivalent ORM) entity definition for the `package_license` join table. The table maps packages to their declared licenses, containing at minimum a package ID foreign key and a license SPDX identifier column. The entity provides the column definitions, relation definitions, and model struct needed to query this table.

**How it is used**: In `modules/fundamental/src/package/service/mod.rs`, the license filter implementation adds a JOIN from the `package` table to the `package_license` table using this entity. Specifically:

- The entity's relation definition (linking `package.id` to `package_license.package_id`) is used to construct the JOIN clause.
- The entity's SPDX identifier column is referenced as the target column for the `apply_filter` call, allowing the filter to match against declared license values.
- When no `license` parameter is provided, the JOIN is omitted entirely, so there is zero performance impact on unfiltered queries.

**Why reuse is correct**: The `package_license` table and entity already exist in the codebase — they represent an established part of the data model. Creating a new entity, raw SQL query, or alternative join mechanism would be redundant and would diverge from the ORM-based query patterns used throughout the codebase.

**What is NOT done**: No new entity file is created. No database migration is needed. No raw SQL is written to perform the join — the existing entity's relation definitions handle this declaratively.

---

## Summary

| Reuse Candidate | Reuse Type | Benefit |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | Eliminates need for custom comma-parsing and SQL IN clause logic |
| `advisory/endpoints/list.rs` | Structural pattern | Ensures consistent endpoint architecture across modules |
| `entity/src/package_license.rs` | Entity/relation reference | Provides the JOIN table access without new schema work |

All three candidates are essential to the implementation. Together they ensure that the license filter feature requires only the minimal new code specific to the package-license domain — the query struct field, the service method parameter, and the integration tests — while all infrastructure concerns (parsing, SQL generation, entity mapping) are handled by existing, proven code.
