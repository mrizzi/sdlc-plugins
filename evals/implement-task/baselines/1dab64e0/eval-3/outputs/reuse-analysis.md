# Reuse Analysis: TC-9203 -- Add Package License Filter

## Summary

All three Reuse Candidates listed in the task description are directly applicable and will be used. No new utility functions or helpers need to be created. The implementation is entirely composed of reusing existing code and following established patterns.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`
**What it provides**: Handles comma-separated multi-value query parameter parsing and SQL IN clause generation. Given a field name and a raw query string value (e.g., `"MIT,Apache-2.0"`), it splits on commas, validates the individual values, and produces a SeaORM filter condition equivalent to `WHERE field IN ('MIT', 'Apache-2.0')`. For single values, it produces a simple equality condition.

**How it will be reused**: Called directly in `PackageService::list()` (in `modules/fundamental/src/package/service/mod.rs`) to transform the raw `license` query parameter string into a database filter condition. No wrapping, no modification, no reimplementation -- direct invocation.

```rust
// In PackageService::list(), when license filter is present:
let condition = apply_filter("license_identifier", &license_param);
query = query.filter(condition);
```

**Why reuse instead of writing new code**: Writing a custom comma-split-and-IN-clause generator would duplicate the exact logic already provided by `apply_filter`. The existing function also handles edge cases (empty strings, whitespace trimming) that would need to be reimplemented. Using the shared utility ensures consistent behavior across all filtered endpoints in the application.

**Reuse type**: Direct invocation (no modification needed)

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`
**What it provides**: A structurally identical filter implementation -- the advisory list endpoint supports a `severity` query parameter using the same filtering approach needed for the `license` parameter. Specifically:
- A `Query` struct with an `Option<String>` field for the filter parameter
- Axum query parameter extraction in the handler
- Passing the optional filter value to the service layer
- The service layer conditionally applying the filter when the value is `Some`

**How it will be reused**: Used as a structural template (pattern reuse) for both the endpoint and service layer changes:

1. **Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
   - Add `license: Option<String>` to the `Query` struct, following the same field declaration pattern as `severity` in the advisory Query struct
   - Extract and pass the value in the handler function, following the same control flow

2. **Service layer** (`modules/fundamental/src/package/service/mod.rs`):
   - Add an `Option<String>` parameter to `PackageService::list()`, following the same signature extension pattern used in `AdvisoryService::list()` for the severity filter
   - Apply the filter conditionally with `if let Some(...)`, following the same guard pattern

**Why reuse instead of writing new code**: The advisory severity filter is the same problem solved for a different domain entity. Inventing a different approach would introduce inconsistency in the codebase -- all list endpoint filters should follow the same structural pattern. By replicating the advisory pattern exactly, the license filter is immediately familiar to anyone who has worked on the advisory module.

**Reuse type**: Structural pattern reuse (follow the same code structure for a parallel use case)

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`
**What it provides**: The existing SeaORM entity definition for the package-license join table. This entity maps packages to their declared licenses, with columns for `package_id` (foreign key to the package table) and a license identifier column. It includes SeaORM relation definitions that enable type-safe JOINs.

**How it will be reused**: Used in `PackageService::list()` to perform the JOIN query that connects packages to their licenses when the filter is active:

```rust
// JOIN through the package_license entity to filter by license
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(apply_filter("license_identifier", &license_param));
```

The entity's existing relation definitions are used to construct the JOIN -- no raw SQL is written, and no new entity or migration is needed.

**Why reuse instead of writing new code**: The package-license relationship already exists in the data model and is fully defined as a SeaORM entity. Writing raw SQL JOINs or creating a duplicate entity definition would bypass the ORM's type safety and relation management. The existing entity provides:
- Correct table and column names
- Type-safe foreign key references
- Relation definitions compatible with SeaORM's query builder

**Reuse type**: Direct use of existing entity (no modification needed)

## Additional Reuse Opportunities Discovered

Beyond the three listed Reuse Candidates, the following existing code is also reused:

- **`common/src/model/paginated.rs` (`PaginatedResults<T>`)**: The response wrapper for list endpoints. The license filter implementation returns the same `PaginatedResults<PackageSummary>` type -- no new response type is created.

- **`common/src/error.rs` (`AppError`)**: The standard error type for returning 400 Bad Request on invalid license values. Reused directly rather than creating custom error handling.

- **`tests/api/advisory.rs` and `tests/api/sbom.rs`**: Test file patterns (assertion style, response validation, setup/teardown) are followed for the new test file rather than inventing new test approaches.

## Code That Will NOT Be Created (Avoided Duplication)

| Potential new code | Why it is NOT needed |
|---|---|
| Custom comma-separated string parser | `apply_filter` already handles this |
| Custom SQL IN clause builder | `apply_filter` already generates IN clauses |
| New join table entity for package-license | `entity/src/package_license.rs` already exists |
| New response type for filtered results | `PaginatedResults<PackageSummary>` is unchanged |
| Custom query parameter extractor | Axum's standard `Query` derive handles extraction |
| Raw SQL for the license join | SeaORM relations on `package_license` entity provide type-safe JOINs |
