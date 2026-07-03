# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description includes three reuse candidates. All three are directly applicable and would be reused in the implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**Description from task:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it would be reused:**

- **Reuse type:** Direct invocation (no modification needed)
- **Usage location:** `modules/fundamental/src/package/service/mod.rs`, inside the `list` method of `PackageService`
- **Purpose:** Parse the `license` query parameter string (which may contain comma-separated values like `"MIT,Apache-2.0"`) and generate the appropriate SQL WHERE clause:
  - Single value (`"MIT"`) produces `WHERE package_license.license = 'MIT'`
  - Multi-value (`"MIT,Apache-2.0"`) produces `WHERE package_license.license IN ('MIT', 'Apache-2.0')`
- **Rationale:** This function already encapsulates the exact parsing and SQL generation logic needed. Writing new comma-splitting and IN-clause logic would be pure duplication. The advisory endpoint's severity filter already uses this same function, confirming it is the established pattern.
- **Verification step:** Before using, inspect the function signature with `mcp__serena_backend__find_symbol` on `apply_filter` to confirm:
  - It accepts the column/field to filter on
  - It accepts the raw query parameter string
  - It returns a SeaORM condition or query modifier
  - It handles edge cases (empty strings, whitespace around commas)

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Description from task:** The severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field.

**How it would be reused:**

- **Reuse type:** Structural pattern reference (follow the same code pattern, not direct function call)
- **Usage location:** `modules/fundamental/src/package/endpoints/list.rs`
- **What to replicate from the advisory list endpoint:**
  1. **Query struct pattern:** The advisory list endpoint defines a query parameter struct (e.g., `PackageListQuery` or similar Axum extractor struct) with optional fields for each filter. The `severity` field is `Option<String>`. Add `license: Option<String>` to the package endpoint's equivalent struct following the same declaration pattern.
  2. **Handler extraction pattern:** The advisory handler extracts the optional severity from the query struct and passes it to the service layer. The package handler should extract `license` the same way.
  3. **Validation pattern:** If the advisory endpoint validates the severity value before passing it to the service (e.g., checking against known values), follow the same validation approach for license SPDX identifiers.
  4. **Error response pattern:** If the advisory endpoint returns 400 Bad Request for invalid severity values, follow the same error construction pattern (likely using `AppError` from `common/src/error.rs`).
- **Rationale:** Following an existing sibling endpoint's pattern ensures consistency across the API and reduces the risk of introducing a new, incompatible approach. Code reviewers familiar with the advisory filter will immediately recognize the license filter pattern.

---

### 3. `entity/src/package_license.rs` (package-license join table entity)

**Description from task:** Existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL.

**How it would be reused:**

- **Reuse type:** Direct use of existing SeaORM entity for query construction
- **Usage location:** `modules/fundamental/src/package/service/mod.rs`, inside the `list` method
- **Purpose:** When the `license` filter is provided, the query needs to JOIN the `package` table with the `package_license` table to find packages associated with the specified license(s). The `package_license` entity provides:
  1. **Table name and column definitions:** SeaORM entity columns (e.g., `Column::PackageId`, `Column::License`) used in the JOIN condition and WHERE clause without hardcoding table/column names.
  2. **Relation definitions:** SeaORM relations between `package` and `package_license` entities, enabling idiomatic JOIN construction (e.g., `package::Entity::find().join(JoinType::Inner, package_license::Relation::Package.def())`).
  3. **Type safety:** Column references are type-checked at compile time, catching typos or schema mismatches.
- **Rationale:** Using the existing entity is both safer and more maintainable than raw SQL. If the schema changes (e.g., column rename), the entity update will cause a compile error at the JOIN site, rather than a runtime SQL failure. This follows the project convention where all database access goes through SeaORM entities (as established by `sbom_advisory.rs`, `sbom_package.rs`, and other join table entities in `entity/src/`).
- **Verification step:** Inspect the entity with `mcp__serena_backend__get_symbols_overview` on `entity/src/package_license.rs` to confirm:
  - It has a column for the license identifier (likely `license` or `spdx_id`)
  - It has a column for the package foreign key (likely `package_id`)
  - It defines a SeaORM relation to the `package` entity

---

## Additional Reuse Opportunities Discovered During Analysis

### 4. `common/src/model/paginated.rs::PaginatedResults<T>`

- **Not in Reuse Candidates, but critical:** The response wrapper is already used by the existing `list` handler. No changes needed to this type -- the license filter only affects query input, not output shape. This confirms acceptance criterion #4 (response shape unchanged).

### 5. `common/src/error.rs::AppError`

- **Not in Reuse Candidates, but used for validation:** The 400 Bad Request response for invalid license values should use the existing `AppError` enum, following the same pattern used throughout the codebase. No new error types are needed.

---

## Reuse Summary

| Candidate | Reuse Type | Where Used | New Code Avoided |
|---|---|---|---|
| `apply_filter` | Direct call | `PackageService::list()` | Comma-separated parsing + SQL IN clause generation |
| Advisory list pattern | Structural pattern | `package/endpoints/list.rs` | Query struct design + handler extraction + validation |
| `package_license` entity | Direct use | `PackageService::list()` | JOIN table definition + column references + raw SQL |
| `PaginatedResults<T>` | Unchanged | Response type | No new response wrapper needed |
| `AppError` | Direct use | Validation error path | No new error type needed |

**Reuse impact:** By leveraging these three primary reuse candidates, the implementation avoids writing:
- Custom comma-separated value parsing logic
- Raw SQL for the JOIN and IN clause
- A new query parameter extraction pattern
- New entity definitions for the join table

The net new code is limited to:
1. Adding the `license` field to the package query struct (following advisory pattern)
2. Threading the license value from handler to service
3. Constructing the JOIN + filter query using existing building blocks
4. Validation logic for invalid license values
5. Integration tests
