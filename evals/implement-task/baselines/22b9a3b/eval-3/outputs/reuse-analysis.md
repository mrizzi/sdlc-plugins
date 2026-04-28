# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details which Reuse Candidates from the task description are used, how they are applied, and why no new utility code needs to be written.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and generates a SQL `IN` clause for filtering. It takes a raw query string value (e.g., `"MIT,Apache-2.0"`), splits on commas, and produces the appropriate SeaORM condition.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, we call `apply_filter` directly with the license string. This eliminates the need to write any custom string-splitting, SQL clause generation, or value-escaping logic. The function is called exactly as it is used in the advisory service for severity filtering.

**Reuse type**: Direct invocation -- no wrapping, no modification.

**Benefit**: Avoids duplicating comma-separated parsing logic. Ensures consistent behavior with other filters in the codebase (same escaping, same SQL generation, same handling of edge cases like trailing commas).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: A structural template for adding an optional filter query parameter to a list endpoint. The advisory list endpoint defines a query struct with an optional `severity` field, extracts it in the handler, validates it, and passes it to `AdvisoryService::list()`. This is the exact same pattern needed for the package license filter.

**How it is reused**: The package `list.rs` endpoint handler is modified to follow the same pattern:
1. Add `license: Option<String>` to the `PackageListQuery` struct (matching how `severity: Option<String>` is defined in the advisory query struct).
2. Extract the value from the query parameters in the handler function.
3. Pass it to `PackageService::list()` as an additional parameter.
4. Use the same validation approach for returning 400 on invalid values.

**Reuse type**: Structural pattern replication -- the advisory implementation serves as the authoritative reference for how filter parameters are added in this codebase.

**Benefit**: Ensures consistency across all list endpoints. The license filter will behave identically to the severity filter in terms of query parameter handling, error responses, and service layer integration. No new patterns or abstractions are introduced.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`

**What it provides**: The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity already defines the table columns, relationships, and can be used in SeaORM queries for JOINs.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, the filter query JOINs through the `package_license` entity to match packages by license. Instead of writing raw SQL like `JOIN package_license ON ...`, we use the SeaORM relation defined in the entity to perform the join. The `apply_filter` result (the `IN` clause condition) is applied to the license column of this joined table.

**Reuse type**: Direct use of existing entity for query construction.

**Benefit**: Avoids raw SQL, leverages SeaORM's type-safe query building, and uses the relationship definitions already established in the entity layer. If the `package_license` schema ever changes, the entity will be updated in one place and all consumers (including this new filter) will pick up the change.

---

## Additional Existing Code Reused (not listed as Reuse Candidates but still reused)

### `common/src/model/paginated.rs` -- `PaginatedResults<T>`
The response wrapper is already used by the package list endpoint. No changes needed; the filter is applied before pagination, so results are still wrapped in the same `PaginatedResults<PackageSummary>` type.

### `common/src/error.rs` -- `AppError`
Used to return `400 Bad Request` for invalid license parameter values. This is the standard error type used across all endpoints. No new error variants are needed -- the existing validation error variant (with `.context()` wrapping) is sufficient.

---

## Duplication Avoided

| Potential duplication | How it was avoided |
|---|---|
| Comma-separated parameter parsing | Reused `apply_filter` from `query.rs` |
| SQL IN clause generation | Reused `apply_filter` from `query.rs` |
| Query struct with optional filter field | Followed advisory `list.rs` pattern exactly |
| Package-to-license JOIN logic | Used `package_license` SeaORM entity |
| Error handling for invalid input | Used existing `AppError` enum |
| Paginated response wrapping | Used existing `PaginatedResults<T>` |

**No new utility functions, helpers, or abstractions are introduced.** The entire implementation is composed from existing building blocks in the codebase.
