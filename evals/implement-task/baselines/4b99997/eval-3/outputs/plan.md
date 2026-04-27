# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint in the
trustify-backend repository. The filter supports exact-match filtering on SPDX license
identifiers, with both single-value (`?license=MIT`) and comma-separated multi-value
(`?license=MIT,Apache-2.0`) usage.

## Project Configuration Validation (Step 0)

The project CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` with rust-analyzer

## Dependency Check (Step 2)

No dependencies listed -- proceed immediately.

## Branch (Step 5)

Create feature branch: `git checkout -b TC-9203`

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** This file implements the `GET /api/v2/package` list endpoint. It
currently accepts query parameters for pagination and possibly other filters, but has
no `license` query parameter.

**Changes:**

1. **Add `license` field to the Query struct**: Following the pattern in
   `modules/fundamental/src/advisory/endpoints/list.rs` (where `severity` is an
   optional query parameter), add an `Option<String>` field named `license` to the
   endpoint's `Query` struct (or equivalent Axum extractor struct).

   ```rust
   /// Optional license filter -- accepts a single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Pass the license parameter to the service layer**: In the handler function,
   extract `query.license` and pass it to `PackageService::list()` as a new parameter
   (or as part of an options/filter struct, following the pattern used by the advisory
   severity filter).

3. **Validate the license parameter**: Before passing to the service, validate that
   the license values are non-empty strings. If an empty or whitespace-only value is
   provided, return a `400 Bad Request` response using `AppError` from
   `common/src/error.rs`. Follow the existing error handling convention of
   `Result<T, AppError>` with `.context()` wrapping.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with a `list` method that queries the
database for packages and returns `PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` filter parameter to the `list` method**: Add an
   `Option<String>` parameter (or extend an existing filter/options struct) to accept
   the license filter value.

   ```rust
   /// Lists packages with optional filtering.
   ///
   /// When `license` is provided, filters results to packages matching the given
   /// SPDX license identifier(s). Supports comma-separated values for OR matching.
   pub async fn list(
       &self,
       // ... existing parameters ...
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Build the license filter query**: Use `apply_filter` from
   `common/src/db/query.rs` to handle the comma-separated parsing and generate the
   SQL `IN` clause. This is the same mechanism used by the advisory severity filter.

3. **Join through `package_license` entity**: Use the SeaORM entity defined in
   `entity/src/package_license.rs` to join the `package` table with the
   `package_license` table. Apply the license filter on the joined
   `package_license.license` column. The join ensures that only packages with a
   matching license association are returned.

   The query construction follows the SeaORM pattern:

   ```rust
   // When license filter is present, join through package_license
   if let Some(ref license_value) = license {
       let license_values = apply_filter(license_value);  // parses comma-separated values
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(package_license::Column::License.is_in(license_values));
   }
   ```

4. **Preserve response shape**: The return type `PaginatedResults<PackageSummary>`
   remains unchanged. The license filter only narrows the result set.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter functionality.

**Structure:** Follow the test conventions observed in sibling test files
(`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for validation failures
- Follow `test_<endpoint>_<scenario>` naming convention
- Hit a real PostgreSQL test database
- Add doc comments to every test function
- Use given-when-then section comments for non-trivial tests

**Test functions to implement:**

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: packages with MIT and Apache-2.0 licenses in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only MIT-licensed packages are returned
}

/// Verifies that comma-separated license values return packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: packages with various licenses in the database
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned unchanged
}

/// Verifies that an invalid/empty license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // Given: a request with an empty license parameter
    // When: GET /api/v2/package?license=
    // Then: response status is 400 Bad Request
}
```

**Test assertions will be value-based** (not length-only): each test will assert on
specific package names or identifiers in the response, not just on `items.len()`.

### 2. Module registration for the new test file

The new test file `tests/api/package_license_filter.rs` needs to be registered as a
module. Check `tests/Cargo.toml` for test target configuration, and add a `mod
package_license_filter;` declaration in whatever test harness entry point exists
(typically `tests/api/mod.rs` or referenced from `Cargo.toml`).

## Files NOT Modified (scope containment)

The following files are referenced in the task but are used as-is, not modified:

- `common/src/db/query.rs` -- reused directly (its `apply_filter` function)
- `entity/src/package_license.rs` -- reused directly (SeaORM entity for joins)
- `modules/fundamental/src/advisory/endpoints/list.rs` -- pattern reference only
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` used unchanged
- `common/src/error.rs` -- `AppError` used unchanged

## API Changes

| Endpoint | Change | Details |
|---|---|---|
| `GET /api/v2/package` | MODIFY | Add optional `license` query parameter |
| `GET /api/v2/package?license=MIT` | NEW behavior | Single license exact match |
| `GET /api/v2/package?license=MIT,Apache-2.0` | NEW behavior | Multi-value OR filter |

The response shape (`PaginatedResults<PackageSummary>`) is not changed.

## Convention Conformance

Based on the repository structure and conventions described:

- **Framework**: Axum for HTTP, SeaORM for database -- all new code follows this
- **Module pattern**: `model/ + service/ + endpoints/` -- changes are within the existing package module structure
- **Error handling**: `Result<T, AppError>` with `.context()` -- will use this for the license validation error
- **Query helpers**: `common/src/db/query.rs` `apply_filter` function -- direct reuse
- **Response types**: `PaginatedResults<T>` -- no change to response type
- **Testing**: Integration tests in `tests/api/` with real PostgreSQL -- following this pattern
- **Naming**: Following `verb_noun` convention for service methods

## Data-Flow Trace

```
HTTP request (GET /api/v2/package?license=MIT)
  -> Axum query extractor (endpoints/list.rs: Query struct)
  -> Validation (non-empty check, 400 on failure)
  -> PackageService::list() (service/mod.rs)
  -> apply_filter() parses comma-separated values (common/src/db/query.rs)
  -> SeaORM query with JOIN on package_license entity
  -> SQL: SELECT ... FROM package INNER JOIN package_license ON ... WHERE license IN ('MIT')
  -> PaginatedResults<PackageSummary> response (unchanged shape)
```

All stages are connected -- no incomplete paths.

## Acceptance Criteria Verification Plan

| Criterion | Verified By |
|---|---|
| `?license=MIT` returns only MIT packages | `test_list_packages_filter_single_license` |
| `?license=MIT,Apache-2.0` returns either | `test_list_packages_filter_multiple_licenses` |
| No `license` param returns all packages | `test_list_packages_no_license_filter` |
| Response shape unchanged | All tests validate `PaginatedResults<PackageSummary>` deserialization |
| Invalid license returns 400 | `test_list_packages_invalid_license_returns_400` |

## Self-Verification Checklist

- [ ] `git diff --name-only` contains only in-scope files
- [ ] No sensitive patterns in staged diff
- [ ] Documentation: API docs updated if they exist (check `docs/api.md`)
- [ ] CONVENTIONS.md CI checks run and pass
- [ ] Duplication check: no overlapping filter logic elsewhere
- [ ] Contract & sibling parity with advisory severity filter implementation

## Commit Plan

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value exact-match
filtering on SPDX license identifiers. Reuses the existing
apply_filter helper and package_license entity for the join query.

Implements TC-9203
```

With `--trailer="Assisted-by: Claude Code"`.
