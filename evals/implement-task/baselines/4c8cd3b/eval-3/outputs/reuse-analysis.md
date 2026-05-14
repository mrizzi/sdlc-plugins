# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Summary

The task description identifies three Reuse Candidates. All three are directly applicable and would be reused in the implementation. No additional reusable code needs to be written — the existing infrastructure fully supports the required functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces a SeaORM condition that matches any of the provided values.

**How it would be reused**: Called directly in `PackageService::list()` to transform the `license` query parameter string into a database filter condition. The function would be invoked as:

```rust
if let Some(license) = license_filter {
    let condition = apply_filter("license", &license);
    query = query.filter(condition);
}
```

This eliminates the need to write custom comma-parsing or SQL IN clause generation logic. The function already handles edge cases such as whitespace trimming and empty segments.

**Reuse type**: Direct invocation — no modification to `apply_filter` is needed.

**Benefit**: Avoids duplicating comma-separated parsing logic and ensures consistency with how other filters (e.g., advisory severity) handle multi-value parameters across the codebase.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter using a query struct pattern with an optional field. This is structurally identical to the license filter needed for the package endpoint. The implementation demonstrates:

1. **Query struct pattern**: An `AdvisoryQuery` struct (or similar) with `#[derive(Deserialize)]` and an `Option<String>` field for the filter parameter.
2. **Handler wiring**: How the handler extracts the filter value from the query struct and passes it to the service layer.
3. **Service integration**: How the service method accepts the optional filter and conditionally applies it to the database query using `apply_filter`.

**How it would be reused**: Used as a structural template — the advisory endpoint's pattern would be replicated for the package endpoint:

- **Endpoint layer** (`package/endpoints/list.rs`): Add a `license: Option<String>` field to the package query struct, following the same `#[serde(default)]` and deserialization pattern as the advisory's `severity` field.
- **Service layer** (`package/service/mod.rs`): Add the license filter parameter to `PackageService::list()` and conditionally apply the filter using `apply_filter`, following the same conditional-application pattern used in `AdvisoryService::list()` for severity.
- **Validation**: Follow the same validation approach (if any) that the advisory endpoint uses for invalid severity values to handle invalid license values consistently.

**Reuse type**: Structural pattern replication — the advisory code serves as the reference implementation; the same architecture and calling conventions are applied to the package module.

**Benefit**: Ensures the package license filter is consistent with the established filtering pattern in the codebase. Reduces implementation risk by following a proven, tested pattern rather than inventing a new approach.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`

**What it provides**: A SeaORM entity definition for the `package_license` join table that maps packages to their associated licenses. This entity defines:

- The table columns (likely `package_id`, `license_id` or `license_spdx`)
- The SeaORM `Relation` definitions linking to the `package` entity
- The `Model`, `ActiveModel`, `Entity`, and `Column` types used by SeaORM for type-safe queries

**How it would be reused**: Used in `PackageService::list()` to construct the JOIN query when filtering by license. Instead of writing raw SQL, the implementation would use SeaORM's type-safe join API with this entity:

```rust
use entity::package_license;

// When license filter is present, join through the package_license table
if license_filter.is_some() {
    query = query
        .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
        .filter(package_license::Column::LicenseSpdx.is_in(license_values));
}
```

The exact column name for the license identifier would be confirmed by inspecting the entity definition, but the entity already provides the complete mapping needed for the JOIN — no new entity or migration is required.

**Reuse type**: Direct usage — the existing entity is used as-is for query construction. No modifications to the entity are needed.

**Benefit**: Avoids writing raw SQL JOINs and leverages SeaORM's compile-time type checking. The entity already encodes the correct table name, column names, and foreign key relationships, reducing the risk of SQL errors.

---

## Additional Reuse Opportunities

During implementation, the following additional reusable components would also be leveraged (not listed as Reuse Candidates in the task but discovered through codebase analysis):

- **`common/src/model/paginated.rs`** (`PaginatedResults<T>`): The existing pagination wrapper is already used by the package list endpoint and would continue to be used unchanged. No new response type is needed.
- **`common/src/error.rs`** (`AppError`): The existing error enum with `IntoResponse` implementation would be used for the 400 Bad Request response on invalid license values, following the same `.context()` wrapping pattern used throughout the codebase.

---

## Reuse Impact Summary

| Component | Reuse Type | New Code Avoided |
|---|---|---|
| `apply_filter` | Direct invocation | Comma-separated parsing, SQL IN clause generation |
| Advisory list endpoint pattern | Structural template | Query struct design, handler-service wiring, conditional filter application |
| `package_license` entity | Direct usage | JOIN table mapping, raw SQL, migration |
| `PaginatedResults<T>` | Continued usage | Response wrapper |
| `AppError` | Continued usage | Error response handling |

**Conclusion**: The three identified Reuse Candidates cover the core implementation needs completely. The `apply_filter` function handles the query parameter parsing, the advisory endpoint provides the architectural template, and the `package_license` entity provides the database mapping. The implementation consists primarily of wiring these existing components together in the package module, with minimal new logic (the `license` field on the query struct and the JOIN condition in the service method).
