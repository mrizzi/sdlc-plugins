# Reuse Analysis: TC-9203

This document details how each Reuse Candidate identified in the task description is applied in the implementation.

## 1. `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a raw query string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace from each segment, and produces a SeaORM `Condition` with an `IN` clause matching any of the provided values.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` filter parameter is present, the raw string from the query parameter is passed directly to `apply_filter`. The returned condition is applied to the `license` column of the `package_license` table in the query builder. This avoids writing any new parsing logic for comma-separated values — the same function that powers multi-value filtering in other modules (such as the advisory severity filter) is called here with no modifications.

**Why reuse over new code**: Writing a custom comma-split-and-filter function would duplicate exactly what `apply_filter` already does. Using it directly ensures consistent behavior across all list endpoints (same trimming rules, same edge-case handling for empty segments, same SQL generation strategy) and reduces the surface area for bugs.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter using an optional field on a query parameters struct. The handler extracts the field, passes it to the service layer, and the service layer applies the filter using `apply_filter`. This is a complete, working example of the exact pattern needed for the license filter.

**How it is reused**: The advisory list endpoint is used as a **structural template** — not copied verbatim, but followed step-by-step:
1. The `PackageListQuery` struct in `modules/fundamental/src/package/endpoints/list.rs` gains an `Option<String>` field for `license`, mirroring how the advisory query struct has an `Option<String>` field for `severity`.
2. The handler function conditionally passes the license value to the service method, following the same conditional-pass pattern used in the advisory handler.
3. The service method applies the filter using `apply_filter`, matching the advisory service's approach.

This ensures the package license filter is structurally consistent with existing filters in the codebase, making it immediately familiar to other developers and reducing code review friction.

## 3. `entity/src/package_license.rs`

**What it provides**: A SeaORM entity definition for the `package_license` table, which maps packages to their declared licenses. This entity defines the table columns, the `Model` struct, and `Relation` definitions that connect it to other entities (notably `Package`).

**How it is reused**: In the `PackageService::list` method (`modules/fundamental/src/package/service/mod.rs`), when a license filter is active, the query joins through `package_license` using the existing SeaORM entity and its defined relations. This is done via SeaORM's `.join()` or `.find_also_related()` API, referencing `entity::package_license::Entity` and its relation to `entity::package::Entity`. The `apply_filter` condition is then applied to the `package_license` table's license column within this joined query.

**Why reuse over alternatives**: Writing a raw SQL JOIN would bypass SeaORM's type safety, relation validation, and query composition capabilities. Creating a new entity for the same table would introduce a redundant definition that could drift out of sync with the existing one. The `package_license` entity already encodes the correct table name, column names, and relations — using it directly is both safer and simpler.
