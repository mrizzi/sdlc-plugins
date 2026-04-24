# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Summary

Add a `license` query parameter to `GET /api/v2/package` that supports exact-match
filtering by SPDX license identifier, with both single-value and comma-separated
multi-value input.

---

## Step 0 -- Validate Project Configuration

The mock CLAUDE.md for `trustify-backend` contains all required sections:

1. **Repository Registry** -- present, maps `trustify-backend` to Serena instance `serena_backend`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present with tool naming convention `mcp__serena_backend__<tool>`

Validation passes; proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9203:

| Section | Content |
|---|---|
| Repository | trustify-backend |
| Description | Add `license` query parameter to `GET /api/v2/package` for filtering by SPDX identifier; support single and comma-separated values |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` (add optional param), `GET /api/v2/package?license=MIT,Apache-2.0` (comma-separated) |
| Implementation Notes | Follow advisory severity filter pattern; reuse `apply_filter` from `common/src/db/query.rs`; join through `package_license` entity |
| Acceptance Criteria | 5 criteria (single filter, multi filter, no-filter regression, response shape unchanged, invalid value 400) |
| Test Requirements | 4 tests (single, multi, no filter, invalid) |
| Target PR | None |
| Dependencies | None |

No missing sections. Proceed.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would call:
- `jira.user_info()` to get current user account ID
- `jira.edit_issue("TC-9203", assignee=<account-id>)` to assign
- `jira.transition_issue("TC-9203")` to "In Progress"

Skipped per eval instructions (no external service calls).

## Step 4 -- Understand the Code

### Files to inspect via Serena (`mcp__serena_backend__*`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - `get_symbols_overview` to see current handler and query struct
   - `find_symbol` on the handler function and `PackageQuery` struct to read their bodies
   - Expect: an Axum handler accepting `Query<PackageQuery>` and calling `PackageService::list()`

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - `get_symbols_overview` to see `PackageService` methods
   - `find_symbol` on `PackageService::list` to read its implementation
   - Expect: a method that builds a SeaORM query, applies existing filters, paginates, returns `PaginatedResults<PackageSummary>`

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- sibling)
   - `get_symbols_overview` to see the `AdvisoryQuery` struct and handler
   - `find_symbol` on `AdvisoryQuery` and the handler to see how `severity` filter is wired
   - This is the structural template for the license filter

4. **`common/src/db/query.rs`** (reuse candidate)
   - `find_symbol` on `apply_filter` to read its signature and implementation
   - Expect: a function that takes a comma-separated string, splits it, and generates a SeaORM `IN` clause condition

5. **`entity/src/package_license.rs`** (reuse candidate)
   - `get_symbols_overview` to see the entity struct and its columns/relations
   - Expect: a SeaORM entity with at least `package_id` and `license_id`/`license` columns

6. **`modules/fundamental/src/package/model/summary.rs`** -- verify `PackageSummary` already has a `license` field (task says it does)

7. **`common/src/model/paginated.rs`** -- confirm `PaginatedResults<T>` return type

### Sibling convention analysis

**Endpoint siblings** (from `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`):
- Handlers return `Result<Json<PaginatedResults<T>>, AppError>`
- Query parameters use a `*Query` struct deriving `Deserialize` with `#[serde(default)]` on optional fields
- Filters are applied by calling a shared `apply_filter` function or method
- Error handling uses `.context()` wrapping on service calls

**Service siblings** (from `modules/fundamental/src/advisory/service/advisory.rs`):
- Service methods accept filter parameters directly or via a filter struct
- SeaORM queries are built with `.filter()`, `.find_also_related()`, and `.paginate()`
- Results are collected into `PaginatedResults<T>`

### Test convention analysis

**Sibling test files**: `tests/api/advisory.rs`, `tests/api/sbom.rs`
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Response body is deserialized to `PaginatedResults<T>` and fields are validated
- Error tests assert `StatusCode::BAD_REQUEST` with error body checks
- Tests follow `test_<endpoint>_<scenario>` naming (e.g., `test_list_advisories_filtered`)
- Setup uses a real PostgreSQL test database with fixture insertion

### CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at the repo root. If present, extract CI check commands
(e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`). Record for Step 9.

### Documentation file identification

- `docs/api.md` -- may document the `GET /api/v2/package` endpoint
- `README.md` -- general project docs
- `CONVENTIONS.md` -- project conventions

---

## Step 5 -- Create Branch

```
git checkout -b TC-9203
```

No Target PR, so create a new branch.

---

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to `PackageQuery` struct:**

   ```rust
   /// Query parameters for the package list endpoint.
   #[derive(Debug, Deserialize)]
   pub struct PackageQuery {
       // ... existing fields (pagination, sort, etc.) ...

       /// Optional SPDX license identifier filter. Supports comma-separated values
       /// for matching packages with any of the listed licenses.
       #[serde(default)]
       pub license: Option<String>,
   }
   ```

   This mirrors the `severity: Option<String>` field in `AdvisoryQuery` from
   `modules/fundamental/src/advisory/endpoints/list.rs`.

2. **Pass `license` filter to service layer in the handler function:**

   In the handler body, extract `query.license` and pass it to
   `PackageService::list()`. Example:

   ```rust
   let result = PackageService::new(db)
       .list(query.into_filter(), paginator)
       .await
       .context("Failed to list packages")?;
   ```

   Or, if the service method accepts individual filter parameters:

   ```rust
   let result = service
       .list(query.license.as_deref(), /* other params */)
       .await
       .context("Failed to list packages")?;
   ```

   Follow whichever pattern the advisory endpoint uses.

3. **Add input validation for the `license` parameter:**

   Before calling the service, validate that each comma-separated value is a
   non-empty string (and optionally a valid SPDX identifier pattern). Return
   `AppError::BadRequest` (or equivalent 400 error) for invalid values.

   ```rust
   if let Some(ref license) = query.license {
       for l in license.split(',') {
           let l = l.trim();
           if l.is_empty() {
               return Err(AppError::bad_request("Invalid license value: empty string"));
           }
       }
   }
   ```

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add license filter parameter to `PackageService::list()` method:**

   Add an `Option<&str>` parameter (or incorporate it into a filter struct) for
   the license filter.

2. **Apply license filter using `apply_filter` and `package_license` join:**

   ```rust
   use entity::package_license;
   use common::db::query::apply_filter;

   /// Lists packages with optional filtering by license.
   pub async fn list(
       &self,
       license: Option<&str>,
       /* other params */
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
       let mut query = package::Entity::find();

       // Apply license filter if provided
       if let Some(license_value) = license {
           // Join to package_license table
           query = query.join(
               sea_orm::JoinType::InnerJoin,
               package::Relation::PackageLicense.def(),
           );
           // Use shared apply_filter to handle comma-separated values
           query = apply_filter(query, package_license::Column::License, license_value);
       }

       // ... existing pagination and execution logic ...
   }
   ```

   The `apply_filter` function from `common/src/db/query.rs` handles splitting
   comma-separated values and generating `Column::is_in(values)` conditions.

3. **Ensure DISTINCT results** when joining through `package_license`:

   A package with multiple licenses could appear multiple times. Add `.distinct()`
   to the query when the license filter is active, following the same pattern used
   in advisory filtering if applicable.

### File 3 (new): `tests/api/package_license_filter.rs`

**Create integration tests:**

```rust
/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_single_license_filter() {
    // Given a database with packages having MIT and Apache-2.0 licenses
    let ctx = TestContext::new().await;
    ctx.seed_package("pkg-a", "MIT").await;
    ctx.seed_package("pkg-b", "Apache-2.0").await;
    ctx.seed_package("pkg-c", "MIT").await;

    // When requesting packages filtered by MIT license
    let resp = ctx.get("/api/v2/package?license=MIT").await;

    // Then only MIT-licensed packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    assert!(body.items.iter().all(|p| p.license == "MIT"));
}

/// Verifies that comma-separated license filter returns packages matching any listed license.
#[tokio::test]
async fn test_list_packages_multi_license_filter() {
    // Given a database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    let ctx = TestContext::new().await;
    ctx.seed_package("pkg-a", "MIT").await;
    ctx.seed_package("pkg-b", "Apache-2.0").await;
    ctx.seed_package("pkg-c", "GPL-3.0-only").await;

    // When requesting packages filtered by MIT and Apache-2.0
    let resp = ctx.get("/api/v2/package?license=MIT,Apache-2.0").await;

    // Then packages with either license are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
    let licenses: Vec<&str> = body.items.iter().map(|p| p.license.as_str()).collect();
    assert!(licenses.contains(&"MIT"));
    assert!(licenses.contains(&"Apache-2.0"));
}

/// Verifies that omitting the license parameter returns all packages (no regression).
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given a database with packages having various licenses
    let ctx = TestContext::new().await;
    ctx.seed_package("pkg-a", "MIT").await;
    ctx.seed_package("pkg-b", "Apache-2.0").await;

    // When requesting packages without a license filter
    let resp = ctx.get("/api/v2/package").await;

    // Then all packages are returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 2);
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() {
    // Given a running server
    let ctx = TestContext::new().await;

    // When requesting packages with an empty/invalid license value
    let resp = ctx.get("/api/v2/package?license=").await;

    // Then a 400 Bad Request is returned
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

**Test file registration:** Add `mod package_license_filter;` to `tests/api/mod.rs`
(or the test harness entry point) so the new test file is compiled.

---

## Step 7 -- Write Tests

Tests are defined above in the "File 3" section. After writing them, run:

```
cargo test --test api -- package_license_filter
```

Fix any compilation or assertion failures before proceeding.

---

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|---|---|
| 1 | `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_list_packages_single_license_filter` |
| 2 | `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Covered by `test_list_packages_multi_license_filter` |
| 3 | `GET /api/v2/package` without license returns all (no regression) | Covered by `test_list_packages_no_license_filter` |
| 4 | Response shape `PaginatedResults<PackageSummary>` unchanged | No changes to `PackageSummary` or `PaginatedResults`; the `license` field already exists on `PackageSummary` |
| 5 | Invalid license values return 400 | Covered by `test_list_packages_invalid_license_returns_400` |

---

## Step 9 -- Self-Verification

### Scope containment

Expected `git diff --name-only` output:

```
modules/fundamental/src/package/endpoints/list.rs
modules/fundamental/src/package/service/mod.rs
tests/api/package_license_filter.rs
```

The first two are listed in "Files to Modify." The third is listed in "Files to Create."
All files are in scope.

A possible out-of-scope file: `tests/api/mod.rs` (if it needs a `mod` declaration for
the new test file). This is a minimal, necessary change to register the test module --
would flag to user for approval.

### Sensitive-pattern check

No passwords, API keys, or secrets expected in these changes.

### Data-flow trace

- **Input**: HTTP query parameter `license` on `GET /api/v2/package`
- **Parsing**: Axum deserializes into `PackageQuery.license` via serde
- **Validation**: Handler validates non-empty values, returns 400 on invalid input
- **Processing**: `PackageService::list()` receives filter, joins `package_license` table, applies `apply_filter` for SQL IN clause
- **Output**: Filtered `PaginatedResults<PackageSummary>` returned as JSON

Data flow is complete end-to-end.

### Contract & sibling parity

- `PackageService::list()` signature change is additive (new optional parameter)
- `find_referencing_symbols` on `PackageService::list` would identify all callers --
  they pass `None` for the new parameter, preserving backward compatibility
- Sibling parity with `AdvisoryService::list()` severity filter: same pattern used

### Duplication check

No duplication expected: the filter logic reuses `apply_filter` from `common/src/db/query.rs`
rather than reimplementing comma-separated parsing.

### CI checks

Would run commands from `CONVENTIONS.md` (e.g., `cargo fmt --check`, `cargo clippy`,
`cargo test`). Fix any issues before committing.

---

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value SPDX license filtering.
Reuses apply_filter helper and package_license entity join.

Implements TC-9203"
git push -u origin TC-9203
```

Then open PR:

```
gh pr create --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary
- Add optional \`license\` query parameter to \`GET /api/v2/package\`
- Support single and comma-separated SPDX license identifiers
- Reuse \`apply_filter\` helper and \`package_license\` entity join

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)

## Test plan
- [x] Single license filter returns matching packages only
- [x] Comma-separated filter returns packages matching any listed license
- [x] No filter returns all packages (regression check)
- [x] Invalid license value returns 400 Bad Request"
```

---

## Step 11 -- Update Jira

Would update Jira with:
- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment summarizing changes and linking PR
- Transition TC-9203 to "In Review"

Skipped per eval instructions.
