# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates Evaluated

### 1. `common/src/db/query.rs::apply_filter`

**Role**: Handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation.

**Reuse decision**: REUSE DIRECTLY (no modification needed)

**How it is used**:
- Called from `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs` when the `license` parameter is `Some(value)`.
- The `apply_filter` function receives the raw license string (e.g., `"MIT"` or `"MIT,Apache-2.0"`) and the target column reference (the SPDX identifier column from the `package_license` entity).
- It internally splits on commas, trims whitespace, and generates either an equality condition (single value) or an `IN (...)` clause (multiple values).
- Error handling for invalid/empty values is also handled by `apply_filter`, which returns an error that gets propagated as a 400 response.

**Why reuse rather than rewrite**:
- Constraint 5.4 explicitly prohibits duplicating existing utility functions.
- The function already handles the exact parsing and SQL generation logic needed. Writing a custom parser for comma-separated license values would be redundant.
- Proven and tested in the advisory severity filter path.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Role**: Demonstrates the structural pattern for adding an optional filter query parameter to a list endpoint.

**Reuse decision**: FOLLOW PATTERN (structural template, not a direct function call)

**How it is used**:
- The `Query` struct in the advisory list endpoint includes an optional `severity: Option<String>` field with `#[serde(default)]`. The package list endpoint's `Query` struct will add `license: Option<String>` following the identical pattern.
- The advisory handler extracts `query.severity` and passes it to the advisory service's list method. The package handler will extract `query.license` and pass it to `PackageService::list()` in the same way.
- The advisory service method calls `apply_filter` when severity is present. The package service method will call `apply_filter` when license is present, using the same call pattern.

**Specific elements adopted from this pattern**:
1. **Query struct field**: `pub license: Option<String>` with `#[serde(default)]` — mirrors `pub severity: Option<String>`.
2. **Handler wiring**: Extract the optional field from the deserialized query struct and pass it as a parameter to the service method.
3. **Service integration**: Conditionally apply the filter only when the parameter is `Some`, leaving the base query unchanged when `None`.

**Why follow pattern rather than abstract**:
- The advisory and package modules are separate domain modules. Creating a shared generic "filterable endpoint" abstraction would over-engineer for two instances and would violate the scope constraint (5.1) by modifying files outside the allowed list.
- Following the pattern ensures consistency without coupling.

---

### 3. `entity/src/package_license.rs`

**Role**: Existing SeaORM/Diesel entity representing the `package_license` join table that maps packages to their declared licenses.

**Reuse decision**: REUSE DIRECTLY (no modification needed)

**How it is used**:
- Imported in `modules/fundamental/src/package/service/mod.rs` to perform the JOIN between the `package` table and the `package_license` table.
- The entity's column definitions (specifically the SPDX identifier column and the package ID foreign key column) are used in:
  1. The JOIN condition: `package.id = package_license.package_id` (using the entity's relation or column references).
  2. The filter target: `apply_filter` is called with the `package_license::Column::LicenseIdentifier` (or equivalent column name) as the target column.

**Why reuse rather than raw SQL**:
- Constraint 5.4: The entity already exists; using raw SQL to query the same table would duplicate the schema definition.
- The entity provides type-safe column references, which the ORM query builder and `apply_filter` expect.
- Consistent with how other service methods perform joins through entity relations.

---

## Additional Existing Code Referenced (not in Reuse Candidates list)

### `common/src/model/paginated.rs` — `PaginatedResults<T>`

**Reuse decision**: NO MODIFICATION — used as-is

The response type `PaginatedResults<PackageSummary>` is already the return type of the package list endpoint. The license filter is applied at the query level before pagination. No changes to pagination logic are needed.

### `common/src/error.rs` — `AppError`

**Reuse decision**: NO MODIFICATION — used as-is

Error variants (e.g., `AppError::BadRequest`) are used to propagate validation failures from `apply_filter` or the service layer back to the endpoint as HTTP 400 responses. No new error variants are needed.

### `tests/api/advisory.rs` — Test infrastructure patterns

**Reuse decision**: FOLLOW PATTERN

Test setup (database seeding, HTTP client construction, assertion helpers) from the advisory integration tests will be followed when writing `tests/api/package_license_filter.rs`. This ensures consistent test style and avoids reinventing test infrastructure.

---

## Summary

| Candidate | Reuse Type | Location Used |
|---|---|---|
| `apply_filter` | Direct function call | `package/service/mod.rs` |
| Advisory severity filter pattern | Structural template | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | Direct import | `package/service/mod.rs` |
| `PaginatedResults<T>` | Unchanged (no modification) | Already in use |
| `AppError` | Unchanged (no modification) | Already in use |
| Advisory test patterns | Structural template | `tests/api/package_license_filter.rs` |

No new utility functions or abstractions need to be created. All required logic is either directly available via `apply_filter` or follows established patterns in the advisory module.
