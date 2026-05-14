# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Step 0 — Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID present
- **Code Intelligence**: Tool naming convention documented, `serena_backend` instance configured with `rust-analyzer`

Validation passes. Proceed with implementation.

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Jira ID**: TC-9203
- **Dependencies**: None
- **Target PR**: None (default flow — create new branch)

## Step 4 — Understand the Code

### Files to Modify

#### 1. `modules/fundamental/src/package/endpoints/list.rs`
- **Current state**: Implements `GET /api/v2/package` list endpoint. Contains a query parameter struct (likely `PackageQuery` or similar) and a handler function that calls `PackageService::list()`.
- **Planned inspection**: Use `mcp__serena_backend__get_symbols_overview` to see the existing query struct and handler signature. Use `mcp__serena_backend__find_symbol` to read the handler body.

#### 2. `modules/fundamental/src/package/service/mod.rs`
- **Current state**: Contains `PackageService` with `fetch` and `list` methods. The `list` method builds a database query, applies pagination/sorting, and returns `PaginatedResults<PackageSummary>`.
- **Planned inspection**: Use `mcp__serena_backend__find_symbol` on `PackageService::list` with `include_body=true` to understand the current query construction.

### Sibling / Reference Files to Inspect

#### 3. `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate)
- **Purpose**: Reference implementation — the advisory list endpoint already implements a `severity` query parameter using the same filtering pattern needed for `license`.
- **Planned inspection**: Use `mcp__serena_backend__get_symbols_overview` to see the query struct pattern (likely an `AdvisoryQuery` struct with an `Option<String>` field for `severity`). Read the handler to see how it passes the filter to the service layer.

#### 4. `common/src/db/query.rs` (Reuse Candidate)
- **Purpose**: Contains `apply_filter` function that handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation.
- **Planned inspection**: Use `mcp__serena_backend__find_symbol` on `apply_filter` with `include_body=true` to understand its signature, parameters, and how it integrates with SeaORM query builders.

#### 5. `entity/src/package_license.rs` (Reuse Candidate)
- **Purpose**: SeaORM entity mapping the `package_license` join table — links packages to their licenses. Required for the JOIN when filtering by license.
- **Planned inspection**: Use `mcp__serena_backend__get_symbols_overview` to see the entity's columns and relations.

### Sibling Test Files

#### 6. `tests/api/advisory.rs`
- **Purpose**: Reference for test conventions — advisory endpoint integration tests likely include filter tests for the `severity` parameter.
- **Planned inspection**: Use `mcp__serena_backend__get_symbols_overview` to see test function names and patterns.

#### 7. `tests/api/sbom.rs`
- **Purpose**: Additional reference for test conventions — another sibling endpoint test file.

### CONVENTIONS.md

- Check for `CONVENTIONS.md` at repository root for CI check commands and project conventions.
- Extract any verification commands for Step 9.

### Documentation Files

- `README.md` at repo root
- `docs/api.md` — API reference, may need updating to document the new `license` query parameter

## Step 5 — Create Branch

```
git checkout -b TC-9203
```

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the query parameter struct**: Add an `Option<String>` field named `license` to the existing query struct (following the same pattern as the `severity` field in the advisory list endpoint's query struct).

   ```rust
   /// Optional license filter — supports single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Pass the license filter to the service layer**: In the handler function, extract the `license` field from the query struct and pass it to `PackageService::list()` as an additional parameter (or within an options/filter struct, depending on the existing calling convention).

3. **Add validation**: If the license parameter is present but contains empty segments after splitting on commas (e.g., `?license=,` or `?license=MIT,,Apache-2.0`), return a `400 Bad Request` using the `AppError` enum from `common/src/error.rs`.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add license filter parameter to `list` method signature**: Add an `Option<String>` parameter (or extend an existing filter/options struct) for the license filter.

2. **Build the filter query using `apply_filter`**: When the license parameter is present:
   - Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate the appropriate SQL `IN` clause.
   - JOIN through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers.
   - The join should use SeaORM's `JoinType::InnerJoin` on the package-to-package_license relationship.

3. **Preserve existing behavior**: When the license parameter is `None`, the query remains unchanged — no JOIN is added, and all packages are returned (no regression).

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

See Step 7 below for full test plan.

### API Changes

- `GET /api/v2/package?license=MIT` — add optional `license` query parameter
- `GET /api/v2/package?license=MIT,Apache-2.0` — support comma-separated values
- Response shape (`PaginatedResults<PackageSummary>`) remains unchanged

### Module Registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test runner's module tree) so the new test file is compiled and executed.

### Documentation Impact

- Update `docs/api.md` if it documents the `GET /api/v2/package` endpoint — add the `license` query parameter with description and examples.

## Step 7 — Write Tests

### File: `tests/api/package_license_filter.rs` (CREATE)

Following the test conventions from sibling files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given: packages with MIT and Apache-2.0 licenses exist in the database
    // When: GET /api/v2/package?license=MIT
    // Then: only packages with MIT license are returned
    // Assert: response status is 200, items contain only MIT-licensed packages,
    //         verify specific package identifiers (value-based assertions)
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given: packages with MIT, Apache-2.0, and GPL-3.0 licenses exist
    // When: GET /api/v2/package?license=MIT,Apache-2.0
    // Then: packages with MIT or Apache-2.0 are returned, GPL-3.0 excluded
    // Assert: response status is 200, verify returned packages by identifier
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given: packages with various licenses exist
    // When: GET /api/v2/package (no license parameter)
    // Then: all packages are returned (no regression)
    // Assert: response status is 200, total_count matches expected, items contain all packages
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // Given: the API is running
    // When: GET /api/v2/package?license=
    // Then: 400 Bad Request is returned
    // Assert: response status is 400
}
```

All tests use `assert_eq!(resp.status(), StatusCode::OK)` (or `BAD_REQUEST`) pattern and validate specific field values, not just collection lengths.

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `?license=MIT` returns only MIT-licensed packages | Covered by `test_list_packages_filter_single_license` |
| `?license=MIT,Apache-2.0` returns packages matching either | Covered by `test_list_packages_filter_multiple_licenses` |
| No `license` parameter returns all packages | Covered by `test_list_packages_no_license_filter` |
| Response shape unchanged | Tests validate `PaginatedResults<PackageSummary>` deserialization |
| Invalid license values return 400 | Covered by `test_list_packages_invalid_license_returns_400` |

## Step 9 — Self-Verification Checklist

1. **Scope containment**: `git diff --name-only` should show only the 3 files listed above (2 modified, 1 created), plus potentially `tests/api/mod.rs` for module registration and `docs/api.md` for documentation — flag any others for user approval.
2. **Untracked file check**: The new test file `tests/api/package_license_filter.rs` will be untracked — verify it is referenced from the test module tree and stage it.
3. **Sensitive-pattern check**: Search staged diff for passwords, API keys, secrets.
4. **Duplication check**: Verify no existing license filter logic exists elsewhere in the codebase.
5. **Data-flow trace**: `license` query param → parsed in endpoint → passed to `PackageService::list` → `apply_filter` generates SQL IN clause → JOINs `package_license` table → filtered results returned as `PaginatedResults<PackageSummary>` — **COMPLETE**.
6. **Contract & sibling parity**: Verify the new query struct field follows the same `Option<String>` + `#[serde(default)]` pattern as advisory's severity field.
7. **CI checks**: Run commands from `CONVENTIONS.md` (if present), otherwise `cargo build && cargo test && cargo clippy`.

## Step 10 — Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX license filtering.
Reuses apply_filter from common query helpers and joins through the
existing package_license entity.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --title "feat(api): add license filter to package list endpoint" \
  --body "..."
```

## Step 11 — Update Jira

- Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
- Add comment summarizing changes and linking to PR
- Transition TC-9203 to "In Review"
