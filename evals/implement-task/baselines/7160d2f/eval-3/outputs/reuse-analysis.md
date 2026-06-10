# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description lists three Reuse Candidates. All three are used in this implementation.
No new code is written that duplicates their functionality.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN
clause generation. Accepts a string like `"MIT,Apache-2.0"`, splits on commas, and produces
the appropriate SQL `WHERE column IN (...)` clause for SeaORM queries.

**How it is reused:**

In `modules/fundamental/src/package/service/mod.rs`, the `list` method receives the raw
`license` query parameter string from the endpoint layer. Instead of writing custom
comma-splitting or SQL filter logic, it calls `apply_filter` directly:

```rust
// In PackageService::list()
if let Some(license) = license_filter {
    apply_filter(&mut query, "license", &license);
}
```

This reuses `apply_filter` exactly as it was designed -- no wrapper, no duplication. The
function already handles:
- Single-value input (`"MIT"` -> `WHERE license = 'MIT'`)
- Multi-value comma-separated input (`"MIT,Apache-2.0"` -> `WHERE license IN ('MIT', 'Apache-2.0')`)
- Edge cases in parsing (whitespace trimming, empty segments)

**Why reuse over reimplementation:** Writing custom comma-splitting and IN-clause generation
would duplicate 100% of what `apply_filter` already does. The function exists precisely for
this use case. Reimplementing it would create a maintenance burden (two implementations to
keep in sync) and risk inconsistent behavior with other filter endpoints.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A structurally identical filter implementation on the advisory list
endpoint. The advisory endpoint has a Query struct with an optional `severity` field, extracts
it from query parameters, and passes it to the advisory service for filtering. This serves as
the reference pattern for the license filter.

**How it is reused:**

The advisory endpoint's pattern is followed as the structural template for the package
endpoint changes. Specifically:

1. **Query struct pattern**: The package endpoint's Query struct in
   `modules/fundamental/src/package/endpoints/list.rs` gets a new `license: Option<String>`
   field, following the exact same pattern as the advisory endpoint's `severity: Option<String>`
   field.

2. **Handler extraction pattern**: The handler function extracts `query.license` and passes it
   to the service layer, mirroring how the advisory handler extracts `query.severity` and passes
   it to `AdvisoryService::list()`.

3. **Service integration pattern**: The service method signature and filter application follow the
   same structure as the advisory service -- accepting an optional filter string parameter and
   conditionally applying it via `apply_filter`.

**Why reuse over reimplementation:** The advisory severity filter is the established convention
for adding query parameter filters to list endpoints in this codebase. Following this pattern
ensures consistency across modules, makes the code instantly recognizable to anyone familiar
with the advisory endpoint, and avoids inventing a new filtering approach that would diverge
from existing conventions.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The SeaORM entity definition for the `package_license` table, which maps
packages to their licenses (a join/association table). This entity defines the table columns,
primary keys, and relations to the `package` entity.

**How it is reused:**

In `modules/fundamental/src/package/service/mod.rs`, the license filter query uses the
`package_license` entity to perform the JOIN between the `package` table and the
`package_license` table:

```rust
// In PackageService::list() -- conceptual
use entity::package_license;

query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
// Then apply_filter on the license column from the joined table
```

The existing entity is used directly for:
- Defining the JOIN relationship (using SeaORM's relation definitions from the entity)
- Referencing the license column for the WHERE clause filter
- Leveraging SeaORM's type-safe column references instead of raw SQL strings

**Why reuse over reimplementation:** The entity already defines the table schema, columns,
and relations in SeaORM's type-safe model. Writing raw SQL JOINs would bypass SeaORM's
relation system, lose type safety, and diverge from how every other entity relationship is
queried in the codebase. Using the existing entity ensures the JOIN is consistent with
SeaORM conventions and benefits from any future schema migrations applied to the entity.

---

## Additional Reuse Opportunities Discovered

Beyond the three listed Reuse Candidates, the implementation leverages these existing
components:

| Component | Location | How Reused |
|---|---|---|
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Response wrapper for the list endpoint -- already used by `PackageService::list()`, no changes needed |
| `AppError` | `common/src/error.rs` | Error type for 400 Bad Request on invalid license values -- already the standard error type for all handlers |
| Test patterns | `tests/api/advisory.rs`, `tests/api/sbom.rs` | Assertion patterns, test setup, and naming conventions reused in the new test file |

## Reuse Summary

| Reuse Candidate | Action | Duplication Avoided |
|---|---|---|
| `apply_filter` | Called directly from service layer | Comma-separated parsing + SQL IN clause generation |
| Advisory severity filter pattern | Followed as structural template for endpoint + service changes | Query struct design, handler extraction, service integration |
| `package_license` entity | Used for SeaORM JOIN in service query | Raw SQL JOIN logic, table/column name hardcoding |

**No new utility code was written.** All filtering logic delegates to existing shared
infrastructure (`apply_filter`). All query construction uses existing entities
(`package_license`). All structural decisions follow the established advisory filter pattern.
