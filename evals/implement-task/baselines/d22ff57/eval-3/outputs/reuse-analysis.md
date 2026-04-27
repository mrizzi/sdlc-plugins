# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document details each Reuse Candidate listed in the task description, how it would be used in the implementation, and any additional reuse opportunities discovered.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:**
- Parses comma-separated multi-value query parameter strings (e.g., `"MIT,Apache-2.0"`) into individual values
- Generates a SQL `IN` clause for filtering (e.g., `WHERE license IN ('MIT', 'Apache-2.0')`)
- Handles single-value input as a degenerate case of multi-value (one-element IN clause)
- Integrates with SeaORM query builders

**How it would be reused:**

Direct reuse — called as-is from `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs`. When the `license` parameter is `Some`, the service passes the raw query string to `apply_filter`, which handles all parsing and SQL generation:

```rust
if let Some(license_value) = license {
    query = apply_filter(query, "package_license", "license", &license_value)?;
}
```

**Why reuse instead of reimplementing:**
- The comma-separated parsing logic (splitting, trimming, empty-segment rejection) is already tested and handles edge cases
- Writing a custom parser would duplicate this logic and risk inconsistency with how other filters (e.g., severity) handle the same input format
- The SQL IN clause generation integrates with SeaORM's query builder in a way that is already proven in the advisory module

**Modifications needed:** None. `apply_filter` is generic enough to accept any entity/column combination. No changes to the shared function are required.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:**
- A structural pattern for adding an optional filter query parameter to a list endpoint
- Shows how to declare an optional field on the Axum query parameter extraction struct
- Shows how to pass the optional filter value from the endpoint handler to the service layer
- Shows the validation pattern for filter values before forwarding

**How it would be reused:**

Structural reference — the advisory list endpoint's `severity` filter implementation serves as the template for the package list endpoint's `license` filter. The same pattern is applied to a different entity and field:

1. **Query struct pattern:** The advisory endpoint has a query struct (e.g., `AdvisoryListQuery`) with an `Option<String>` field for `severity`. The package endpoint's query struct would add the same kind of field for `license`:
   ```rust
   #[derive(Deserialize)]
   pub struct PackageListQuery {
       // ... existing pagination/sorting fields
       /// Optional license filter; supports comma-separated SPDX identifiers.
       pub license: Option<String>,
   }
   ```

2. **Handler forwarding pattern:** The advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package handler would do the same with `query.license` to `PackageService::list()`.

3. **Validation pattern:** If the advisory handler validates the severity value before forwarding (e.g., checking for empty strings or invalid characters), the same validation logic would be replicated for the license parameter.

**Why reuse this pattern:**
- Ensures consistency across list endpoints — consumers of the API see the same filtering behavior regardless of which entity they query
- The advisory severity filter is already tested and reviewed; following the same pattern reduces risk of structural errors
- Convention conformance: sibling endpoints should follow identical patterns for identical features

**Modifications needed:** This is a pattern reference, not a code import. The package endpoint would implement the same structural approach with `license` substituted for `severity` and `PackageService` substituted for `AdvisoryService`.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:**
- The SeaORM entity definition for the `package_license` join table
- Column definitions mapping packages to their declared licenses
- Relation definitions connecting the `package_license` entity to the `package` entity (and potentially the `license` entity)
- The entity's `Column` enum with variants for the license identifier field

**How it would be reused:**

Direct reuse — the entity is used in `PackageService::list()` to build the JOIN clause when the license filter is active:

```rust
use entity::package_license;

// In the list method, when license filter is active:
if license.is_some() {
    query = query.join(
        JoinType::InnerJoin,
        package_license::Relation::Package.def().rev(),
    );
}
```

The entity's `Column` enum is used by `apply_filter` to reference the correct database column for the WHERE clause.

**Why reuse instead of raw SQL:**
- The SeaORM entity already defines the table structure, column names, and relations — using it ensures type-safe query construction
- Writing raw SQL JOINs would bypass SeaORM's query builder, creating inconsistency with how other parts of the codebase build queries
- The relation definitions in the entity handle the foreign key mapping, so the JOIN is correct by construction
- If the database schema changes (e.g., column rename), the SeaORM entity would be updated in one place and all consumers (including this filter) would get the fix automatically

**Modifications needed:** None. The existing entity and its relations are sufficient for the JOIN query. No new columns, relations, or methods need to be added.

---

## Additional Reuse Opportunities Discovered

### `common/src/model/paginated.rs` — `PaginatedResults<T>`

**What it provides:** The generic paginated response wrapper used by all list endpoints.

**How it is reused:** The package list endpoint already returns `PaginatedResults<PackageSummary>`. Adding the license filter does not change the response type — `PaginatedResults<T>` wraps the filtered result set transparently. No changes needed; this is existing reuse that continues to work.

### `common/src/error.rs` — `AppError`

**What it provides:** The shared error enum implementing `IntoResponse` for Axum.

**How it is reused:** The license filter validation logic (returning 400 for invalid input) would use `AppError` variants to produce the error response. This follows the same error handling pattern used by all other endpoints and avoids creating custom error types.

### Advisory service filter pattern (`modules/fundamental/src/advisory/service/advisory.rs`)

**What it provides:** The service-layer pattern for applying an optional filter parameter to a SeaORM query.

**How it is reused:** Structural reference for how `PackageService::list()` should receive the optional `license` parameter, conditionally build the JOIN and WHERE clauses, and return the filtered results. This complements the endpoint-layer pattern from Reuse Candidate 2.

---

## Reuse Summary

| Candidate | Reuse Type | Location Used | Modifications |
|---|---|---|---|
| `apply_filter` | Direct code reuse | `PackageService::list()` in `service/mod.rs` | None |
| Advisory severity filter pattern | Structural pattern | `PackageListQuery` struct and handler in `endpoints/list.rs` | Adapted for `license` field |
| `package_license` entity | Direct code reuse | JOIN clause in `PackageService::list()` | None |
| `PaginatedResults<T>` | Existing (unchanged) | Return type of list endpoint | None |
| `AppError` | Existing (unchanged) | Validation error responses | None |
| Advisory service filter pattern | Structural pattern | `PackageService::list()` filter application | Adapted for license/package_license |

All three explicitly listed Reuse Candidates would be used. No new utility functions or shared modules need to be created — the existing infrastructure fully supports the license filter feature.
