# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces the appropriate filter condition for use in SeaORM queries.

**How it would be reused:** Call `apply_filter` directly in `PackageService::list()` when the `license` parameter is `Some`. Pass the raw query string value from the endpoint handler. This eliminates the need to write any custom comma-splitting or SQL `IN` clause generation logic.

**Reuse type:** Direct invocation — no modification to the existing function is needed. The function is generic enough to handle any string-valued filter parameter.

**Without reuse, we would need to:** Write custom logic to split the comma-separated license string, sanitize each value, and construct a SeaORM `Condition` with `col.is_in(values)`. This would duplicate the exact logic already in `apply_filter`.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A reference implementation of query parameter filtering on a list endpoint. The advisory endpoint accepts an optional `severity` query parameter in its `Query` struct, extracts it in the handler, passes it to the service layer, and the service uses `apply_filter` to build the database query. This is structurally identical to the license filter needed for the package endpoint.

**How it would be reused:** Follow the same structural pattern — not code reuse by import, but pattern reuse by convention:

1. **Query struct pattern:** Add an `Option<String>` field named `license` to the package endpoint's query parameter struct, mirroring how `severity: Option<String>` is declared in the advisory endpoint's query struct.

2. **Handler pattern:** In the list handler function, extract `query.license` and pass it to the service method, mirroring how the advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`.

3. **Service pattern:** In `PackageService::list()`, accept the license parameter and conditionally apply the filter using `apply_filter`, mirroring the advisory service's conditional severity filter application.

**Reuse type:** Structural/pattern reuse — the advisory implementation serves as the template. Following this pattern ensures consistency across endpoints and makes the codebase predictable for future developers.

**Without reuse, we would need to:** Design the parameter extraction, handler flow, and service integration from scratch, risking inconsistency with established patterns (different parameter naming conventions, different error handling, different service method signatures).

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity includes the relation definitions needed to join the `package` table with license data.

**How it would be reused:** Use this entity in the `PackageService::list()` query to perform the JOIN between packages and their licenses. Specifically:

1. Use the entity's `Relation` definitions to add a `.join()` clause to the SeaORM query builder, joining the package query with the `package_license` table.
2. Apply the license filter condition (from `apply_filter`) on the license identifier column defined in this entity.
3. This keeps all database queries using SeaORM's type-safe API rather than raw SQL strings.

**Reuse type:** Direct entity usage — the entity already exists and defines the exact table structure and relations needed for the join. No modification to the entity is required.

**Without reuse, we would need to:** Write raw SQL JOIN clauses or define ad-hoc join logic, bypassing SeaORM's type safety and relation management. This would be inconsistent with how other modules perform joins and would not benefit from any future schema changes reflected in the entity definitions.

---

## Summary

| Reuse Candidate | Reuse Type | Avoids Duplicating |
|---|---|---|
| `apply_filter` in `common/src/db/query.rs` | Direct invocation | Comma-separated parsing, SQL IN clause generation |
| Advisory severity filter in `advisory/endpoints/list.rs` | Structural pattern | Query struct design, handler-to-service flow, conditional filter application |
| `package_license` entity in `entity/src/package_license.rs` | Direct entity usage | Raw SQL joins, manual table/column references |

All three reuse candidates are used. No new utility functions or helpers are created that would duplicate existing functionality.
