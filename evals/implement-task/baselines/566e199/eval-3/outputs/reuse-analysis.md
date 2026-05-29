# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document analyzes all three Reuse Candidates listed in the task description and
describes how each is used in the implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Task description:** "handles comma-separated multi-value query parameter parsing and SQL
IN clause generation; reuse directly for the license filter"

**How it is reused:**

The `apply_filter` function is called directly in `modules/fundamental/src/package/endpoints/list.rs`
to parse the `license` query parameter value. When a user provides `?license=MIT,Apache-2.0`,
`apply_filter` splits the comma-separated string into individual values and generates the
appropriate SQL `IN` clause (e.g., `WHERE license_id IN ('MIT', 'Apache-2.0')`). For a
single value like `?license=MIT`, it produces a simple equality condition.

**Why reuse instead of new code:** Writing new parsing logic for comma-separated query
parameters would duplicate functionality that `apply_filter` already provides. The function
is the established, shared utility for this pattern across the codebase (used by the
advisory severity filter and other endpoints). Reusing it ensures consistent behavior,
avoids bugs from reimplementing string splitting and SQL generation, and keeps the
codebase DRY.

**No new utility functions are created** that would duplicate `apply_filter` functionality.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Task description:** "the severity filter implementation is structurally identical to the
license filter needed here; follow the same Query struct pattern with an optional field"

**How it is reused:**

The advisory list endpoint serves as the structural template for the package license filter
implementation. Specifically, the implementation follows its pattern in three ways:

1. **Query struct pattern**: The advisory endpoint defines a query parameter struct with an
   optional `severity` field. The package endpoint's query struct is extended with an
   analogous optional `license` field using the same type annotation and serde attributes.

2. **Handler wiring**: The advisory handler extracts the severity filter from the query
   struct and passes it to the service layer. The package handler follows the same flow:
   extract the `license` value from the query struct, call `apply_filter` to parse it,
   and pass the result to `PackageService::list()`.

3. **Service call pattern**: The advisory handler's call to `AdvisoryService::list()` with
   the filter parameter establishes the pattern for how `PackageService::list()` receives
   and applies the license filter.

**Why reuse this pattern:** The severity filter in the advisory endpoint is structurally
identical to the license filter needed for packages. Following the same pattern ensures
consistency across modules, makes the codebase predictable for maintainers, and reduces
the risk of introducing unconventional approaches.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Task description:** "existing entity for the package-license join table; use for the
JOIN query rather than writing raw SQL"

**How it is reused:**

The `package_license` SeaORM entity is used in `modules/fundamental/src/package/service/mod.rs`
to build the JOIN query that connects packages to their declared licenses. When the license
filter is active, the service method joins the `package` table to the `package_license`
table using SeaORM's relation/join API (e.g., `find().join()` or equivalent), then applies
the filter condition on the license column from the `package_license` entity.

**Why reuse instead of raw SQL:** The `package_license` entity already defines the table
schema, column types, and relationships in SeaORM's type-safe model layer. Using it for
the JOIN provides:

- **Type safety**: Column references are checked at compile time, preventing typos in table
  or column names.
- **Consistency**: All other cross-entity queries in the codebase use SeaORM entities for
  JOINs (e.g., `sbom_package.rs` for SBOM-to-package relationships, `sbom_advisory.rs`
  for SBOM-to-advisory relationships).
- **Maintainability**: If the `package_license` table schema changes (e.g., column rename),
  the SeaORM entity update propagates to all query sites via compile errors, whereas raw
  SQL would silently break at runtime.

No new entity is created for this relationship, and no raw SQL is written.

---

## Summary

| Reuse Candidate | Location | Reuse Type | New Code Avoided |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | Comma-separated parsing and SQL IN clause generation |
| Advisory list endpoint | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern (template) | Query struct design, handler wiring, service call flow |
| `package_license` entity | `entity/src/package_license.rs` | SeaORM JOIN via existing entity | Raw SQL JOIN query, new entity definition |

All three Reuse Candidates from the task description are used. No new utility functions
or entities are created that would duplicate existing functionality.
