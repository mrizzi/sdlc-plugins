# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are directly applicable and should be used in the implementation. No new utility functions are needed -- the existing codebase already provides all the building blocks required for this feature.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and builds a `WHERE column IN ('MIT', 'Apache-2.0')` clause for the database query.

**How it will be reused:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, call `apply_filter` directly to parse the comma-separated license string and generate the filter condition. This replaces what would otherwise be custom string-splitting and SQL clause construction logic.

**Why reuse instead of writing new code:** Writing custom comma-splitting and IN clause generation would duplicate the exact functionality that `apply_filter` already provides. The function is specifically designed for this use case -- shared query parameter filtering -- and is already used by other modules (e.g., the advisory severity filter). Reusing it ensures consistent parsing behavior (edge case handling, escaping, validation) across all filter parameters in the API.

**Integration point:** The service's `list` method will import `apply_filter` from `common::db::query` and call it when building the SeaORM query, passing the license column and the raw filter string.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** The advisory list endpoint implements a `severity` query parameter filter using a pattern that is structurally identical to what the package license filter requires. Specifically:
- A query parameter struct with an `Option<String>` field for the filter
- Extraction logic in the handler function that reads the optional field
- Forwarding the filter value to the service layer
- Error handling for invalid filter values returning 400 Bad Request

**How it will be reused:** The advisory `list.rs` serves as the reference implementation -- the package `list.rs` will follow the same structural pattern:
1. Add an `Option<String>` field named `license` to the package list endpoint's query parameter struct, mirroring how `severity` is defined in the advisory query struct
2. In the handler function, extract the `license` value using the same pattern the advisory handler uses to extract `severity`
3. Pass the value to `PackageService::list()` following the same calling convention that the advisory handler uses with `AdvisoryService::list()`
4. Handle validation errors the same way the advisory handler does

**Why reuse this pattern:** The advisory severity filter is a proven, reviewed implementation of the exact same feature shape (optional comma-separated filter on a list endpoint). Following its pattern ensures consistency across the API, makes the codebase predictable for maintainers, and avoids introducing an alternative filter approach that would fragment the codebase's conventions.

**Not copied verbatim:** The code is not copy-pasted -- the pattern and approach are followed while adapting to the package domain (different field name, different entity, different service method).

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines:
- The table structure (columns: `package_id`, `license`, and likely a primary key)
- SeaORM model and ActiveModel types for type-safe queries
- Relation definitions that connect `Package` to `PackageLicense` (and vice versa)

**How it will be reused:** In `modules/fundamental/src/package/service/mod.rs`, use the `PackageLicense` entity to construct the JOIN query:
1. When the license filter is active, join `Package` to `PackageLicense` using SeaORM's relation-based join API (e.g., `Package::find().join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())`)
2. Apply the filter condition on `package_license::Column::License` using the values parsed by `apply_filter`
3. Use `DISTINCT` on the package selection to prevent duplicate results when a package has multiple matching licenses

**Why reuse instead of raw SQL:** The `package_license` entity already encodes the table schema and foreign key relationships in Rust types. Using it:
- Provides compile-time type safety for column names and relations
- Follows the SeaORM convention used throughout the codebase (no raw SQL)
- Automatically adapts if the table schema changes (via migration + entity regeneration)
- Leverages existing relation definitions rather than hardcoding join conditions

## Summary

| Reuse Candidate | Location | How Used | Avoids |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Called directly in PackageService to parse comma-separated license values and generate SQL IN clause | Writing custom string splitting and SQL clause generation |
| Advisory severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural reference for the query struct, handler extraction, and service forwarding pattern | Inventing a different filter parameter approach |
| `PackageLicense` entity | `entity/src/package_license.rs` | Used for type-safe SeaORM JOIN query from Package to PackageLicense | Writing raw SQL joins or hardcoding table/column names |

No new utility functions are proposed. All filtering, parsing, and query construction needs are covered by the existing `apply_filter` function and SeaORM entity infrastructure.
