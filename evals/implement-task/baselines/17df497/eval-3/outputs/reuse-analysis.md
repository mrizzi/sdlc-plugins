# Reuse Analysis for TC-9203: Add package license filter to list endpoint

This document details how each Reuse Candidate listed in the task description would
be used during implementation, along with any additional reuse opportunities discovered
during code inspection.

---

## Reuse Candidates from Task Description

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:**
Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.
Given a raw query string like `"MIT,Apache-2.0"` and a SeaORM column reference, it:
- Splits the string on commas
- Trims whitespace from each value
- Generates a `Column::is_in(vec![...])` SeaORM condition

**How it would be reused:**
Directly invoked in `PackageService::list()` to convert the raw `license` query parameter
into a SeaORM filter condition. No modification to `apply_filter` itself is needed -- it is
used as-is.

```rust
// In PackageService::list()
if let Some(license_value) = license {
    query = apply_filter(query, package_license::Column::License, license_value);
}
```

**Reuse type:** Direct call (no modification required)

**Why reuse matters here:**
Without `apply_filter`, the implementation would need to manually split the comma-separated
string, trim values, validate them, and construct the `is_in()` condition -- duplicating
logic that already exists and is tested. Reusing `apply_filter` ensures consistent behavior
with other filter parameters (e.g., the advisory severity filter) and reduces the risk of
subtle parsing bugs (e.g., forgetting to trim whitespace).

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
A complete, working implementation of an optional query parameter filter on a list endpoint.
The advisory list endpoint supports a `severity` query parameter using a pattern that is
structurally identical to the license filter needed here:

- An `AdvisoryQuery` struct with `severity: Option<String>` field (serde-deserialized)
- The handler extracts the optional field and passes it to `AdvisoryService::list()`
- The service method applies the filter conditionally (only when `Some`)

**How it would be reused:**
Used as a structural template -- not called directly, but its pattern is replicated in the
package module. Specifically:

1. **Query struct pattern**: Add `license: Option<String>` to `PackageQuery` in
   `modules/fundamental/src/package/endpoints/list.rs`, mirroring how `severity: Option<String>`
   is defined in `AdvisoryQuery`.

2. **Handler wiring pattern**: Pass `query.license` to the service method in the same way
   the advisory handler passes `query.severity` to `AdvisoryService::list()`.

3. **Service integration pattern**: In `PackageService::list()`, conditionally apply the
   filter using the same guard pattern (`if let Some(value) = filter_param`).

**Reuse type:** Structural template (pattern replication, not direct invocation)

**Why reuse matters here:**
Following the advisory pattern ensures consistency across the codebase. All list endpoints
will handle optional filters the same way, making the codebase predictable for developers.
Inventing a different approach (e.g., a custom middleware, a different parameter extraction
strategy) would create unnecessary divergence and increase cognitive load for reviewers.

---

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:**
An existing SeaORM entity representing the `package_license` database table, which maps
packages to their declared licenses. The entity includes:

- Column definitions (at minimum `package_id` and `license`/`license_id`)
- Relation definitions linking back to the `package` entity
- SeaORM model/entity trait implementations

**How it would be reused:**
Used in `PackageService::list()` to perform the JOIN between the `package` table and the
`package_license` table when the license filter is active.

```rust
use entity::package_license;

// Join to package_license table for filtering
query = query.join(
    sea_orm::JoinType::InnerJoin,
    package::Relation::PackageLicense.def(),
);
// Then apply the filter on package_license::Column::License
query = apply_filter(query, package_license::Column::License, license_value);
```

**Reuse type:** Direct reference (entity and its columns/relations used in query building)

**Why reuse matters here:**
The entity already defines the correct table structure, column names, and relationships.
Writing raw SQL or hand-coding a JOIN expression would bypass SeaORM's type safety and
risk column name mismatches. Using the entity also ensures the query benefits from any
future schema migrations that update the entity definition.

---

## Additional Reuse Opportunities Discovered

### 4. `common/src/model/paginated.rs::PaginatedResults<T>`

**What it provides:**
The generic response wrapper used by all list endpoints, providing `items`, `total_count`,
and pagination metadata.

**How it would be reused:**
No change needed -- `PackageService::list()` already returns `PaginatedResults<PackageSummary>`.
The license filter modifies the query that feeds into this wrapper but does not change the
wrapper itself. The response shape remains identical.

**Reuse type:** Unchanged dependency (already in use, confirmed unchanged)

### 5. `common/src/error.rs::AppError`

**What it provides:**
The shared error enum implementing Axum's `IntoResponse`. Includes variants for common HTTP
error codes (400, 404, 500).

**How it would be reused:**
Used to return `400 Bad Request` when the `license` parameter contains invalid values
(e.g., empty strings after splitting on commas).

```rust
return Err(AppError::bad_request("Invalid license value: empty string"));
```

**Reuse type:** Direct use (error construction, already available in scope)

---

## Reuse Summary

| Candidate | Source File | Reuse Type | Modification Needed |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct call | None |
| Advisory severity pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template | None (pattern replicated) |
| `package_license` entity | `entity/src/package_license.rs` | Direct reference | None |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Unchanged dependency | None |
| `AppError` | `common/src/error.rs` | Direct use | None |

**Key finding:** All three task-specified reuse candidates are directly applicable without
modification. The `apply_filter` function is the most impactful reuse -- it eliminates the
need to write any custom query parameter parsing or SQL condition generation logic. The
advisory endpoint serves as a complete structural blueprint, ensuring the implementation
follows established conventions rather than inventing new patterns.
