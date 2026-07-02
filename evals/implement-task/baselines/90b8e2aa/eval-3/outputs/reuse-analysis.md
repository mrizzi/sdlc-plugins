# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are reused directly in the implementation — no new utility functions are created, and no existing functionality is duplicated.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query string (e.g., `"MIT,Apache-2.0"`) and produces the appropriate SQL filter condition.

**How it is reused**:

- **In `modules/fundamental/src/package/endpoints/list.rs`**: The `license` query parameter value (an `Option<String>`) is passed to `apply_filter` to parse the comma-separated string into individual license identifiers and generate the corresponding SQL IN clause. This handles both single-value (`?license=MIT`) and multi-value (`?license=MIT,Apache-2.0`) cases without any custom parsing logic.

- **In `modules/fundamental/src/package/service/mod.rs`**: The `PackageService::list()` method receives the parsed filter output from `apply_filter` and incorporates it into the SeaORM query builder. The filter is applied as a WHERE condition on the `package_license` table's license column.

**Why reuse instead of new code**: Writing custom comma-separated parsing or SQL IN clause generation would directly duplicate what `apply_filter` already does. The function is a shared utility specifically designed for this pattern across all list endpoints.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint's severity filter implementation demonstrates the structural pattern for adding an optional filter parameter to a list endpoint. It includes: (1) a Query struct with an optional filter field, (2) extraction and validation of the parameter in the handler, (3) passing the filter to the service layer.

**How it is reused**:

- **Pattern reuse in `modules/fundamental/src/package/endpoints/list.rs`**: The package endpoint's Query struct is extended with an `Option<String>` field for `license`, following the identical pattern used for `severity` in the advisory endpoint. The handler function follows the same control flow: extract the optional field from the query struct, call `apply_filter` if present, pass the result to the service method. This is structural/pattern reuse — the advisory endpoint serves as the template for the package endpoint modification.

- **Specific elements reused from the advisory pattern**:
  - Query struct field declaration style (`license: Option<String>` matching `severity: Option<String>`)
  - Conditional filter application (only apply when the parameter is `Some`)
  - Error handling for invalid values (return 400 via `AppError`)
  - Handler-to-service parameter passing convention

**Why reuse this pattern**: The advisory severity filter is described in the Implementation Notes as "structurally identical" to the license filter needed here. Following the same pattern ensures consistency across list endpoints, makes the codebase predictable for maintainers, and avoids inventing a new approach when a proven one exists in the same module.

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity defines the table schema, column definitions, and SeaORM relations needed to query the package-license relationship.

**How it is reused**:

- **In `modules/fundamental/src/package/service/mod.rs`**: The `PackageService::list()` method uses the `package_license` entity to construct a JOIN between the `package` table and the `package_license` table when filtering by license. The join is expressed using SeaORM's relation API (e.g., `package::Entity::find().join(JoinType::Inner, package_license::Relation::...)`) rather than raw SQL. The entity's column definitions are used to specify the filter condition on the license SPDX identifier column.

- **Specific elements used from the entity**:
  - `package_license::Entity` — the SeaORM entity for query building
  - `package_license::Column::LicenseId` (or equivalent) — for the WHERE/IN clause on license identifiers
  - `package_license::Relation::Package` (or equivalent) — for defining the JOIN relationship

**Why reuse this entity**: The `package_license` entity already encodes the table structure, column types, and relationships needed for the filter query. Writing raw SQL or defining inline join conditions would bypass SeaORM's type safety, duplicate the schema knowledge already captured in the entity, and violate the project's convention of using SeaORM entities for all database interactions.

## Summary Table

| Reuse Candidate | Location | Reuse Type | Used In |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | `endpoints/list.rs`, `service/mod.rs` |
| Advisory severity filter | `advisory/endpoints/list.rs` | Structural pattern | `package/endpoints/list.rs` |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity usage | `package/service/mod.rs` |

## Anti-Duplication Verification

No new utility functions, helpers, or shared modules are created by this implementation. All filtering, parsing, and query-building logic is delegated to existing code:

- Comma-separated parsing: handled by `apply_filter` (not reimplemented)
- SQL IN clause generation: handled by `apply_filter` (not reimplemented)
- Join table schema: defined by `package_license` entity (not redefined)
- Query struct pattern: follows advisory endpoint pattern (not reinvented)

The only new code is the glue that connects these existing components for the specific license filter use case: the `license` field on the Query struct, the validation logic in the handler, and the conditional join in the service method.
