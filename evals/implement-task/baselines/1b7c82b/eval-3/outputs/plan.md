# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting
both single-value and comma-separated multi-value filtering by SPDX license identifier.

## Step 0 — Validate Project Configuration

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, custom fields
- **Code Intelligence**: Serena instance `serena_backend` with `rust-analyzer`

Validation passes. Proceed.

## Step 1 — Parse Task Description

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new PR flow)

### Parsed Sections

| Section | Content |
|---|---|
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` (single), `GET /api/v2/package?license=MIT,Apache-2.0` (multi) |
| Reuse Candidates | `common/src/db/query.rs::apply_filter`, advisory list endpoint pattern, `entity/src/package_license.rs` |

## Step 4 — Understand the Code

### Code Inspection Plan

Using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`
on the following files:

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current package list
   endpoint handler. Inspect the existing query parameter struct and handler function
   to understand where the `license` field should be added.

2. **`modules/fundamental/src/package/service/mod.rs`** — PackageService list method.
   Inspect the current method signature and query construction to understand where
   to inject the license filter.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (sibling/reuse) — the
   advisory list endpoint with the existing `severity` filter. This is the structural
   template for the license filter implementation.

4. **`common/src/db/query.rs`** — shared query builder. Locate the `apply_filter`
   function to understand its signature, parameters, and how it handles comma-separated
   multi-value parsing.

5. **`entity/src/package_license.rs`** — the package-license join entity. Understand
   the SeaORM entity structure and relationships to use in the JOIN query.

6. **`modules/fundamental/src/package/model/summary.rs`** — PackageSummary struct.
   Verify the `license` field exists and understand the response shape.

### Sibling Convention Analysis

**Sibling endpoints inspected** (2-3 siblings in `modules/fundamental/src/*/endpoints/list.rs`):
- `modules/fundamental/src/advisory/endpoints/list.rs`
- `modules/fundamental/src/sbom/endpoints/list.rs`

**Discovered conventions:**
- **Query parameter struct**: Each list endpoint defines a `Query` struct (or similar)
  with `#[derive(Deserialize)]` containing optional fields for filters, plus pagination fields.
- **Handler signature**: Handlers take `Query<QueryParams>` extractor and return
  `Result<Json<PaginatedResults<T>>, AppError>`.
- **Error handling**: Handlers use `Result<T, AppError>` with `.context()` wrapping
  from the `anyhow` crate.
- **Filter application**: Filters are applied in the service layer, not the handler.
  The handler extracts parameters and passes them to the service method.
- **Response type**: All list endpoints return `PaginatedResults<T>` from
  `common/src/model/paginated.rs`.

### Test Convention Analysis

**Sibling test files inspected:**
- `tests/api/advisory.rs`
- `tests/api/sbom.rs`

**Discovered test conventions:**
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status
  code checks, followed by body deserialization into the expected response type.
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`,
  and at least one item's key fields.
- **Error cases**: All endpoint tests include a test for invalid input returning
  `StatusCode::BAD_REQUEST`.
- **Test naming**: Tests follow `test_<endpoint>_<scenario>` pattern.
- **Test setup**: Tests use a real PostgreSQL test database with fixture seeding at the
  start of each test function.
- **Documentation**: Sibling tests do not consistently have doc comments, but per
  implement-task rules, all new test functions will include `///` doc comments.

### Documentation Files Identified

- `README.md` (repository root)
- `docs/api.md` (REST API reference)
- `CONVENTIONS.md` (repository root, if it exists)

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root. If present, extract CI check commands.
If not present, proceed with standard build/lint checks (`cargo build`, `cargo clippy`,
`cargo fmt --check`).

## Step 5 — Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named
   `license` to the existing query parameter struct used by the list handler. This
   follows the same pattern as the `severity` field in the advisory list endpoint's
   Query struct.

   ```rust
   #[derive(Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (pagination, sort, etc.)
       /// Optional license filter — single SPDX ID or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass `license` to the service layer**: In the handler function, extract
   `query.license` and pass it to `PackageService::list()` as an additional parameter.

   ```rust
   let result = service
       .list(/* existing params */, query.license.as_deref())
       .await
       .context("failed to list packages")?;
   ```

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Update the `list` method signature**: Add `license: Option<&str>` parameter to
   the `PackageService::list()` method.

2. **Build the license filter query**: When `license` is `Some`, use
   `apply_filter` from `common/src/db/query.rs` to parse the comma-separated value
   and generate a SQL `IN` clause. Join through the `package_license` entity to filter
   packages by their declared license.

   ```rust
   use common::db::query::apply_filter;
   use entity::package_license;

   pub async fn list(
       &self,
       /* existing params */
       license: Option<&str>,
   ) -> Result<PaginatedResults<PackageSummary>, anyhow::Error> {
       let mut query = /* existing query setup */;

       // Apply license filter if provided
       if let Some(license_value) = license {
           query = apply_filter(
               query,
               package_license::Column::License,
               license_value,
           )?;
       }

       // ... rest of existing query execution
   }
   ```

3. **Join the package_license table**: If the license filter is active, add a JOIN
   to `package_license` entity so the filter column is available. Follow the SeaORM
   join pattern used elsewhere in the codebase.

   ```rust
   if license.is_some() {
       query = query.join(
           JoinType::InnerJoin,
           package::Relation::PackageLicense.def(),
       );
   }
   ```

4. **Validate license values**: If parsing the license value(s) fails or they are
   empty strings, return an `AppError` with `StatusCode::BAD_REQUEST`. Follow the
   same validation pattern as the advisory severity filter.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create a new integration test file with the following test functions:

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_single_license_filter() {
    // Given a database seeded with packages having MIT and Apache-2.0 licenses
    // When requesting GET /api/v2/package?license=MIT
    // Then only MIT-licensed packages are returned
    // Assert on specific package names/IDs, not just count
}

/// Verifies that filtering by multiple comma-separated licenses returns packages matching any.
#[tokio::test]
async fn test_list_packages_multi_license_filter() {
    // Given a database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    // When requesting GET /api/v2/package?license=MIT,Apache-2.0
    // Then packages with either MIT or Apache-2.0 are returned, but not GPL-3.0
    // Assert on specific package names/IDs
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given a database seeded with packages having various licenses
    // When requesting GET /api/v2/package (no license param)
    // Then all packages are returned
    // Assert total_count matches expected seed count
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // Given a running server
    // When requesting GET /api/v2/package?license= (empty string or invalid)
    // Then response status is 400 Bad Request
}
```

Each test will:
- Use the real PostgreSQL test database pattern from sibling tests
- Seed fixture data with known packages and licenses
- Use `assert_eq!(resp.status(), StatusCode::OK)` (or `BAD_REQUEST` for error case)
- Deserialize response body into `PaginatedResults<PackageSummary>`
- Assert on specific field values (`license` field, package names) not just counts
- Include `///` doc comments on every test function
- Include `// Given`, `// When`, `// Then` section comments

### Module Registration

The new test file `tests/api/package_license_filter.rs` needs to be registered in
`tests/Cargo.toml` (if tests are organized as separate binaries) or referenced via
`mod package_license_filter;` in the test module root, following the same pattern as
`tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Documentation Impact

- **`docs/api.md`**: Update the `GET /api/v2/package` section to document the new
  optional `license` query parameter, including the comma-separated multi-value format.
- **No other documentation changes needed** — the response shape is unchanged, no
  configuration changes, no architectural changes.

## Step 7 — Run Tests

```
cargo test --test package_license_filter
cargo test  # full suite to check for regressions
```

## Step 8 — Verify Acceptance Criteria

| Criterion | Verification Method |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | `test_list_packages_single_license_filter` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns either | `test_list_packages_multi_license_filter` |
| No `license` param returns all packages | `test_list_packages_no_license_filter` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | All tests deserialize into this type |
| Invalid license returns 400 | `test_list_packages_invalid_license_returns_400` |

## Step 9 — Self-Verification Checklist

1. **Scope containment**: `git diff --name-only` should show only the 2 modified files,
   1 created test file, and possibly `docs/api.md`. Any other files are out-of-scope.
2. **Untracked file check**: verify `tests/api/package_license_filter.rs` is staged.
3. **Sensitive-pattern check**: scan staged diff for secrets/credentials.
4. **Documentation currency**: verify `docs/api.md` reflects the new `license` parameter.
5. **Duplication check**: confirm no existing license filter logic exists elsewhere.
6. **CI checks**: run `cargo fmt --check`, `cargo clippy`, `cargo build`, `cargo test`.
7. **Data-flow trace**: 
   - `GET /api/v2/package?license=MIT` -> extract query param in handler -> pass to
     PackageService::list() -> apply_filter builds SQL IN clause -> JOIN package_license
     table -> return filtered PaginatedResults -> JSON response — **COMPLETE**
8. **Contract & sibling parity**: verify handler returns same `Result<Json<PaginatedResults<PackageSummary>>, AppError>` as sibling endpoints; verify `apply_filter` is called the same way as in advisory severity filter.

## Step 10 — Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs \
       docs/api.md
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX license filtering.
Reuses apply_filter from common query helpers and joins through the
existing package_license entity.

Implements TC-9203"
```

```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary
- Add optional \`license\` query parameter to \`GET /api/v2/package\`
- Support single-value (\`?license=MIT\`) and comma-separated multi-value (\`?license=MIT,Apache-2.0\`) filtering
- Reuse \`apply_filter\` from \`common/src/db/query.rs\` and JOIN through \`package_license\` entity
- Add integration tests for single, multi, no-filter, and invalid-input cases

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)"
```

## Step 11 — Update Jira

1. Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format.
2. Add comment summarizing: PR link, changes made (license filter on package list
   endpoint, reusing apply_filter and package_license entity), no deviations from plan.
3. Transition TC-9203 to In Review.

## Files Summary

| File | Action | Description |
|---|---|---|
| `modules/fundamental/src/package/endpoints/list.rs` | MODIFY | Add `license` field to Query struct; pass to service |
| `modules/fundamental/src/package/service/mod.rs` | MODIFY | Add `license` param to `list()`; apply filter with JOIN |
| `tests/api/package_license_filter.rs` | CREATE | 4 integration tests covering all acceptance criteria |
| `docs/api.md` | MODIFY | Document new `license` query parameter |
