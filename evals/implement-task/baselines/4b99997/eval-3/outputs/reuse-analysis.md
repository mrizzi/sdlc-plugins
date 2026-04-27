# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description identifies three reuse candidates. All three are directly
applicable and will be used in the implementation. No new utility code needs to be
written -- the entire filter mechanism is assembled from existing components.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:** The `apply_filter` function handles parsing of comma-separated
multi-value query parameter strings and generates SQL `IN` clause conditions. It
already handles:
- Single value input (e.g., `"MIT"`) -- produces a single-element filter
- Comma-separated input (e.g., `"MIT,Apache-2.0"`) -- splits and produces a
  multi-element `IN` clause
- Whitespace trimming around values

**How it will be used:** Called directly in `PackageService::list()` to parse the raw
`license` query string into a list of filter values. The parsed values are then passed
to SeaORM's `.is_in()` method on the license column.

```rust
// In modules/fundamental/src/package/service/mod.rs
use common::db::query::apply_filter;

if let Some(ref license_value) = license {
    let license_values = apply_filter(license_value);
    query = query.filter(package_license::Column::License.is_in(license_values));
}
```

**Reuse type:** Direct call -- no modification, extension, or wrapping needed. The
function's existing interface exactly matches the requirements.

**Why reuse matters here:** Writing custom comma-separation parsing logic would
duplicate what `apply_filter` already does, introducing inconsistency risk. If the
parsing behavior ever changes (e.g., adding support for negation or wildcard
patterns), the license filter would automatically benefit from the shared
implementation.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A complete, working example of how to add an optional filter
query parameter to a list endpoint in this codebase. The advisory `severity` filter
demonstrates:
- Adding an `Option<String>` field to the `Query` extractor struct
- Passing the extracted value through to the service layer
- The service layer conditionally applying the filter when the value is `Some`
- Integration with `apply_filter` for comma-separated multi-value support

**How it will be used:** The advisory severity filter serves as the structural
template for the package license filter. The implementation will mirror its pattern
in three places:

1. **Endpoint Query struct** (`package/endpoints/list.rs`): Add `license: Option<String>`
   to the query parameters, exactly as `severity: Option<String>` exists in the
   advisory endpoint.

2. **Handler function** (`package/endpoints/list.rs`): Pass `query.license` to the
   service method, following how the advisory handler passes `query.severity`.

3. **Service method** (`package/service/mod.rs`): Add the `license` parameter and
   conditionally apply the filter in the database query, matching the advisory
   service's conditional severity filter logic.

**Reuse type:** Structural pattern replication -- the advisory code is not called or
imported, but its architecture is followed to ensure consistency across modules.
This is a convention-conformance reuse: the advisory module establishes the
"how to add a filter" pattern, and the package module follows it.

**Why reuse matters here:** Deviating from this established pattern would create
inconsistency between modules. A developer familiar with the advisory severity filter
should immediately recognize the package license filter as following the same
approach. This reduces cognitive load for code reviewers and future maintainers.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:** A SeaORM entity definition for the `package_license` database
table, which is the join table mapping packages to their declared licenses. This
entity includes:
- Column definitions (including the `license` column for SPDX identifiers)
- Relation definitions (linking to the `package` entity)
- SeaORM model and ActiveModel implementations

**How it will be used:** The entity is used in the `PackageService::list()` method to
construct a JOIN query between the `package` table and the `package_license` table.
The join is needed because license information is stored in a separate table, not
directly on the package entity.

```rust
// In modules/fundamental/src/package/service/mod.rs
use entity::package_license;

query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(package_license::Column::License.is_in(license_values));
```

**Reuse type:** Direct use of existing entity -- no modification needed. The entity
already defines the columns and relations required for the filter join.

**Why reuse matters here:** Writing raw SQL for the join would bypass SeaORM's type
safety, relationship management, and query composition. The existing entity already
encodes the correct table name, column names, and foreign key relationships. Using it
ensures the join is correct and consistent with how other parts of the codebase
interact with the package-license relationship.

---

## Additional Reuse (Discovered, Not Listed in Task)

### `common/src/error.rs::AppError`

The `AppError` enum from `common/src/error.rs` will be reused for the 400 Bad Request
validation error when an invalid (empty) license value is provided. This is the
standard error type used by all handlers in the codebase (convention:
`Result<T, AppError>` with `.context()` wrapping). No new error types need to be
created.

### `common/src/model/paginated.rs::PaginatedResults<T>`

The existing `PaginatedResults<PackageSummary>` response type is reused unchanged.
The license filter narrows the result set but does not alter the response shape.
This is a key requirement: the filter is purely additive to the input, not a change
to the output.

---

## Summary

| Reuse Candidate | Location | Reuse Type | Modification Required |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct function call | None |
| Advisory severity filter pattern | `advisory/endpoints/list.rs` | Structural template | None (pattern replication) |
| `package_license` entity | `entity/src/package_license.rs` | Direct entity use (JOIN) | None |
| `AppError` | `common/src/error.rs` | Direct use | None |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Direct use | None |

All five reusable components are used as-is. Zero new utility code is written. The
entire feature is assembled by composing existing building blocks following an
established pattern.
