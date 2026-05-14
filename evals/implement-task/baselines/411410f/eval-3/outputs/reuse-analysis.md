# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description provides three Reuse Candidates. All three are directly applicable and would be used in the implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. This is a shared utility already used across the codebase for building filter queries.

**How it would be reused:** Called directly in `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) to parse the `license` query parameter value. When the user passes `?license=MIT,Apache-2.0`, `apply_filter` splits the comma-separated string into individual values and generates the appropriate SQL `IN` clause for the query builder.

**Reuse type:** Direct invocation — no modification needed to the utility itself. The function is generic enough to handle the license filter without any changes.

**Benefit:** Eliminates the need to write custom comma-parsing and SQL generation logic. Ensures consistent behavior with all other filters in the application that use the same utility. If the parsing behavior changes in the future (e.g., trimming whitespace, case normalization), the license filter benefits automatically.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** A structurally identical filter implementation for the advisory list endpoint. The severity filter uses an optional field on a Query struct, passes it to the service layer, and uses `apply_filter` to build the SQL filter — the exact same pattern needed for the license filter.

**How it would be reused:** Used as a structural template (not called directly). The implementation would follow the same pattern:

1. **Query struct pattern:** Add `license: Option<String>` to the package endpoint's query parameter struct, mirroring how `severity: Option<String>` is defined in the advisory endpoint's query struct.

2. **Service call pattern:** Pass the `license` value from the endpoint handler to `PackageService::list()` in the same way the advisory handler passes `severity` to `AdvisoryService::list()`.

3. **Filter application pattern:** In the service method, apply the filter using the same `apply_filter` call pattern used in the advisory service for severity filtering.

**Reuse type:** Structural pattern reuse — the advisory filter serves as a reference implementation that is replicated with substitutions (severity -> license, advisory entity -> package_license entity).

**Benefit:** Ensures the license filter follows established conventions in the codebase. Reduces implementation risk because the pattern is already proven to work for the severity filter. Makes code review easier because reviewers can compare the new filter against the existing severity filter.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The existing SeaORM entity that maps the relationship between packages and their licenses (a join table). This entity defines the database schema, column mappings, and relations needed to query which licenses belong to which packages.

**How it would be reused:** Used in the `PackageService::list` method to build a JOIN query that filters packages by their associated license identifiers. Instead of writing raw SQL to join through the package-license table, the implementation would use this SeaORM entity's relations to construct the join:

```
Package --[JOIN]--> PackageLicense --[WHERE license_id IN ('MIT', 'Apache-2.0')]
```

The entity provides:
- The table name and column definitions for the join table
- SeaORM `Relation` definitions that enable type-safe JOINs
- Column enum variants for building filter conditions on the license identifier column

**Reuse type:** Direct usage of existing entity — no modification needed. The entity is used as a building block in the query builder.

**Benefit:** Avoids raw SQL for the join query, which would bypass SeaORM's type safety and migration tracking. Uses the same entity that other parts of the codebase use to access package-license data, ensuring consistency. If the table schema changes via a migration, the entity update propagates to the license filter automatically.

---

## Additional Reuse Opportunities Identified

Beyond the three candidates listed in the task description, the following existing code would also be reused:

### `common/src/model/paginated.rs` — `PaginatedResults<T>`

The response wrapper type is already used by the package list endpoint. No changes needed — the license filter only affects query construction, not the response shape. This confirms the acceptance criterion that the response shape remains unchanged.

### `common/src/error.rs` — `AppError`

The existing error type would be used for the 400 Bad Request response when invalid license values are provided. Following the `.context()` wrapping pattern used throughout the codebase for error handling.

### Sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`)

Used as structural templates for writing the integration tests. The assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`), response deserialization approach, and test naming conventions (`test_<endpoint>_<scenario>`) would all be replicated from these siblings.

---

## Summary

| Reuse Candidate | Reuse Type | Modified? | Location Used |
|---|---|---|---|
| `apply_filter` | Direct invocation | No | `package/service/mod.rs` |
| Advisory severity filter pattern | Structural template | No (source); Yes (target) | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | Direct usage in JOIN | No | `package/service/mod.rs` |
| `PaginatedResults<T>` | Unchanged return type | No | `package/service/mod.rs` |
| `AppError` | Error response | No | `package/endpoints/list.rs` |
| Sibling test files | Test pattern template | No (source); Yes (target) | `tests/api/package_license_filter.rs` |

All three task-specified Reuse Candidates are used. No new utility code needs to be written — the implementation composes existing building blocks following established patterns.
