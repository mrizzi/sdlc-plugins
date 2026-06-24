# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description lists three Reuse Candidates. All three are used in the
implementation plan. No new utility functions are created that duplicate existing
functionality.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and
SQL `IN` clause generation. Given a raw query string like `"MIT,Apache-2.0"`, it splits
on commas, validates the tokens, and produces a SeaORM condition that filters rows
matching any of the provided values.

**How it is reused:** Called directly in `modules/fundamental/src/package/service/mod.rs`
to implement the license filtering logic. Instead of writing custom comma-splitting,
validation, or SQL generation code, the service method passes the raw `license` query
string and the target column (`package_license::Column::License`) to `apply_filter`,
which handles all parsing and clause generation.

**Why reuse is appropriate:** The license filter has identical semantics to the advisory
severity filter — both are optional string parameters that support comma-separated
multi-value matching. `apply_filter` was designed for exactly this pattern. Writing a
new parser or filter builder would duplicate this existing, tested utility.

**Integration point:** `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs`.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A complete reference implementation of an optional filter query
parameter on a list endpoint. The advisory list endpoint's `severity` filter demonstrates:
- How to declare an optional filter field in the endpoint's `Query` struct
- How to extract the filter value from query parameters via Axum's `Query` extractor
- How to pass the filter value from the endpoint handler to the service layer
- How to structure input validation for the filter parameter

**How it is reused:** Used as a structural template (not called directly) for the changes
to `modules/fundamental/src/package/endpoints/list.rs`. The package endpoint's `Query`
struct gains a `license: Option<String>` field following the same pattern as the advisory
endpoint's `severity: Option<String>` field. The handler function passes `query.license`
to `PackageService::list()` in the same way the advisory handler passes `query.severity`
to `AdvisoryService::list()`.

**Why reuse is appropriate:** The advisory severity filter is structurally identical to
the needed license filter — both are optional, comma-separated string parameters on list
endpoints that follow the module's `model/ + service/ + endpoints/` architecture. Following
this established pattern ensures consistency across the codebase and avoids inventing a
new approach for an already-solved problem.

**Integration point:** Pattern applied in `modules/fundamental/src/package/endpoints/list.rs`.

---

### 3. `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the package-license join table,
mapping packages to their declared SPDX license identifiers. Includes the entity's
columns (package ID, license identifier), relations (to the package table), and primary
key definition.

**How it is reused:** Used directly in the database query built by
`PackageService::list()` in `modules/fundamental/src/package/service/mod.rs`. When the
`license` filter is present, the service method adds an `INNER JOIN` to the
`package_license` table using the entity's relation definition:

```rust
query = query.join(
    JoinType::InnerJoin,
    entity::package_license::Relation::Package.def().rev(),
);
```

The entity's `Column::License` enum variant is passed to `apply_filter` to specify
which column the filter condition applies to.

**Why reuse is appropriate:** The `package_license` entity already encodes the schema
and relationships needed for the join. Using SeaORM's relation-based join API through
this entity is the standard approach in the codebase (as seen in other modules that
join through similar mapping tables). Writing raw SQL or redefining the join
relationship would bypass the ORM's type safety and duplicate the schema knowledge
already captured in the entity.

**Integration point:** Join and column reference in `modules/fundamental/src/package/service/mod.rs`.

---

## Summary

| Reuse Candidate | Reuse Type | Used In |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `package/service/mod.rs` |
| `advisory/endpoints/list.rs` | Structural pattern template | `package/endpoints/list.rs` |
| `entity/src/package_license.rs` | Direct entity reference (JOIN + column) | `package/service/mod.rs` |

All three Reuse Candidates are integral to the implementation. No new utility functions,
filter parsers, or query builders are created. The implementation follows the existing
patterns exactly, extending them to a new domain (license filtering) without duplication.
