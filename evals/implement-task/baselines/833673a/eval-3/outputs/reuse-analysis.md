# Reuse Analysis for TC-9203

## Overview

The task description lists three Reuse Candidates. All three are reused in the implementation plan. No new utility functions are created that duplicate existing functionality.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** A shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. This function takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SQL `IN (...)` clause for filtering.

**How it is reused:** Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) when the `license` parameter is present. The license string from the query parameter is passed to `apply_filter`, which handles:
- Splitting comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
- Generating the SQL `IN` clause for the `package_license` table's license column
- Handling the single-value case (e.g., `"MIT"` becomes a simple equality check or single-element `IN`)

**Why direct reuse is correct:** The `apply_filter` function already handles exactly the parsing and SQL generation needed for this feature. Writing a new parser for comma-separated values or manually constructing SQL `IN` clauses would duplicate `apply_filter`'s functionality and violate the reuse-first principle (constraint 5.4). The license filter is structurally identical to other filters in the codebase that already use `apply_filter`.

**No wrapper or adapter needed:** `apply_filter` is called directly -- no intermediate utility function, wrapper, or adapter is created.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A reference implementation of the exact pattern needed -- the advisory list endpoint's `severity` query parameter filter. This includes:
- A Query struct with an optional filter field (`severity: Option<String>`)
- Axum query parameter extraction into the struct
- Delegation of the filter value to the service layer

**How it is reused:** The pattern is followed structurally (not copied verbatim) when modifying the package list endpoint:
- The existing Query struct in `modules/fundamental/src/package/endpoints/list.rs` gets a new `license: Option<String>` field, mirroring how `severity: Option<String>` is declared in the advisory Query struct
- The handler passes `query.license` to `PackageService::list()`, mirroring how the advisory handler passes `query.severity` to `AdvisoryService::list()`
- The field is optional, so omitting the parameter returns all packages (same behavior as omitting severity in the advisory endpoint)

**Why pattern reuse is correct:** The advisory severity filter is described in the task as "structurally identical to the license filter needed here." Following the same struct pattern ensures consistency across the codebase's list endpoints and avoids inventing a different approach for the same kind of operation.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** An existing SeaORM entity that maps the `package_license` join table in the database. This entity defines the relationship between packages and their declared licenses, with columns for the package ID and the license identifier (SPDX).

**How it is reused:** Used in `PackageService::list()` to perform the JOIN query when filtering by license:
- The service JOINs the `package` table to the `package_license` table using this entity's relation definitions
- The `apply_filter`-generated condition is applied to the license column defined in this entity
- SeaORM's relation and query builder APIs are used with this entity -- no raw SQL is written

**Why entity reuse is correct:** The `package_license` entity already encodes the database schema for the package-to-license relationship. Writing raw SQL JOINs or creating a new entity for the same table would duplicate what already exists and risk schema drift. Using the existing entity ensures type safety and consistency with the rest of the ORM-based data access layer.

## Summary

| Reuse Candidate | Reuse Type | Used In |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `modules/fundamental/src/package/service/mod.rs` |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern (Query struct with optional filter field) | `modules/fundamental/src/package/endpoints/list.rs` |
| `entity/src/package_license.rs` | Entity reuse for JOIN query | `modules/fundamental/src/package/service/mod.rs` |

No new utility functions, helpers, or abstractions were created. All filtering logic leverages existing code.
