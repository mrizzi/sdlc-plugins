# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details how each Reuse Candidate listed in the task description would be
used during implementation, following the skill's "Reuse first" principle from Step 6.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles comma-separated multi-value
query parameter parsing and SQL `IN` clause generation. It takes a string value
(e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SQL
predicate — a direct equality check for single values or an `IN (...)` clause for
multiple values.

**How it would be reused:** This function is reused **directly** in
`modules/fundamental/src/package/service/mod.rs` when building the license filter
query. Instead of writing custom comma-splitting and SQL generation logic, the
service layer calls `apply_filter` with the raw license query parameter value and
the target column (the license identifier column from the `package_license` entity).

**Reuse type:** Direct invocation — no modification to `apply_filter` is needed.
The function's existing signature and behavior exactly match the requirements for
license filtering (comma-separated input, SQL IN output).

**Benefit:** Eliminates the need to write and test custom parameter parsing logic.
The `apply_filter` function is already tested and handles edge cases (single value,
multiple values, whitespace trimming). Using it ensures consistency with how other
filters in the codebase (e.g., the advisory severity filter) handle multi-value
parameters.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint already implements a `severity` query
parameter filter using an optional field on the query parameters struct. This
implementation demonstrates the established pattern for adding optional filters to
list endpoints in this codebase:

1. Define an `Option<String>` field on the query parameter struct with `#[serde(default)]`.
2. Extract the field value in the handler function.
3. Pass it to the corresponding service method.
4. The service uses `apply_filter` to generate the SQL predicate.

**How it would be reused:** The structural pattern from the advisory severity filter
is followed as a **template** for the license filter implementation. Specifically:

- In `modules/fundamental/src/package/endpoints/list.rs`: the query parameter struct
  gains a `license: Option<String>` field with the same serde attributes used by the
  advisory endpoint's `severity` field. The handler extraction and service invocation
  follow the same flow.

- In `modules/fundamental/src/package/service/mod.rs`: the service method's filter
  application mirrors how `AdvisoryService::list` applies the severity filter — calling
  `apply_filter` on the appropriate column when the parameter is `Some`.

**Reuse type:** Structural pattern reuse (template). The advisory endpoint code is not
called or imported; rather, its architecture is replicated for the package endpoint to
maintain consistency across the codebase.

**Benefit:** Ensures the license filter implementation is architecturally consistent
with existing filters in the codebase. Developers familiar with the advisory severity
filter will immediately understand the license filter. Reduces design decisions and
potential for introducing non-standard patterns.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the `package_license` join table,
which maps packages to their declared licenses. This entity provides typed access to the
join table's columns (package ID, license identifier) through SeaORM's model/entity
pattern, enabling type-safe query building.

**How it would be reused:** This entity is reused **directly** in
`modules/fundamental/src/package/service/mod.rs` to perform the JOIN between the
`package` table and the `package_license` table when the license filter is active.

Instead of writing raw SQL like:
```sql
SELECT p.* FROM package p
JOIN package_license pl ON p.id = pl.package_id
WHERE pl.license IN ('MIT', 'Apache-2.0')
```

The implementation uses SeaORM's query builder with the `package_license` entity:
```rust
// Pseudocode showing the pattern
query.join(JoinType::InnerJoin, package_license::Relation::Package.def())
     .filter(package_license::Column::License.is_in(license_values))
```

**Reuse type:** Direct usage — the entity is imported and used in query construction.
No modifications to the entity definition are needed.

**Benefit:** Avoids raw SQL, maintains type safety, and follows the SeaORM patterns
used throughout the codebase. If the `package_license` table schema changes (e.g.,
column rename), the entity's migration will update the generated code, and the
compiler will catch any breakage — something raw SQL strings would miss.

---

## Additional Reuse Discovered During Analysis

### `common/src/error.rs` — `AppError` enum

While not listed as a Reuse Candidate in the task, the `AppError` enum from
`common/src/error.rs` would be reused for input validation error responses. When the
license parameter is provided but invalid (e.g., empty string after parsing), the
handler returns an `AppError` variant that maps to HTTP 400 Bad Request. This follows
the same error handling pattern used by all other handlers in the codebase
(`Result<T, AppError>` with `.context()` wrapping).

### `common/src/model/paginated.rs` — `PaginatedResults<T>`

The response type `PaginatedResults<PackageSummary>` is already used by the existing
package list endpoint and remains unchanged. No new response types are needed — the
filter only changes which items are included in the existing paginated response.

---

## Summary

| Reuse Candidate | Reuse Type | Location Used |
|---|---|---|
| `apply_filter` (query.rs) | Direct invocation | `package/service/mod.rs` — filter query building |
| Advisory list endpoint pattern | Structural template | `package/endpoints/list.rs` — query struct and handler flow |
| `package_license` entity | Direct usage | `package/service/mod.rs` — JOIN query construction |
| `AppError` enum | Direct usage (discovered) | `package/endpoints/list.rs` — validation error responses |
| `PaginatedResults<T>` | Existing usage (unchanged) | `package/endpoints/list.rs` — response type |

All three listed Reuse Candidates are used. No new utility functions or shared modules
need to be created. The implementation composes existing building blocks rather than
introducing duplicated logic.
