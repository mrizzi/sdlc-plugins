# Reuse Analysis: TC-9203 — Add Package License Filter to List Endpoint

## Reuse Candidates from Task Description

The task description lists three reuse candidates. All three are used in the
implementation plan. No new utility functions are created that duplicate existing
functionality.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and
SQL IN clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas,
produces individual values, and generates the appropriate SQL `WHERE column IN (...)`
clause for SeaORM queries.

**How it is reused:** Called directly in `modules/fundamental/src/package/service/mod.rs`
within the `PackageService::list()` method. When the `license` query parameter is
present (`Some`), `apply_filter` is invoked with the raw license string and the target
column (the license identifier column from the `package_license` table). This handles
both single-value (`license=MIT`) and multi-value (`license=MIT,Apache-2.0`) cases
without writing any custom parsing or SQL generation logic.

**Why reuse is correct:** The `apply_filter` function is the project's standard mechanism
for optional multi-value query parameter filtering. The advisory module's severity filter
already uses it for the same purpose. Writing custom comma-splitting or IN clause logic
would duplicate this existing, tested utility.

**Alternative considered and rejected:** Writing a custom `parse_license_filter` function
that splits on commas and builds the query. Rejected because `apply_filter` already does
exactly this, and introducing a parallel implementation would create duplication and
diverge from the established pattern.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (Severity Filter Pattern)

**What it provides:** A complete, working example of how to add an optional filter
query parameter to a list endpoint in the trustify-backend architecture. The advisory
list endpoint supports a `severity` query parameter using a Query struct with an
`Option<String>` field, which is then passed to the service layer for filtering.

**How it is reused:** The structural pattern is replicated in the package list endpoint:

1. **Query struct pattern:** The advisory endpoint defines a Query struct (or extends a
   shared one) with `severity: Option<String>`. The package endpoint follows the same
   pattern, adding `license: Option<String>` to its Query struct.

2. **Handler-to-service parameter passing:** The advisory handler extracts
   `query.severity` and passes it to `AdvisoryService::list()`. The package handler
   follows the same pattern, extracting `query.license` and passing it to
   `PackageService::list()`.

3. **Service-layer filter application:** The advisory service calls `apply_filter`
   with the severity value. The package service follows the same pattern, calling
   `apply_filter` with the license value.

**Why reuse is correct:** The advisory severity filter and the package license filter
are structurally identical features — both add an optional query parameter to a list
endpoint, both support comma-separated multi-value filtering, and both apply the filter
at the service layer using `apply_filter`. Following the existing pattern ensures
consistency across the codebase and reduces review friction.

**What is NOT copied:** The actual column being filtered and the JOIN logic differ.
The advisory filter operates on a column directly on the advisory entity, whereas the
license filter requires a JOIN through the `package_license` table. This is the only
structural difference and is handled by adding a SeaORM join in the package service
query builder.

---

### 3. `entity/src/package_license.rs` (Package-License Entity)

**What it provides:** The SeaORM entity definition for the `package_license` join table
that maps packages to their declared licenses. This entity defines the table columns,
relationships, and types needed for constructing JOINs between packages and licenses.

**How it is reused:** Used in `modules/fundamental/src/package/service/mod.rs` to build
the JOIN query. Instead of writing raw SQL like
`JOIN package_license ON package.id = package_license.package_id`, the implementation
uses SeaORM's type-safe join API with the `package_license` entity:

```rust
// Conceptual usage (exact API depends on SeaORM version):
query.join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())
     .filter(entity::package_license::Column::License.is_in(license_values))
```

**Why reuse is correct:** The entity already exists and defines the correct table
structure, column names, and relationships. Using it provides type-safe column references
and relationship definitions. Writing raw SQL or re-defining the join table mapping would
bypass SeaORM's type safety and duplicate the entity definition.

---

## Summary Table

| Reuse Candidate | Location | How Reused | Avoids Duplication Of |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Called directly for comma-separated filter parsing and SQL IN clause generation | Custom comma-splitting logic and SQL IN clause construction |
| Severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern replicated: Query struct with Optional field, handler-to-service pass-through, service-layer filter application | Inventing a new filtering architecture that diverges from the established pattern |
| PackageLicense entity | `entity/src/package_license.rs` | Used for type-safe JOIN in the service query builder | Raw SQL JOINs or duplicated table/column definitions |

## New Code Created

No new utility functions, helpers, or shared modules are created. All filtering logic
is implemented by composing existing components:

- `apply_filter` handles parsing and SQL generation
- `package_license` entity handles the JOIN definition
- The advisory severity filter pattern provides the architectural blueprint

The only new code is:
- An additional field (`license: Option<String>`) on the package Query struct
- An additional parameter and filter call in `PackageService::list()`
- Integration tests in `tests/api/package_license_filter.rs`

None of this duplicates existing functionality.
