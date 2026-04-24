# Reuse Analysis for TC-9203: Add package license filter to list endpoint

This document details how each Reuse Candidate listed in the task description is used in the implementation, demonstrating that existing code is reused rather than duplicated.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Task description says:** "handles comma-separated multi-value query parameter parsing and SQL IN clause generation; reuse directly for the license filter"

**How it is reused:**

The `apply_filter` function is called directly in `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) to handle the license filter. No new parsing or SQL generation logic is written.

Specifically:
- `apply_filter` receives the raw license query string (e.g., `"MIT,Apache-2.0"`)
- It splits the comma-separated values into individual tokens
- It generates a SQL `WHERE ... IN (...)` clause for the license column
- It returns the modified query builder with the filter applied

**What is NOT duplicated:**
- No custom comma-splitting logic is written in the package module
- No manual SQL `IN` clause construction is written
- No new query parameter parsing utilities are created
- The existing function's error handling for malformed values is inherited

**Call site:**
```rust
// In modules/fundamental/src/package/service/mod.rs
use common::db::query::apply_filter;

if let Some(ref license_param) = license {
    query = apply_filter(query, "package_license", "license", license_param)?;
}
```

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Task description says:** "the severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field"

**How it is reused:**

The advisory list endpoint's pattern is used as the structural template for the package list endpoint changes. The advisory endpoint already demonstrates how to:

1. **Add an optional filter field to the Query struct:** The advisory endpoint's Query struct has an `Option<String>` field for `severity`. The package endpoint's Query struct is extended with an identical `Option<String>` field for `license`.

2. **Pass the filter to the service layer:** The advisory endpoint extracts `query.severity` and passes it to `AdvisoryService::list`. The package endpoint follows the same pattern, passing `query.license` to `PackageService::list`.

3. **Validate input and return errors:** The advisory endpoint validates its filter parameter and returns `AppError` for invalid values. The package endpoint uses the same validation and error-handling approach.

**What is NOT duplicated:**
- No new endpoint architecture is invented; the existing advisory pattern is followed exactly
- No new query parameter extraction mechanism is created; the Axum `Query` derive macro pattern from the advisory endpoint is reused
- The error response format is inherited from the shared `AppError` type, not reimplemented

**Structural mapping:**

| Advisory endpoint (existing) | Package endpoint (new changes) |
|---|---|
| `AdvisoryListQuery.severity: Option<String>` | `PackageListQuery.license: Option<String>` |
| `handler` passes `query.severity` to service | `handler` passes `query.license` to service |
| `AdvisoryService::list(severity)` applies filter | `PackageService::list(license)` applies filter |
| Uses `apply_filter` for severity column | Uses `apply_filter` for license column |
| Returns `PaginatedResults<AdvisorySummary>` | Returns `PaginatedResults<PackageSummary>` (unchanged) |

## Reuse Candidate 3: `entity/src/package_license.rs`

**Task description says:** "existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL"

**How it is reused:**

The `package_license` entity (a SeaORM entity definition) is used in `PackageService::list` to perform the JOIN between the `package` table and the `package_license` table. This enables filtering packages by their associated license values.

Specifically:
- The entity's `Column` enum is used to reference the join columns (`PackageId`, `License`) in a type-safe manner
- The entity's `Entity` type is used in SeaORM's `.join()` method to define the join relationship
- No raw SQL is written for the join; the SeaORM join API with the existing entity provides full type safety and compile-time verification

**What is NOT duplicated:**
- No new entity or model is created for the package-license relationship
- No raw SQL JOIN statements are written
- No new migration is needed; the table and entity already exist
- The existing column definitions and relationships defined in `package_license.rs` are used as-is

**Usage site:**
```rust
// In modules/fundamental/src/package/service/mod.rs
use entity::package_license;

query = query.join(
    JoinType::InnerJoin,
    package_license::Entity,
    package_license::Column::PackageId.eq(package::Column::Id),
);
```

## Summary of Reuse

| Reuse Candidate | Location | Reuse Strategy | New Code Written? |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Called directly -- no wrapper, no copy | No new parsing/SQL logic |
| Advisory severity filter | `advisory/endpoints/list.rs` | Structural template -- same Query struct pattern, same service delegation | No new endpoint architecture |
| `package_license` entity | `entity/src/package_license.rs` | Used as-is for SeaORM JOIN | No new entity or raw SQL |

All three Reuse Candidates are used. No existing filtering, parsing, or query-building logic is duplicated. The only new code written is:

1. The `license` field added to the package Query struct (following the advisory pattern)
2. The `license` parameter added to `PackageService::list` (following the advisory pattern)
3. The conditional `apply_filter` call and JOIN in the service method (composing existing building blocks)
4. Input validation for the license parameter (following the advisory error-handling pattern)
5. Integration tests (new file, following sibling test conventions)
