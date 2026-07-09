# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Summary

All three Reuse Candidates identified in the task description are used. No new utility functions are created. The implementation follows the "reuse first" principle from the SKILL.md: existing infrastructure handles comma-separated parsing, SQL generation, and entity relationships, leaving the implementation to wire these together following an established pattern.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`, function `apply_filter`

**What it provides:**
- Accepts a raw query parameter string (e.g., `"MIT"` or `"MIT,Apache-2.0"`)
- Splits comma-separated values into individual filter terms
- Generates the appropriate SQL condition: a simple equality check for single values, or a `WHERE ... IN (...)` clause for multiple values
- Returns a SeaORM `Condition` that can be composed into a query builder chain

**How it is reused:**

The `apply_filter` function is called directly in `modules/fundamental/src/package/service/mod.rs` within the `PackageService::list` method. When the `license` parameter is `Some(value)`, the service passes the raw string and the target column (`package_license::Column::License`) to `apply_filter`. The returned `Condition` is applied to the query via `.filter()`.

This is a direct reuse -- no wrapping, no adaptation, no new helper function. The function is imported from `common::db::query` and called exactly as it is called elsewhere in the codebase (e.g., in the advisory service for severity filtering).

**Why no new utility is created:**

`apply_filter` already handles the complete parsing-to-SQL pipeline for comma-separated multi-value parameters. Creating a new function (e.g., `parse_license_filter` or `build_license_condition`) would duplicate this exact functionality. The task explicitly instructs reuse of `apply_filter` for this reason, and the SKILL.md Step 6 states: "If they do, use or extend the existing code."

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`, the severity filter implementation

**What it provides:**

A structural template for adding an optional filter parameter to a list endpoint. The advisory list endpoint demonstrates the full pattern:

1. **Query struct pattern:** The `Query` struct in the advisory list endpoint includes an `Option<String>` field for the `severity` filter. This is deserialized from query parameters by Axum's extractor.

2. **Handler-to-service wiring:** The handler function extracts `query.severity` and passes it as an argument to `AdvisoryService::list()`. The handler does not perform any parsing or filtering logic itself.

3. **Service-level filter application:** The advisory service method receives the optional filter string, checks if it is `Some`, and if so calls `apply_filter` with the appropriate entity column to build the query condition.

**How it is reused:**

The advisory list endpoint is used as a structural reference, not as code that is imported or called. The implementation in `modules/fundamental/src/package/endpoints/list.rs` and `modules/fundamental/src/package/service/mod.rs` mirrors the advisory pattern step-by-step:

- The `Query` struct in `package/endpoints/list.rs` gains an `Option<String>` field named `license`, structurally identical to the `severity` field in the advisory `Query` struct.
- The handler in `package/endpoints/list.rs` passes `query.license` to `PackageService::list()`, following the same call pattern as the advisory handler passes `query.severity` to `AdvisoryService::list()`.
- The `PackageService::list()` method in `package/service/mod.rs` conditionally applies the filter using `apply_filter`, following the same conditional pattern used in `AdvisoryService::list()`.

By following this established pattern rather than inventing a new approach, the implementation maintains consistency across the codebase's list endpoints and reduces review friction.

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`, a SeaORM entity definition

**What it provides:**

The `package_license` entity maps the join table between packages and their declared licenses. It includes:

- Column definitions (e.g., `package_id`, `license` for the SPDX identifier)
- Relation definitions linking back to the `package` entity
- SeaORM `Entity` and `Model` derive macros for type-safe query building

**How it is reused:**

The entity is used in `modules/fundamental/src/package/service/mod.rs` to construct the JOIN query that connects packages to their licenses. Instead of writing raw SQL (`JOIN package_license ON ...`), the implementation uses SeaORM's relation-based join:

```rust
query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
```

This leverages the existing relation definition in `package_license.rs` to generate the correct JOIN condition. The `package_license::Column::License` enum variant is then used as the target column for `apply_filter`, ensuring type-safe column references.

**Why raw SQL is avoided:**

The `entity/src/package_license.rs` entity already encodes the table schema, column names, and foreign key relationships. Writing raw SQL would bypass these type-safe abstractions and create a maintenance liability if the schema changes. Using the entity is consistent with how all other modules in the codebase perform joins (e.g., `sbom_package`, `sbom_advisory` entities are used similarly for their respective joins).

## Reuse coverage summary

| Reuse Candidate | Location | Usage Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | `package/service/mod.rs` |
| Advisory severity filter | `advisory/endpoints/list.rs` | Structural pattern (followed) | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | `entity/src/package_license.rs` | Entity for JOIN query | `package/service/mod.rs` |

## New code that is NOT created (duplication avoidance)

The following utilities or helpers are explicitly **not** created, because existing code already provides their functionality:

- **No `parse_comma_separated()` function** -- `apply_filter` in `common/src/db/query.rs` already handles comma-separated parsing internally.
- **No `build_license_filter()` function** -- `apply_filter` already generates the SQL condition (equality or IN clause) based on the input.
- **No custom `LicenseFilter` struct** -- the `Option<String>` pattern used by the advisory severity filter is sufficient; a dedicated struct would add unnecessary abstraction.
- **No raw SQL for the join** -- the `package_license` SeaORM entity provides type-safe join construction via its relation definitions.
