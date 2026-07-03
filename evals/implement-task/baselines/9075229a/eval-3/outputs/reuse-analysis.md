# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are directly applicable and should be reused to avoid writing duplicate logic. This analysis details how each candidate maps to the implementation.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SQL `WHERE ... IN (...)` clause for the database query.

**How it will be reused:** This function will be called directly in the `PackageService::list()` method (in `modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter. Instead of writing custom string-splitting and SQL clause generation logic, the implementation will pass the raw license parameter string to `apply_filter`, which will:

1. Parse the comma-separated values into individual license identifiers
2. Generate the SQL `IN` clause targeting the `package_license` table's license column
3. Handle edge cases (single value, multiple values) consistently with other filters in the codebase

**Reuse type:** Direct invocation -- no modification to `apply_filter` is needed. The function is generic enough to handle the license filter use case as-is.

**Location in implementation:** Called from `modules/fundamental/src/package/service/mod.rs` within the `list` method when building the database query with an active license filter.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint's severity filter implementation serves as the structural template for the license filter. It demonstrates the established pattern for adding an optional filter query parameter to a list endpoint in this codebase, including:

- A `Query` struct with an optional filter field (e.g., `severity: Option<String>`)
- Parameter extraction in the Axum handler function
- Passing the filter value through to the service layer
- Integration with the `apply_filter` helper from `common/src/db/query.rs`

**How it will be reused:** This candidate is used as a **structural pattern reference** (not direct code invocation). The implementation will replicate the same architecture in the package endpoint:

1. **Query struct pattern:** Add an `license: Option<String>` field to the package endpoint's `Query` struct, mirroring how the advisory endpoint defines `severity: Option<String>`
2. **Handler extraction pattern:** Extract the license parameter from the query in the same way the advisory handler extracts the severity parameter
3. **Service delegation pattern:** Pass the filter to the service method using the same parameter-passing approach (optional filter parameter on the service's `list` method)
4. **Filter application pattern:** Apply the filter using `apply_filter` in the service layer, following the same sequence as the advisory service

**Reuse type:** Pattern replication -- the advisory severity filter's architecture is copied and adapted for the package license filter. The code structure, error handling approach, and data flow are all derived from this existing implementation.

**Location in implementation:** The pattern is applied across two files:
- `modules/fundamental/src/package/endpoints/list.rs` (Query struct + handler extraction)
- `modules/fundamental/src/package/service/mod.rs` (service-layer filter application)

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the database schema mapping (table name, column names, relationships) needed to join packages with their license data.

**How it will be reused:** This entity will be used directly in the database query within `PackageService::list()` to construct the JOIN between the `package` table and the `package_license` table. Instead of writing raw SQL or defining a new entity, the implementation will:

1. Import the `package_license` entity module
2. Use SeaORM's query builder to construct the JOIN: `package.id = package_license.package_id`
3. Apply the license filter condition on the `package_license` table's license column
4. Let SeaORM generate the correct SQL from the entity's column and relation definitions

**Reuse type:** Direct usage -- the entity is imported and used with SeaORM's query builder API. No modifications to the entity file are needed.

**Location in implementation:** Used in `modules/fundamental/src/package/service/mod.rs` within the `list` method's query construction logic.

## Summary Table

| Reuse Candidate | File | Reuse Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | `package/service/mod.rs` |
| Advisory severity filter | `advisory/endpoints/list.rs` | Pattern replication | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | `entity/src/package_license.rs` | Direct usage (import) | `package/service/mod.rs` |

## Code Duplication Avoided

By reusing these three candidates, the implementation avoids writing:
- Custom comma-separated parameter parsing logic (handled by `apply_filter`)
- A novel filter architecture that diverges from existing endpoint patterns (follows advisory pattern)
- Raw SQL or a new entity definition for the package-license relationship (uses existing `package_license` entity)

This ensures the license filter is consistent with the codebase's established patterns and reduces the surface area for bugs.
