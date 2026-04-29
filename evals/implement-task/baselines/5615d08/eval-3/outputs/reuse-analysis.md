# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is leveraged in the implementation, and identifies additional existing code that is reused.

---

## Reuse Candidates from Task Description

### 1. `common/src/db/query.rs::apply_filter`

**What it provides**: A shared utility function that accepts a raw query parameter string (potentially comma-separated), splits it into individual values, and generates a SQL `IN (...)` clause compatible with SeaORM's query builder.

**How it is reused**: The `PackageService::list()` method calls `apply_filter` directly with the raw `license` query parameter string. This function handles:

- Splitting `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`
- Generating the equivalent of `WHERE package_license.spdx_id IN ('MIT', 'Apache-2.0')`
- Handling the single-value case (`"MIT"` becomes `WHERE package_license.spdx_id = 'MIT'`)

**Why reuse instead of writing new code**: Writing custom comma-splitting and SQL IN clause generation would duplicate logic that already exists, is tested, and handles edge cases (whitespace trimming, empty segments, SQL injection prevention via parameterized queries). The `apply_filter` function is specifically designed for this pattern and is already used by the advisory severity filter.

**Reuse type**: Direct function call -- no modification to `apply_filter` is needed.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides**: A working example of how to add an optional filter query parameter to a list endpoint. The advisory list endpoint defines a `Query` struct (derived with `Deserialize` and Axum's query extraction) containing an `Option<String>` field for `severity`. The handler extracts this struct and passes the filter value to `AdvisoryService::list()`.

**How it is reused**: The package endpoint's `list.rs` follows the identical structural pattern:

1. The query parameter extraction struct (e.g., `PackageListQuery`) gets a new `license: Option<String>` field, mirroring how the advisory struct declares `severity: Option<String>`.
2. The handler function destructures or accesses `query.license` and passes it to `PackageService::list()`, exactly as the advisory handler passes `query.severity` to `AdvisoryService::list()`.
3. The same Axum `Query<T>` extractor is used for deserialization.

**Why reuse instead of writing new code**: The advisory severity filter is described in the task as "structurally identical" to the license filter. Deviating from this established pattern would introduce inconsistency in the codebase and risk missing conventions (error handling, parameter naming, deserialization attributes). Following the existing pattern ensures the new filter integrates consistently with the rest of the API surface.

**Reuse type**: Structural pattern replication -- the advisory code serves as a template; the package code mirrors its structure with domain-specific names substituted.

---

### 3. `entity/src/package_license.rs`

**What it provides**: A SeaORM entity definition for the `package_license` database table, which maps packages to their declared SPDX license identifiers. This entity defines the `Relation` to both the `package` table and the license data, enabling type-safe JOIN queries through SeaORM's relation system.

**How it is reused**: In `PackageService::list()`, when a license filter is active, the query builder uses `package_license::Entity` to construct a JOIN:

```
// Pseudocode illustrating the approach:
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(package_license::Column::SpdxId.is_in(license_values))
```

The entity's column definitions and relation declarations are used directly -- no raw SQL table or column names are hardcoded.

**Why reuse instead of writing new code**: The `package_license` entity already encodes the schema knowledge (column names, types, relations). Writing raw SQL JOINs would bypass SeaORM's type safety, risk column name mismatches, and diverge from the project's convention of using SeaORM entities for all database access.

**Reuse type**: Direct entity usage -- the existing entity is imported and its columns/relations are used in query construction. No modification to the entity file is needed.

---

## Additional Existing Code Reused

### 4. `common/src/model/paginated.rs` -- `PaginatedResults<T>`

**What it provides**: A generic response wrapper that adds pagination metadata (total count, page, page size) around a `Vec<T>` of results.

**How it is reused**: The `GET /api/v2/package` endpoint already returns `PaginatedResults<PackageSummary>`. The license filter is applied at the query level before pagination, so the same return type is used without modification. Tests deserialize responses as `PaginatedResults<PackageSummary>` to verify filtering correctness.

---

### 5. `common/src/error.rs` -- `AppError`

**What it provides**: A centralized error enum that implements Axum's `IntoResponse` trait, mapping application errors to HTTP status codes.

**How it is reused**: Validation of the license parameter (e.g., rejecting empty values) uses `AppError` to produce `400 Bad Request` responses, following the same `.context()` wrapping pattern used throughout the codebase.

---

### 6. `tests/api/advisory.rs` -- Test structure pattern

**What it provides**: An example of integration test structure: database seeding, HTTP request construction, response assertion, and body deserialization.

**How it is reused**: The new `tests/api/package_license_filter.rs` follows the same test scaffolding pattern -- setting up a test database with known data, making HTTP requests via the test client, and asserting on status codes and deserialized response bodies.

---

## Summary

| Candidate | Source | Reuse Type | Modifications Needed |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | None |
| Severity filter pattern | `advisory/endpoints/list.rs` | Structural pattern replication | None (source unchanged) |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage in JOINs | None |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Existing return type | None |
| `AppError` | `common/src/error.rs` | Error handling | None |
| Advisory test structure | `tests/api/advisory.rs` | Test pattern replication | None (source unchanged) |

No new utility functions, abstractions, or shared modules are needed. The entire implementation is composed by reusing existing infrastructure and following established patterns.
