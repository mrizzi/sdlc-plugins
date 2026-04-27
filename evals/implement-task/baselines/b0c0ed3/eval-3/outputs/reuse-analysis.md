# Reuse Analysis -- TC-9203: Add package license filter to list endpoint

## Overview

The task description provides three explicit Reuse Candidates. All three are directly applicable and must be used to avoid duplicating existing functionality (per constraint SS5.4 -- no duplication).

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Location**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. This is shared infrastructure already used across modules (advisory severity filtering, and likely SBOM filtering).

**How it will be reused**: The license filter requires exactly this behavior -- accepting a single value like `license=MIT` or a comma-separated list like `license=MIT,Apache-2.0` and converting it into a SQL `WHERE ... IN (...)` clause. Instead of writing new parsing or clause-building logic, the implementation will call `apply_filter` directly, passing the raw `license` query parameter string and the target column reference (`package_license::Column::License` or equivalent).

**Reuse mode**: Direct invocation -- no modification to `apply_filter` itself is needed. The function is generic over column/value types and already supports the comma-separated multi-value pattern.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Location**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter using a Query struct pattern. This struct has an optional `severity` field that, when present, is passed to the service layer for filtering. The endpoint deserializes query parameters into this struct via Axum's `Query` extractor.

**How it will be reused**: The license filter is structurally identical to the severity filter. The implementation will follow the same pattern:

1. **Query struct**: In `modules/fundamental/src/package/endpoints/list.rs`, add an `Option<String>` field named `license` to the existing `PackageListQuery` struct (or create one following the same shape as the advisory's query struct if none exists).
2. **Extraction**: Use Axum's `Query<PackageListQuery>` extractor in the handler signature, identical to how advisory's list handler extracts its query parameters.
3. **Delegation**: Pass the extracted `license` value down to `PackageService::list()`, mirroring how the advisory handler passes `severity` to `AdvisoryService::list()`.

**Reuse mode**: Pattern replication -- the advisory endpoint serves as a structural template. No code from the advisory module is imported; instead, the same architectural pattern is followed to maintain consistency across modules.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Location**: `entity/src/package_license.rs`

**What it provides**: The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the `Relation` to both the `package` table and the license identifiers.

**How it will be reused**: When building the filter query in `PackageService::list()`, the implementation will JOIN through the `package_license` entity rather than writing raw SQL. Specifically:

1. Use `package_license::Entity::find()` or join via SeaORM's `.find_also_related()` / `.join()` methods to link packages to their licenses.
2. Apply the filter condition on the license column of this entity using `apply_filter` from Candidate 1.
3. The entity's existing `Relation` definitions handle the JOIN conditions, so no manual `ON` clauses are needed.

**Reuse mode**: Direct usage of the existing entity and its relations -- no modification to `package_license.rs` is needed.

---

## Summary

| # | Candidate | Reuse Mode | Modification Required |
|---|---|---|---|
| 1 | `common/src/db/query.rs::apply_filter` | Direct invocation | None |
| 2 | `advisory/endpoints/list.rs` (severity filter pattern) | Pattern replication | None (template only) |
| 3 | `entity/src/package_license.rs` | Direct usage (JOIN entity) | None |

All three candidates are used. No new utility functions, query helpers, or entity definitions need to be created. The implementation is scoped entirely to the files listed in "Files to Modify" and "Files to Create".
