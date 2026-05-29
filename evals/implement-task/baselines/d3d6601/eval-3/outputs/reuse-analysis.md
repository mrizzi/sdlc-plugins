# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are directly applicable and will be reused in the implementation. No new logic needs to be written from scratch for query parameter parsing, SQL filter generation, or entity mapping -- existing infrastructure covers all of these concerns.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a string like `"MIT,Apache-2.0"`, it splits on commas, trims whitespace, and produces a SeaORM condition equivalent to `WHERE column IN ('MIT', 'Apache-2.0')`. For single values (no comma), it produces a simple `WHERE column = 'MIT'` equality check.

**How it will be reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some(value)`, the service will call `apply_filter(value, package_license::Column::SpdxId)` (or the equivalent column name) to generate the filter condition. This is a direct reuse -- no wrapping, no adaptation, no duplication. The function is called exactly as it is used elsewhere in the codebase.

**Why reuse instead of reimplementing**: Writing custom comma-splitting and SQL IN clause generation would duplicate the exact logic that `apply_filter` already provides. It would also risk subtle differences in edge-case handling (e.g., trailing commas, whitespace around values) that the shared function already handles consistently across all endpoints.

**Location**: `common/src/db/query.rs`

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (filter pattern)

**What it provides**: The advisory list endpoint already implements a `severity` query parameter using an optional field on a Query struct. The pattern is:
1. Define a Query struct with an `Option<String>` field for the filter parameter
2. Axum deserializes query parameters into this struct automatically
3. The handler extracts the optional filter value and passes it to the service layer
4. The service layer calls `apply_filter` when the value is present

This is structurally identical to what the license filter needs.

**How it will be reused**: The advisory list endpoint serves as the structural template for the package list endpoint changes. Specifically:
- In `modules/fundamental/src/package/endpoints/list.rs`, the existing Query struct (or equivalent parameter struct) will gain an `Option<String>` field named `license`, mirroring how the advisory endpoint defines its `severity` field
- The handler function will extract `query.license` and pass it to `PackageService::list()`, mirroring how the advisory handler passes `query.severity` to `AdvisoryService::list()`
- Error handling for invalid values will follow the same pattern used for the severity filter

**Why reuse this pattern**: The advisory filter is a proven, reviewed implementation of the exact same filtering concept. Following this pattern ensures consistency across the API surface -- consumers who are familiar with the `severity` filter on advisories will find the `license` filter on packages works identically. It also means reviewers can verify the implementation by comparing it structurally to the advisory endpoint.

**Location**: `modules/fundamental/src/advisory/endpoints/list.rs`

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity definition for the `package_license` join table. This entity maps the many-to-many relationship between packages and their declared licenses. It defines the table schema, column types, relations to the `package` entity, and any associated SeaORM traits.

**How it will be reused**: In `modules/fundamental/src/package/service/mod.rs`, the license filter query will JOIN through `package_license` to find packages that have a matching license. Instead of writing raw SQL like `JOIN package_license ON package.id = package_license.package_id WHERE package_license.spdx_id IN (...)`, the implementation will use SeaORM's relation-based join with the `package_license` entity:

```rust
// Pseudocode showing the reuse pattern:
use entity::package_license;

query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(apply_filter(license_value, package_license::Column::SpdxId));
```

The entity's column definitions (`package_license::Column::SpdxId` or equivalent) are used directly in the `apply_filter` call, and the entity's relation definitions are used for the JOIN. No raw SQL is needed.

**Why reuse this entity**: The `package_license` entity already encodes the correct table name, column names, column types, and relations. Using it ensures type safety (the Rust compiler verifies column references at compile time), avoids hardcoding table/column names as strings, and automatically benefits from any future schema changes that update the entity definition.

**Location**: `entity/src/package_license.rs`

## Summary Table

| Reuse Candidate | Location | Reuse Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | `package/service/mod.rs` |
| Advisory filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template | `package/endpoints/list.rs` |
| `package_license` entity | `entity/src/package_license.rs` | Entity import for JOIN | `package/service/mod.rs` |

## Duplication Avoidance

By reusing all three candidates:
- **No custom query parameter parsing** is written -- `apply_filter` handles it
- **No new query struct pattern** is invented -- the advisory pattern is followed exactly
- **No raw SQL** is written -- the `package_license` entity provides type-safe access
- **No new entity definitions** are needed -- the join table entity already exists

The only new code is the glue that connects these existing pieces: adding the `license` field to the query parameter struct, threading it through the handler to the service, and composing the `apply_filter` call with the `package_license` entity join in the service method.
