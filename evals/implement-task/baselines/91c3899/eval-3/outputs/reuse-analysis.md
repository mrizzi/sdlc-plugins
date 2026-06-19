# Reuse Analysis for TC-9203

## Summary

The task description provides 3 Reuse Candidates. All 3 are directly applicable and should be reused as-is. No new utility functions or duplicate logic should be created.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a raw query string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces the appropriate SQL filter (either a direct equality for single values or an `IN (...)` clause for multiple values).

**How it is reused:**

- In `modules/fundamental/src/package/endpoints/list.rs`: after extracting the optional `license` query parameter from the HTTP request, pass the raw string value to `apply_filter` to produce the database filter condition. This avoids writing any custom comma-splitting or SQL generation logic.
- In `modules/fundamental/src/package/service/mod.rs`: the service layer receives the parsed filter (produced by `apply_filter`) and applies it to the SeaORM query builder as a condition on the license identifier column.

**Why reuse instead of writing new code:** Writing a new function to split comma-separated values and build an `IN` clause would directly duplicate what `apply_filter` already does. The task's Implementation Notes explicitly state to use this function. Creating a separate utility would violate the DRY principle and diverge from the established pattern used by other endpoints (e.g., the advisory severity filter).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter using a Query struct pattern with an optional filter field. This is structurally identical to the license filter needed for the package endpoint. The pattern includes:
- A query parameters struct with an optional `severity: Option<String>` field
- Extraction of the query parameter in the Axum handler
- Passing the filter value to the corresponding service method
- Using `apply_filter` to handle the comma-separated parsing

**How it is reused:**

- The advisory list endpoint's Query struct pattern is followed as a template for adding the `license: Option<String>` field to the package endpoint's query parameters struct in `modules/fundamental/src/package/endpoints/list.rs`.
- The handler logic for extracting the optional parameter, checking if it is present, and forwarding it to the service layer follows the same control flow as the advisory severity filter.
- The error handling approach (returning 400 for invalid values) matches the advisory endpoint's pattern.

**Why reuse instead of inventing a new approach:** The advisory severity filter is a proven, reviewed pattern already in production. Following it ensures consistency across the codebase's list endpoints and reduces review friction. Inventing a different pattern for the same type of operation would create unnecessary divergence between sibling endpoints.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the `package_license` join table. This entity maps the many-to-many relationship between packages and licenses, providing:
- Column definitions for the join table (package ID, license identifier)
- SeaORM `Relation` definitions connecting to the `package` and license tables
- The entity struct and model needed for type-safe query building

**How it is reused:**

- In `modules/fundamental/src/package/service/mod.rs`: when the `license` filter is present, the service builds a SeaORM query that JOINs the `package` table with the `package_license` table using the entity's defined relations. The join condition uses the entity's column definitions (e.g., `package_license::Column::PackageId` and `package_license::Column::LicenseIdentifier` or equivalent).
- The `IN` clause filter (produced by `apply_filter`) is applied to the appropriate column from `package_license::Column`, ensuring type-safe filtering through the ORM rather than raw SQL strings.

**Why reuse instead of writing raw SQL:** The entity already encodes the table schema, column names, and relations. Using it with SeaORM's query builder provides compile-time type safety, automatic escaping, and consistency with how every other join query in the codebase is written. Writing raw SQL would bypass these safeguards and diverge from the project's ORM-first convention.

---

## Reuse Coverage Summary

| # | Reuse Candidate | Location | Used In | Purpose |
|---|---|---|---|---|
| 1 | `apply_filter` | `common/src/db/query.rs` | `list.rs`, `service/mod.rs` | Comma-separated multi-value parsing and SQL IN clause generation |
| 2 | Advisory severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | `list.rs` | Query struct pattern with optional filter field, handler control flow |
| 3 | `package_license` entity | `entity/src/package_license.rs` | `service/mod.rs` | JOIN query through the package-license mapping table |

All 3 Reuse Candidates are applied. No new utility functions are created that would duplicate existing functionality.
