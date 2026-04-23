# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Summary

All three Reuse Candidates identified in the task description are used directly.
No new parsing utilities, helper functions, or raw SQL are written. The implementation
is entirely assembled from existing building blocks.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:**

`apply_filter` accepts a SeaORM column reference and a raw query-parameter string
and returns a SeaORM `Condition` representing an SQL IN clause. It handles:

- Single-value strings: produces `column = 'value'` (or equivalent single-item IN).
- Comma-separated multi-value strings: splits on `,`, trims whitespace, and produces
  `column IN ('value1', 'value2', …)`.

**Where it is used in this task:**

Inside `modules/fundamental/src/package/service/mod.rs`, within the `list` method,
when `license: Option<String>` is `Some`:

```
// In PackageService::list, after constructing the base select:
if let Some(ref license_param) = license {
    let condition = apply_filter(package_license::Column::LicenseId, license_param);
    query = query
        .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
        .filter(condition);
}
```

**Why no new parsing logic is written:**

The task description explicitly calls out this function for reuse ("reuse directly for
the license filter"). Writing a new comma-splitting implementation would duplicate
`apply_filter`'s behavior and violate the skill's "Reuse first" rule (Step 6) and the
"Duplication check" in Step 9. There is no gap between what `apply_filter` provides and
what the license filter needs.

**Acceptance criteria satisfied by this reuse:**

- "GET /api/v2/package?license=MIT returns only packages with MIT license" — covered
  by the single-value path of `apply_filter`.
- "GET /api/v2/package?license=MIT,Apache-2.0 returns packages matching either license"
  — covered by the multi-value (comma-separated) path of `apply_filter`.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**

The advisory list endpoint implements a `severity` query parameter using a pattern
that is structurally identical to what the license filter requires:

1. A query struct with an `Option<String>` field for the filter value:
   ```
   struct ListQuery {
       // ... pagination/search fields ...
       severity: Option<String>,
   }
   ```
2. An Axum `Query<ListQuery>` extractor in the handler function signature.
3. Forwarding the extracted `Option<String>` to the service layer.
4. The service layer calling `apply_filter` on the value when `Some`.

**Where the pattern is followed in this task:**

In `modules/fundamental/src/package/endpoints/list.rs`:

- The existing query struct is extended with `license: Option<String>`, following the
  same `Option<String>` field shape used for `severity` in the advisory endpoint.
- The handler forwards `params.license` to `PackageService::list`, following the same
  forwarding convention.

In `modules/fundamental/src/package/service/mod.rs`:

- The service-layer filter application mirrors the advisory service's severity filter
  pattern: check `Option`, call `apply_filter`, attach to query builder.

**Why this pattern is followed instead of inventing a new approach:**

The advisory and package endpoints are sibling domain modules in
`modules/fundamental/src/`. Convention conformance analysis (Step 4 of the skill)
requires examining sibling files to identify recurring patterns. The severity filter
is the closest existing analog. Using the same pattern ensures:

- Consistency: consumers of the codebase encounter the same idiom across list endpoints.
- Correctness: the pattern is already tested and proven in production.
- Reviewability: a human reviewer can immediately recognize the pattern and verify the
  implementation by comparison to the advisory endpoint.

**No new patterns are invented.** No custom middleware, no filter DSL, no bespoke
query builder abstraction.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:**

`entity/src/package_license.rs` is the SeaORM entity for the `package_license`
join table that maps packages to their declared licenses. It provides:

- A typed `Column` enum (including `LicenseId` or equivalent) for use in filter
  and JOIN expressions.
- A `Relation` enum that defines the foreign-key relationship back to the `package`
  entity, enabling SeaORM's type-safe JOIN API.
- The entity model struct for row deserialization.

**Where it is used in this task:**

In `modules/fundamental/src/package/service/mod.rs`:

```
use entity::package_license;

// Inside PackageService::list, when license filter is active:
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(apply_filter(package_license::Column::LicenseId, license_param));
```

The entity's `Column::LicenseId` is passed directly to `apply_filter` as the column
reference. The entity's `Relation::Package` is used for the JOIN definition.

**Why the entity is used instead of raw SQL or a new entity:**

- The task description explicitly states: "Use the `package_license` entity in
  `entity/src/package_license.rs` for the JOIN query rather than writing raw SQL or
  creating a new entity."
- The existing entity already encodes the schema and relationships. Creating a new
  entity would duplicate schema knowledge and diverge from the SeaORM conventions
  used across the codebase (e.g., `entity::sbom_advisory`, `entity::sbom_package` are
  used the same way in their respective service files).
- Raw SQL would bypass SeaORM's type safety and break the convention that all
  database access uses the ORM layer.

**No changes are made to `entity/src/package_license.rs` itself.** The entity file
is in-scope only for reading; it is not listed in "Files to Modify" and is used as-is.

---

## Reuse Coverage Matrix

| Reuse Candidate | Used In | Usage Type |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | `modules/fundamental/src/package/service/mod.rs` | Direct function call; handles all comma-separated parsing and IN-clause generation |
| `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern) | `modules/fundamental/src/package/endpoints/list.rs` and `service/mod.rs` | Structural pattern followed for Query struct shape, extractor usage, and service forwarding |
| `entity/src/package_license.rs` | `modules/fundamental/src/package/service/mod.rs` | SeaORM entity used for typed JOIN and column reference in filter |

All three candidates are covered. No functionality duplicating any of the three is
introduced anywhere in the implementation.
