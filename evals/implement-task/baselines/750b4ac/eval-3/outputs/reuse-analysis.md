# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Overview

The task description includes a **Reuse Candidates** section listing three pieces of existing
code that should be reused. This analysis details how each candidate would be used in the
implementation, and whether any additional reuse opportunities exist.

## Reuse Candidates from Task Description

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:**
- Handles comma-separated multi-value query parameter parsing
- Generates SQL `IN` clause from the parsed values
- Shared utility already used by other modules in the codebase

**How it would be reused:**
- Called directly from `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) when the `license` parameter is present
- The license query string (e.g., `"MIT,Apache-2.0"`) is passed to `apply_filter`, which splits on commas and produces the appropriate filter condition
- No modifications to `apply_filter` are needed -- it is used as-is
- This eliminates the need to write custom parsing or SQL generation logic for the license filter

**Reuse type:** Direct invocation -- no changes to the existing code

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
- A structural reference implementation showing how to add an optional filter query parameter to a list endpoint
- Demonstrates the Query struct pattern with an optional field for filtering
- Shows how the filter value flows from HTTP query parameter extraction through to the service layer

**How it would be reused:**
- The advisory list endpoint's severity filter implementation is the architectural template for the license filter
- The same pattern is replicated in the package list endpoint:
  1. Add an `Option<String>` field (named `license`) to the package endpoint's Query struct, mirroring how `severity` is defined in the advisory Query struct
  2. Extract the value from the deserialized query parameters using Axum's `Query` extractor (same mechanism)
  3. Pass the optional value to the service layer method (same calling pattern)
  4. In the service layer, conditionally apply the filter only when the value is `Some` (same control flow)
- No code is copied verbatim -- the pattern is followed structurally for the license domain

**Reuse type:** Structural pattern reuse -- follow the same architecture and code organization, adapted for the license field instead of severity

### 3. `entity/src/package_license.rs` (package-license join entity)

**What it provides:**
- The SeaORM entity definition for the `package_license` database table
- Maps the many-to-many relationship between packages and their declared licenses
- Provides typed column references and relation definitions for building queries

**How it would be reused:**
- Used in the `PackageService::list` method to build a JOIN query that connects packages to their licenses
- The entity's relation definitions are used with SeaORM's query builder to join `package` to `package_license` on `package.id = package_license.package_id`
- The entity's license column is referenced in the WHERE clause (via `apply_filter`) to match against the requested license SPDX identifiers
- This replaces the need for raw SQL JOIN statements -- the existing entity provides type-safe query building
- No modifications to the entity are needed -- it is used as-is

**Reuse type:** Direct invocation -- use existing entity relations and columns in query building, no changes needed

## Reuse Decision Summary

| Reuse Candidate | Location | Reuse Type | Modifications Needed |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | None -- used as-is |
| Advisory severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern reuse | None -- pattern replicated for license domain |
| `package_license` entity | `entity/src/package_license.rs` | Direct invocation | None -- entity used as-is for JOIN |

## Additional Reuse Opportunities

### `common/src/model/paginated.rs` -- PaginatedResults<T>

- **Already in use** by the package list endpoint
- The license filter does not change the response type -- `PaginatedResults<PackageSummary>` continues to be the return type
- No additional reuse action needed; just confirming it remains unchanged

### `common/src/error.rs` -- AppError

- **Already in use** by the package endpoint handlers
- Used for returning 400 Bad Request when an invalid license value is provided
- The existing `AppError` enum likely already has a variant suitable for validation errors (following the pattern used in advisory and other endpoints)
- No additional reuse action needed; just confirming it is used for error responses

### Test patterns from `tests/api/advisory.rs`

- The advisory endpoint integration tests serve as the template for the new `tests/api/package_license_filter.rs` test file
- Test setup patterns (database fixture creation, HTTP client configuration, response deserialization) are reused from the advisory test file
- Assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`, body validation) follow the same conventions

## What is NOT Reused (and Why)

- **No new utility functions created**: The `apply_filter` function already provides all the filtering logic needed. There is no need to create a license-specific filter utility.
- **No modifications to existing shared code**: All three reuse candidates are used without modification. The implementation is purely additive -- new code in the package module that composes existing pieces.
- **No raw SQL**: The SeaORM entity (`package_license.rs`) and query builder (`query.rs`) provide type-safe query construction, eliminating the need for raw SQL strings.

## Impact on Existing Code

The reuse approach ensures minimal risk:

1. **`apply_filter`** is called with the same interface it already supports -- no risk of breaking other callers
2. **Advisory severity filter** is only used as a reference pattern -- no changes to advisory code
3. **`package_license` entity** is used read-only in a JOIN -- no modifications to the entity definition

All changes are confined to the package module (`endpoints/list.rs` and `service/mod.rs`) plus the new test file. No shared code is modified.
