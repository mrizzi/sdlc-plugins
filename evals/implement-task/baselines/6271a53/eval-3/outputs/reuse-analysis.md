# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Summary

All three Reuse Candidates identified in the task are used in this implementation. No new utility functions are created that would duplicate existing functionality (constraint 5.4). The implementation composes existing infrastructure rather than reinventing it.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles parsing comma-separated multi-value query parameter strings and generates the corresponding SQL `IN` clause for filtering. It already supports both single-value and multi-value inputs.

**How it is reused**: Called directly in `modules/fundamental/src/package/service/mod.rs` when the `license` query parameter is present. The raw license string (e.g., `"MIT"` or `"MIT,Apache-2.0"`) is passed to `apply_filter`, which splits on commas and produces the appropriate filter condition. No custom parsing or SQL generation code is written -- `apply_filter` handles the full pipeline.

**Why reuse is appropriate**: Writing custom comma-splitting logic or manual SQL `IN` clause construction would directly duplicate what `apply_filter` already does. The function is the canonical way to implement multi-value query filters in this codebase.

**Location used**: `modules/fundamental/src/package/service/mod.rs` (the list method's filter application logic).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter using a Query struct pattern with an optional field. This is a complete, working reference for how to add an optional filter parameter to a list endpoint in this codebase.

**How it is reused**: The implementation in `modules/fundamental/src/package/endpoints/list.rs` follows the identical structural pattern:
1. Add an `Option<String>` field (`license`) to the endpoint's Query struct, mirroring how `severity` is declared in the advisory Query struct.
2. Extract the field from the deserialized query parameters in the handler function, mirroring the advisory handler's extraction of `severity`.
3. Forward the extracted value to the service layer, mirroring how the advisory handler passes `severity` to its service.

**Why reuse is appropriate**: The advisory severity filter and the package license filter are structurally identical -- both are optional string query parameters that filter a list endpoint using comma-separated values processed by `apply_filter`. Following the established pattern ensures consistency across endpoints and avoids inventing a new (potentially inconsistent) approach.

**Location used**: `modules/fundamental/src/package/endpoints/list.rs` (Query struct definition and handler logic).

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity that maps packages to their SPDX license identifiers via a join table. It defines the columns, relations, and model needed to query the package-license relationship.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when building the filtered query, the service JOINs through the `package_license` entity to access the license column. The entity's defined relations and column types are used directly in the SeaORM query builder -- no raw SQL is written and no new entity is created.

**Why reuse is appropriate**: The `package_license` entity is the authoritative representation of the package-to-license mapping in the database. Creating a new entity or writing raw SQL JOINs would duplicate this existing schema definition and risk inconsistency if the schema changes.

**Location used**: `modules/fundamental/src/package/service/mod.rs` (JOIN clause in the filtered list query).

---

## Additional Reuse (discovered from repository structure)

Beyond the three explicit Reuse Candidates, the implementation also leverages:

- **`common/src/model/paginated.rs`** (`PaginatedResults<T>`) -- The existing pagination wrapper is preserved as-is for the response type. No modifications needed.
- **`common/src/error.rs`** (`AppError`) -- The existing error enum is used to return 400 Bad Request for invalid license values, rather than creating a new error type.
- **`tests/api/advisory.rs`** -- Test patterns (setup, assertions, HTTP client usage) from existing integration tests are followed for consistency in the new test file.

## What is NOT created

- No new query parameter parsing utilities (would duplicate `apply_filter`).
- No new entity definitions (would duplicate `package_license.rs`).
- No new error types (existing `AppError` covers the 400 case).
- No new filter helper functions (the combination of `apply_filter` + SeaORM entity join is sufficient).
