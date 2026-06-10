# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing
consumers to filter packages by their declared SPDX license identifier. Support both
single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`)
filtering.

## Repository

trustify-backend

## Target Branch

main

## Branch

`TC-9203` (created from `main`)

## Step-by-Step Plan

### Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry with `trustify-backend` mapped to Serena instance `serena_backend`
- Jira Configuration with project key TC, Cloud ID, and custom field IDs
- Code Intelligence section with tool naming convention `mcp__serena_backend__<tool>`

Configuration is valid. Proceed.

### Step 1 -- Parse Task Description

All required sections are present:
- Repository: trustify-backend
- Target Branch: main
- Description, Files to Modify, Files to Create, API Changes, Implementation Notes,
  Acceptance Criteria, Test Requirements
- Dependencies: None
- No Target PR (standard flow -- create new branch and PR)
- No Bookend Type (standard implementation task)

### Step 4 -- Understand the Code

#### Files to inspect using Serena (`mcp__serena_backend__<tool>`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - Use `get_symbols_overview` to understand the current query struct and handler function
   - Use `find_symbol` with `include_body=true` on the handler function to see the current
     filtering logic

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - Use `get_symbols_overview` to see the PackageService struct and its methods
   - Use `find_symbol` on the `list` method to understand its current signature and query logic

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- sibling pattern)
   - Use `get_symbols_overview` to see the advisory Query struct with the `severity` field
   - Use `find_symbol` on the Query struct and handler to understand the filter pattern

4. **`common/src/db/query.rs`** (reuse candidate -- shared utility)
   - Use `get_symbols_overview` to locate the `apply_filter` function
   - Use `find_symbol` with `include_body=true` on `apply_filter` to understand its signature,
     how it handles comma-separated values, and how it generates SQL IN clauses

5. **`entity/src/package_license.rs`** (reuse candidate -- entity for JOIN)
   - Use `get_symbols_overview` to understand the entity's fields and relations
   - Identify the foreign key columns linking packages to licenses

6. **`modules/fundamental/src/advisory/service/advisory.rs`** (sibling service -- convention analysis)
   - Use `get_symbols_overview` to see how the advisory service passes filters from the endpoint
     layer to the query layer

#### Sibling convention analysis targets

- **Endpoint siblings**: `modules/fundamental/src/sbom/endpoints/list.rs`,
  `modules/fundamental/src/advisory/endpoints/list.rs` -- to confirm Query struct pattern,
  error handling, and return type conventions
- **Service siblings**: `modules/fundamental/src/sbom/service/sbom.rs`,
  `modules/fundamental/src/advisory/service/advisory.rs` -- to confirm service method patterns

#### Test sibling analysis targets

- `tests/api/advisory.rs` -- to see endpoint test patterns (setup, assertions, status codes)
- `tests/api/sbom.rs` -- to confirm test naming and parameterization conventions

#### Documentation files to check

- `CONVENTIONS.md` at repository root -- for CI check commands and naming rules
- `docs/api.md` -- for API documentation that may need updating

#### CONVENTIONS.md

Look up `CONVENTIONS.md` at the repository root. If present, extract CI check commands
(formatting, linting, compilation) for use in Step 9 verification.

### Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

Standard flow: new branch from main.

### Step 6 -- Implement Changes

#### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license`
   to the existing Query struct used for query parameter extraction. Follow the exact same
   pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.

2. **Pass the license filter to the service layer**: In the handler function, extract
   `query.license` and pass it to `PackageService::list()`. This mirrors how the advisory
   endpoint passes its severity filter.

3. **Input validation**: If the `license` parameter is present but contains empty strings
   after splitting on commas, return a 400 Bad Request using `AppError`. Follow the error
   handling convention (`Result<T, AppError>` with `.context()`).

**Reuse applied:**
- Reuse the Query struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs`
  (add an optional field, extract it, pass to service)
- Do NOT duplicate any comma-splitting or filter-building logic here -- that belongs in
  the service/query layer via `apply_filter`

#### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add `license` parameter to the `list` method signature**: Add an `Option<String>`
   parameter for the license filter. Follow the same pattern used by the advisory service's
   list method for its severity filter parameter.

2. **Build the filter query using `apply_filter`**: When the `license` parameter is present,
   call `common::db::query::apply_filter` to parse the comma-separated string and generate
   the SQL IN clause. This function already handles both single-value and multi-value cases.

3. **JOIN through `package_license` entity**: Use the `entity::package_license` SeaORM entity
   to join the `package` table to the `package_license` table, then filter on the license
   column. Use SeaORM's `JoinType::InnerJoin` with the relation defined in the entity, rather
   than writing raw SQL.

4. **Preserve return type**: The method must continue returning `PaginatedResults<PackageSummary>`
   -- the response shape does not change.

**Reuse applied:**
- Call `apply_filter` from `common/src/db/query.rs` for comma-separated parsing and SQL IN
  clause generation -- do NOT reimplement this logic
- Use the `package_license` entity from `entity/src/package_license.rs` for the JOIN --
  do NOT write raw SQL joins
- Follow the advisory service's pattern for integrating a filter parameter into the list query

#### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create integration tests matching the conventions found in sibling test files
(`tests/api/advisory.rs`, `tests/api/sbom.rs`). Each test function gets a doc comment
explaining what it verifies. Non-trivial tests include given-when-then section comments.

Tests to implement:

1. **`test_list_packages_filter_single_license`**
   - Doc: "Verifies that filtering by a single license returns only packages with that license."
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: assert status 200, assert all returned packages have license "MIT", assert
     specific package names/identifiers (value-based, not just count)

2. **`test_list_packages_filter_multi_license`**
   - Doc: "Verifies that comma-separated license filter returns packages matching any listed license."
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert status 200, assert returned packages have either MIT or Apache-2.0 license,
     assert specific package identifiers, assert GPL-3.0 packages are excluded

3. **`test_list_packages_no_license_filter`**
   - Doc: "Verifies that omitting the license parameter returns all packages (no regression)."
   - Given: seed database with packages having various licenses
   - When: `GET /api/v2/package`
   - Then: assert status 200, assert all seeded packages are returned (value-based checks on
     specific items)

4. **`test_list_packages_invalid_license`**
   - Doc: "Verifies that an invalid license value returns 400 Bad Request."
   - When: `GET /api/v2/package?license=` (empty value) or invalid format
   - Then: assert status 400

**Conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Validate `total_count`, `items.len()`, and key fields of returned items
- Include error case with status code assertion
- Follow `test_<endpoint>_<scenario>` naming pattern
- Register the test file in `tests/Cargo.toml` if needed

#### Module registration

Ensure `tests/api/package_license_filter.rs` is registered as a test module:
- Check `tests/Cargo.toml` for any test registration needed
- Add `mod package_license_filter;` if the test directory uses a `mod.rs` pattern

#### Documentation impact

If `docs/api.md` documents the `GET /api/v2/package` endpoint, update it to include the
new `license` query parameter with usage examples.

### Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | Covered by `test_list_packages_filter_multi_license` |
| `GET /api/v2/package` without license returns all packages | Covered by `test_list_packages_no_license_filter` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | Service return type unchanged; existing test assertions confirm shape |
| Invalid license values return 400 | Covered by `test_list_packages_invalid_license` |

### Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` should show only:
   - `modules/fundamental/src/package/endpoints/list.rs`
   - `modules/fundamental/src/package/service/mod.rs`
   - `tests/api/package_license_filter.rs` (new file)
   - Possibly `docs/api.md` if API docs were updated

2. **Untracked file check**: `tests/api/package_license_filter.rs` is expected as a new
   file listed in Files to Create.

3. **Sensitive-pattern check**: grep staged diff for secrets/credentials.

4. **Duplication check**: Verify no duplication of `apply_filter` logic. Confirm the
   comma-splitting and IN-clause generation is delegated to the shared utility, not
   reimplemented in the endpoint or service.

5. **Data-flow trace**:
   - `GET /api/v2/package?license=MIT` -> extract query param in endpoint handler ->
     pass to `PackageService::list()` -> `apply_filter` builds SQL IN clause ->
     JOIN through `package_license` entity -> filter results -> return
     `PaginatedResults<PackageSummary>` -- **COMPLETE**

6. **Contract & sibling parity**: The modified list endpoint continues to return
   `Result<PaginatedResults<PackageSummary>, AppError>`, matching the contract. The
   new filter follows the same pattern as advisory's severity filter (sibling parity).

7. **CI checks**: Run commands from `CONVENTIONS.md` (if found). At minimum:
   `cargo check`, `cargo fmt --check`, `cargo clippy`, `cargo test`.

### Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
      modules/fundamental/src/package/service/mod.rs \
      tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package supporting
single-value and comma-separated multi-value filtering by SPDX identifier.
Reuses apply_filter from common/src/db/query.rs and joins through the
existing package_license entity.

Implements TC-9203"
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" \
  --body "## Summary

- Add optional \`license\` query parameter to \`GET /api/v2/package\`
- Support single-value and comma-separated multi-value SPDX license filtering
- Reuse \`apply_filter\` from \`common/src/db/query.rs\` for query parsing
- Join through existing \`package_license\` entity for filtering
- Add integration tests for single, multi, no-filter, and invalid cases

Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203)"
```

### Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
- Add comment with PR link, summary of changes, and confirmation of no deviations
- Transition TC-9203 to In Review

## Summary of Files

| File | Action | Description |
|---|---|---|
| `modules/fundamental/src/package/endpoints/list.rs` | MODIFY | Add `license` field to Query struct, pass to service |
| `modules/fundamental/src/package/service/mod.rs` | MODIFY | Add license filter param, call `apply_filter`, JOIN through `package_license` |
| `tests/api/package_license_filter.rs` | CREATE | Integration tests for license filter (4 test functions) |
| `docs/api.md` | MODIFY (if exists) | Document new `license` query parameter |
