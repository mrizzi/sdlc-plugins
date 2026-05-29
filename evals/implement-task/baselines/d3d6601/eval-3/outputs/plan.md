# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Project Configuration Validation

The project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena tool naming convention and configured instances

## Parsed Task Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new branch/PR flow)

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: This file implements the `GET /api/v2/package` list endpoint handler. It currently accepts pagination and sorting query parameters but has no license filtering.

**Changes**:
- Add an optional `license` field to the query parameters struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`)
- The field type should be `Option<String>` to accept both single values (`MIT`) and comma-separated values (`MIT,Apache-2.0`)
- In the handler function, pass the `license` parameter through to the `PackageService::list` method
- Validate the license parameter: if present but empty or malformed, return 400 Bad Request using `AppError`

**Reuse**: Follow the exact Query struct pattern from the advisory list endpoint (`modules/fundamental/src/advisory/endpoints/list.rs`), which already has an optional `severity` filter field with the same structure.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: This file contains `PackageService` with `fetch` and `list` methods. The `list` method builds a database query for packages with pagination and sorting but no license filtering.

**Changes**:
- Add a `license` parameter (type `Option<String>`) to the `list` method signature
- When the `license` parameter is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and generate a SQL `IN` clause
- Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers
- The join should use the SeaORM relation between `package` and `package_license` entities
- When `license` is `None`, skip the join and filter entirely (no regression on existing behavior)

**Reuse**: 
- Call `apply_filter` from `common/src/db/query.rs` directly -- this function already handles comma-separated multi-value query parameter parsing and SQL IN clause generation
- Use `entity::package_license` for the join table entity rather than writing raw SQL

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license filter on the package list endpoint.

**Test cases** (following the assertion patterns from sibling test files in `tests/api/`):

1. **`test_list_packages_filter_single_license`**: Verify that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on specific package identifiers in the response, not just count.

2. **`test_list_packages_filter_multiple_licenses`**: Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that results contain packages with both MIT and Apache-2.0 licenses.

3. **`test_list_packages_no_license_filter`**: Verify that `GET /api/v2/package` without the license parameter returns all packages unchanged (no regression). Compare against a known baseline count and verify response shape.

4. **`test_list_packages_invalid_license`**: Verify that an invalid/malformed license value returns 400 Bad Request. Assert `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions to follow**:
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Deserialize response body to `PaginatedResults<PackageSummary>` and assert on `total_count`, `items.len()`, and specific item field values
- Use given-when-then section comments inside each test
- Add `///` doc comments on every test function
- Follow `test_<endpoint>_<scenario>` naming pattern

**Module registration**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) so the new test file is discovered by `cargo test`.

## API Changes

- `GET /api/v2/package` -- MODIFY: add optional `license` query parameter
  - `?license=MIT` -- filter to packages with MIT license (exact match on SPDX identifier)
  - `?license=MIT,Apache-2.0` -- filter to packages matching either license
  - Response shape (`PaginatedResults<PackageSummary>`) remains unchanged

## Data-Flow Trace

1. HTTP request with `?license=MIT` arrives at the Axum handler in `list.rs`
2. Query parameter struct deserializes the `license` field as `Option<String>`
3. Handler passes `license` to `PackageService::list()`
4. Service calls `apply_filter()` from `common/src/db/query.rs` to parse comma-separated values
5. Service builds a SeaORM query joining `package` to `package_license` on the license column
6. `apply_filter` generates the SQL `WHERE license_spdx_id IN (...)` clause
7. Query executes against PostgreSQL, returning filtered rows
8. Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON

All stages are connected -- the flow is COMPLETE.

## Scope Containment

All changes are strictly within the files listed in Files to Modify and Files to Create:
- `modules/fundamental/src/package/endpoints/list.rs` (modify)
- `modules/fundamental/src/package/service/mod.rs` (modify)
- `tests/api/package_license_filter.rs` (create)

No out-of-scope files will be modified. The response type `PaginatedResults<PackageSummary>` is not changed. Route registration in `modules/fundamental/src/package/endpoints/mod.rs` does not need changes since the existing route handler is being modified in place, not replaced.

## Convention Conformance

Based on the repository conventions:
- **Framework**: Axum for HTTP, SeaORM for database -- all changes use these frameworks
- **Error handling**: Return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoint returns `PaginatedResults<T>` -- unchanged
- **Query helpers**: Use shared `apply_filter` from `common/src/db/query.rs` -- reusing existing infrastructure
- **Testing**: Integration tests in `tests/api/` hitting real PostgreSQL test database

## Commit Plan

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value filtering by
SPDX license identifier. Reuses apply_filter from common query helpers
and joins through the existing package_license entity.

Implements TC-9203
```

Trailer: `Assisted-by: Claude Code`

## PR Details

- **Base branch**: main
- **Head branch**: TC-9203
- **Title**: feat(api): add license filter to package list endpoint
- **Description**: Includes Implements link to Jira issue, summary of changes, and acceptance criteria verification
