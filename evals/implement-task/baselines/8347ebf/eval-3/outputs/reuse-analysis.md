# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is used in the implementation plan. The guiding principle is "reuse first" — no new utility functions are created that duplicate existing functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation. When given a raw query string like `"MIT,Apache-2.0"` and a target column, it:
- Splits the string on commas to produce individual filter values
- Generates a SQL `IN` clause for multiple values (e.g., `WHERE license IN ('MIT', 'Apache-2.0')`)
- Generates a simple equality clause for single values (e.g., `WHERE license = 'MIT'`)

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method calls `apply_filter` directly with the `license` column from the `package_license` entity and the raw comma-separated string received from the endpoint handler. This is exactly the function's intended use case.

**What is NOT done:** No new parsing function, utility, or helper is created for splitting comma-separated values or building IN clauses. The `apply_filter` function handles this entirely. Writing a new `parse_license_filter()` or `split_comma_values()` function would duplicate `apply_filter`'s existing functionality and is explicitly avoided.

**Location of reuse in plan:** `modules/fundamental/src/package/service/mod.rs` — the service layer query building section.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A structurally identical implementation of a query parameter filter on a list endpoint. The advisory list endpoint defines a Query struct with an optional `severity` field, extracts it from the HTTP request, and passes it to the advisory service layer for filtering. This pattern is the template for the license filter.

**How it is reused:** The implementation follows the same structural pattern in `modules/fundamental/src/package/endpoints/list.rs`:

1. **Query struct pattern:** An `Option<String>` field named `license` is added to the package endpoint's query parameter struct, mirroring how `severity` is defined as `Option<String>` in the advisory query struct.

2. **Handler pattern:** The handler function extracts the `license` value from the deserialized query struct and passes it to the service method, exactly as the advisory handler extracts `severity` and passes it to `AdvisoryService`.

3. **Service integration pattern:** The service method accepts the optional filter parameter and conditionally applies it to the database query, following the same conditional logic pattern used in the advisory service.

**What is NOT done:** No new endpoint design pattern or query parameter handling approach is invented. The advisory severity filter is the proven, reviewed pattern in this codebase for optional comma-separated list filters, and the license filter replicates it exactly.

**Location of reuse in plan:** 
- `modules/fundamental/src/package/endpoints/list.rs` — query struct definition and handler logic
- `modules/fundamental/src/package/service/mod.rs` — service method signature and conditional filter application

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the package-license join table. This entity maps the relationship between packages and their declared licenses, providing the column definitions and relation metadata needed for SeaORM JOIN queries.

**How it is reused:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` filter is present, the service method uses SeaORM's join API to join the `package` table with `package_license` using the entity's defined relations. The license column from `package_license` is then used as the target column for `apply_filter`.

Specifically:
- The `package_license` entity's `Column::LicenseId` (or equivalent column enum variant) is used in the `apply_filter` call
- The `package_license` entity's relation to the `package` entity is used for the SeaORM JOIN clause
- No raw SQL is written for the join — the entity's relation metadata handles this declaratively

**What is NOT done:** No raw SQL JOIN statements are written. No new entity or model is created for the package-license relationship. The existing `package_license` entity provides everything needed for the filtered query.

**Location of reuse in plan:** `modules/fundamental/src/package/service/mod.rs` — the JOIN query construction section.

---

## Summary Table

| Reuse Candidate | Source Location | Reuse Location | Reuse Type |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | `package/service/mod.rs` | Direct function call for comma-separated parsing and SQL IN clause |
| Severity filter pattern | `advisory/endpoints/list.rs` | `package/endpoints/list.rs`, `package/service/mod.rs` | Structural pattern replication (query struct, handler, service integration) |
| `package_license` entity | `entity/src/package_license.rs` | `package/service/mod.rs` | Entity reuse for JOIN query (columns and relations) |

## Anti-Patterns Avoided

1. **No new `parse_comma_separated()` utility** — `apply_filter` already handles this
2. **No new query builder wrapper** — the existing query helpers in `common/src/db/query.rs` are sufficient
3. **No raw SQL** — SeaORM entities and `apply_filter` provide type-safe query construction
4. **No new filter pattern** — the advisory severity filter pattern is followed exactly rather than inventing a new approach
5. **No modification to shared code** — `apply_filter`, `package_license` entity, and `PaginatedResults` are all used as-is without modification
