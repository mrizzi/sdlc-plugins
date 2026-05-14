# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is used in the implementation plan. The guiding principle is to reuse existing code directly and avoid creating new utilities that duplicate functionality already present in the codebase.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw string value (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces a SeaORM condition that filters rows whose column value is in the resulting set.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, the service layer calls `apply_filter` directly, passing the raw comma-separated license string and the target column (the SPDX identifier column from the `package_license` entity). This handles both the single-value case (`?license=MIT`) and the multi-value case (`?license=MIT,Apache-2.0`) without any new parsing code.

**What is NOT done**: No new string-splitting logic, no new comma-parsing utility, and no custom SQL `IN` clause builder is created. `apply_filter` already handles all of this.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter using a Query struct pattern. The struct has an `Option<String>` field for the filter value, the handler extracts it from the query string via Axum's `Query` extractor, and passes it to the advisory service's list method. This is the established pattern in the codebase for optional list-endpoint filters.

**How it is reused**: The package list endpoint (`modules/fundamental/src/package/endpoints/list.rs`) follows the same structural pattern:
1. An optional `license: Option<String>` field is added to the existing Query struct, mirroring how `severity: Option<String>` is declared in the advisory Query struct.
2. The handler extracts the value via Axum's `Query` extractor in the same way.
3. The value is passed to `PackageService::list()` as an additional parameter, following the same calling convention used for the advisory service's severity filter.

**What is NOT done**: No new query-parameter extraction mechanism, custom deserializer, or alternative struct pattern is invented. The advisory endpoint's pattern is followed exactly.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity for the `package_license` join table, which maps packages to their declared licenses. This entity defines the schema, relations, and column types needed to query the package-license relationship.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when applying the license filter, the query JOINs through the `package_license` entity using SeaORM's relation-based join API. The entity's `Column` enum provides the SPDX identifier column that is passed to `apply_filter` for the `IN` clause. The entity's defined `Relation` to the `package` table enables the JOIN without raw SQL.

**What is NOT done**: No raw SQL JOIN statements are written. No new entity or migration is created. The existing `package_license` entity is sufficient for the filter query.

---

## Summary Table

| Reuse Candidate | Location | Reuse Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | `package/service/mod.rs` -- filter logic |
| Advisory list severity pattern | `advisory/endpoints/list.rs` | Structural pattern (Query struct + handler flow) | `package/endpoints/list.rs` -- query parameter extraction |
| `package_license` entity | `entity/src/package_license.rs` | SeaORM entity for JOIN | `package/service/mod.rs` -- join to license table |

All three Reuse Candidates are used. No new utility functions or abstractions are introduced that would duplicate existing functionality.
