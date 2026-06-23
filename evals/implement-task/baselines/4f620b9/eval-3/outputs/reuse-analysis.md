# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description provides three explicit Reuse Candidates. Each is analyzed below with a description of how it would be used during implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**Description from task**: Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it would be reused**: This is the core utility for the filter implementation. It would be called directly in `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) when the `license` parameter is present.

**Specific usage**:
- Import `apply_filter` from `common::db::query`
- Call `apply_filter(query_builder, license_value, package_license_column)` where:
  - `query_builder` is the existing SeaORM select query for packages
  - `license_value` is the raw comma-separated string from the query parameter (e.g., `"MIT,Apache-2.0"`)
  - `package_license_column` is the SPDX identifier column on the `package_license` entity
- `apply_filter` internally handles:
  - Splitting the comma-separated string into individual values
  - Generating a SQL `WHERE column IN (val1, val2, ...)` clause
  - Attaching the condition to the query builder
- No modifications to `apply_filter` itself are needed -- it is reused as-is

**Reuse type**: Direct invocation (no modification needed)

**Benefit**: Eliminates the need to write custom comma-separated parsing logic, SQL IN clause construction, or input sanitization. The existing utility already handles edge cases and follows the project's established query-building patterns.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Description from task**: The severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field.

**How it would be reused**: This file serves as the structural template for the changes to `modules/fundamental/src/package/endpoints/list.rs`. The advisory endpoint's approach to filtering is copied and adapted.

**Specific patterns to replicate**:

1. **Query struct definition**: The advisory list endpoint defines a `Query` struct with an `Option<String>` field for `severity`. The package endpoint's Query struct would add an analogous `Option<String>` field for `license`:
   ```rust
   // In advisory/endpoints/list.rs (existing pattern):
   #[derive(Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting) ...
       pub severity: Option<String>,
   }

   // In package/endpoints/list.rs (new, following the pattern):
   #[derive(Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting) ...
       pub license: Option<String>,
   }
   ```

2. **Handler function flow**: The advisory handler extracts `query.severity`, passes it to the service layer, and returns the filtered result. The package handler would follow the identical flow with `query.license`.

3. **Input validation**: If the advisory handler validates the severity parameter before passing it downstream, the same validation approach would be applied to the license parameter.

**Reuse type**: Structural pattern replication (not a code dependency, but a template for implementation)

**Benefit**: Ensures the license filter implementation is consistent with the project's established endpoint patterns. Reduces cognitive overhead during code review since the pattern is already familiar to the team. Avoids inventing a new approach when a proven one exists.

---

### 3. `entity/src/package_license.rs` (Package-License entity)

**Description from task**: Existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL.

**How it would be reused**: This SeaORM entity definition would be imported and used in `PackageService::list` to construct the JOIN between the `package` table and the `package_license` table.

**Specific usage**:
- Import the `package_license` entity module (e.g., `use entity::package_license`)
- Use the entity's `Column` enum to reference the license identifier column in the filter condition
- Use the entity's `Relation` definitions (or explicit join conditions) to construct the SeaORM `.join()` call:
  ```rust
  // Conceptual usage:
  query = query
      .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
      .filter(package_license::Column::LicenseId.is_in(license_values));
  ```
- The existing entity already defines the table name, column names, column types, and relationships -- no need to duplicate any of this

**Reuse type**: Direct import and usage of existing entity (no modification needed)

**Benefit**: Avoids writing raw SQL for the JOIN, ensures type-safe column references, and leverages SeaORM's query builder for correct and maintainable SQL generation. Any future schema changes to the package_license table will be reflected in the entity and caught by the compiler.

---

## Additional Reuse Discovered During Analysis

Beyond the three explicit Reuse Candidates, the following existing code would also be reused:

### 4. `common/src/model/paginated.rs::PaginatedResults<T>`

**What it is**: The generic response wrapper for list endpoints.

**How it would be reused**: The package list endpoint already returns `PaginatedResults<PackageSummary>`. This remains unchanged -- the filter only affects which items populate the result, not the response structure. Reusing the existing wrapper ensures the response shape contract is maintained.

### 5. `common/src/error.rs::AppError`

**What it is**: The shared error enum implementing `IntoResponse` for Axum.

**How it would be reused**: The handler continues to return `Result<T, AppError>`. For invalid license values (empty string), a 400 Bad Request would be returned using the existing `AppError` variant for validation errors, following the same error construction pattern used in sibling endpoints.

### 6. Test infrastructure from `tests/api/advisory.rs` and `tests/api/sbom.rs`

**What it is**: Test setup patterns including database seeding, HTTP client construction, and response assertion helpers.

**How it would be reused**: The new test file `tests/api/package_license_filter.rs` would follow the same test infrastructure patterns -- using the same test database setup, HTTP client construction, and assertion style. Any shared test utilities (e.g., helper functions for seeding test data or making HTTP requests) would be imported rather than reimplemented.

---

## Summary

| Reuse Candidate | Source File | Reuse Type | Modified? |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | No |
| Severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template | N/A (pattern, not dependency) |
| Package-License entity | `entity/src/package_license.rs` | Direct import | No |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Already in use | No |
| `AppError` | `common/src/error.rs` | Already in use | No |
| Test infrastructure | `tests/api/advisory.rs`, `tests/api/sbom.rs` | Structural template | N/A |

All three explicitly listed Reuse Candidates from the task description are incorporated into the implementation plan. No new utility code needs to be written for the core filter logic -- the existing `apply_filter` function and `package_license` entity provide everything needed. The advisory endpoint serves as a proven structural template that ensures consistency with the codebase's established patterns.
