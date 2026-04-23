# Reuse Analysis -- TC-9203: Add package license filter to list endpoint

This document analyzes each of the three Reuse Candidates identified in the task description and describes exactly how each would be reused in the implementation.

---

## 1. `common/src/db/query.rs::apply_filter`

**What it provides:** `apply_filter` is a shared utility function that handles comma-separated multi-value query parameter parsing and SQL filter generation. When given a string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and generates the appropriate SQL clause -- an `=` condition for single values or an `IN (...)` clause for multiple values. It handles edge cases such as empty strings, trailing commas, and whitespace padding.

**How it is reused:** The `PackageService` list method calls `apply_filter` directly with the raw `license` query parameter string and the target column (the license identifier column from the `package_license` table). `apply_filter` returns the query condition, which is applied to the SeaORM query builder.

**What is NOT done:** No new parsing function is written. There is no manual `.split(',')` call, no custom `IN` clause builder, and no new filtering utility. The entire parsing-and-SQL-generation pipeline is delegated to the existing `apply_filter` function. Writing a new `parse_license_filter` or `build_license_clause` function would duplicate `apply_filter`'s exact responsibility and is explicitly avoided.

**Why this reuse is correct:** The license filter has the same semantics as every other comma-separated filter in the codebase: split on commas, match any value. `apply_filter` was designed for exactly this pattern, and using it ensures consistent behavior (same trimming rules, same empty-value handling, same SQL generation) across all filter parameters in the API.

---

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint implements a `severity` query parameter that follows a specific structural pattern:

1. A query/params struct with an `Option<String>` field for the filter value.
2. An Axum extractor that deserializes the query string into this struct.
3. A handler function that extracts the optional field and passes it to the service layer.
4. The service layer calls `apply_filter` to generate the SQL condition.

This is the canonical pattern for optional list-endpoint filters in the trustify-backend codebase.

**How it is reused:** The license filter implementation follows this pattern step by step as a structural guide:

- **Query struct:** Add `license: Option<String>` to the package endpoint's query struct, mirroring how `severity: Option<String>` appears in the advisory query struct.
- **Handler function:** Extract `params.license` and pass it to `PackageService::list()`, following the same control flow as the advisory handler extracts `params.severity` and passes it to `AdvisoryService::list()`.
- **Service method:** Accept the optional license string as a parameter and, when present, apply it using `apply_filter` -- the same call pattern used in the advisory service's severity handling.

**What is NOT done:** No new architectural pattern is invented. The advisory severity filter is treated as a proven template, and the license filter is a structural copy with domain-specific names substituted (severity -> license, advisory -> package, advisory table -> package_license join table). The handler, query struct, and service method signatures all follow the advisory precedent.

**Why this reuse is correct:** Using the same structural pattern ensures that the license filter behaves consistently with the severity filter from the API consumer's perspective (same query string syntax, same comma-separated semantics, same response shape). It also makes the codebase easier to navigate -- a developer familiar with the advisory severity filter will immediately recognize the license filter's structure.

---

## 3. `entity/src/package_license.rs`

**What it provides:** This file defines the SeaORM entity for the `package_license` database table, which is the join table mapping packages to their declared licenses. It includes the entity's column definitions (including the license identifier column and the package foreign key), the `Model` struct, and the `Relation` definitions that connect it to both the `package` table and the `license` table.

**How it is reused:** When the license filter is active, the `PackageService` list query adds a JOIN to the `package_license` table using SeaORM's `JoinType::InnerJoin` (or `LeftJoin` depending on the filter semantics) with the relation defined in `package_license.rs`. The JOIN condition uses the entity's defined relations -- specifically the foreign key from `package_license` to `package` -- rather than hand-writing a raw SQL `JOIN ... ON` clause.

After the JOIN, the filter condition from `apply_filter` is applied to `package_license::Column::LicenseId` (or the equivalent license identifier column defined in the entity). This targets the correct column through the entity's typed column enum, catching any column name mismatches at compile time.

**What is NOT done:**
- No raw SQL JOIN is written (`SELECT ... JOIN package_license ON ...`). The SeaORM entity's relations handle the join condition.
- No new entity file is created. The existing `package_license.rs` entity already maps the join table accurately.
- No manual foreign key mapping is written. The entity's `Relation` definitions already encode the package-to-license relationship.

**Why this reuse is correct:** The `package_license` entity is the canonical representation of the package-license mapping in the codebase. Using it ensures that the JOIN uses the correct table name, column names, and foreign key relationships as defined in the schema. Any future schema migration that changes the join table will update the entity in one place, and the license filter will automatically reflect the change.

---

## Summary

All three reuse candidates are used directly without modification or duplication:

| Candidate | Role in Implementation | Alternative Avoided |
|---|---|---|
| `apply_filter` | Parses comma-separated values, generates SQL IN clause | Writing a new `parse_license_filter()` or manual `.split(',')` logic |
| Advisory severity filter pattern | Structural template for query struct, handler, and service method | Inventing a new endpoint filter architecture |
| `package_license` entity | SeaORM JOIN via typed relations and column enums | Writing raw SQL JOINs or creating a new entity |

The implementation introduces no new utility functions, no new entity definitions, and no new filtering patterns. It connects existing infrastructure (query parameter -> `apply_filter` -> `package_license` JOIN -> filtered results) using the same wiring pattern proven by the advisory severity filter.
