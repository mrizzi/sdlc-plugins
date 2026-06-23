# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` mapped to `serena_backend` at `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID, custom fields all present
- **Code Intelligence**: Serena instance `serena_backend` with `rust-analyzer`, tool naming convention documented

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9203:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier.
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs`
  - `modules/fundamental/src/package/service/mod.rs`
- **Files to Create**:
  - `tests/api/package_license_filter.rs`
- **API Changes**:
  - `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
  - `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values
- **Implementation Notes**: Follow advisory severity filter pattern, use `apply_filter` from `common/src/db/query.rs`, join through `entity/src/package_license.rs`
- **Reuse Candidates**: 3 candidates identified (see reuse-analysis.md)
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 test cases
- **Target PR**: None (default flow)
- **Bookend Type**: None (standard implementation)
- **Dependencies**: None
- **GitHub Issue custom field**: `customfield_10747` -- would check for value on fetched issue

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9203)`, search for `[sdlc-workflow] Description digest:` marker, and verify the SHA-256 digest against the current description using `python3 scripts/sha256-digest.py`.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9203, assignee=<account-id>)` to assign the task
3. `jira.transition_issue(TC-9203)` to "In Progress"

## Step 4 -- Understand the Code

### Files to inspect using Serena (`mcp__serena_backend__<tool>`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - `get_symbols_overview` to see the current handler structure, Query struct, and route registration
   - `find_symbol` on the list handler function and the Query struct with `include_body=true`

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - `get_symbols_overview` to see PackageService methods
   - `find_symbol` on the `list` method with `include_body=true` to understand current query construction

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- sibling pattern)
   - `get_symbols_overview` to see the severity filter implementation
   - `find_symbol` on the Query struct and list handler to understand the filter pattern

4. **`common/src/db/query.rs`** (reuse candidate -- shared utility)
   - `find_symbol` on `apply_filter` with `include_body=true` to understand the API and how to call it

5. **`entity/src/package_license.rs`** (reuse candidate -- entity for JOIN)
   - `get_symbols_overview` to see the SeaORM entity definition, columns, and relations

6. **`modules/fundamental/src/package/model/summary.rs`** (verify response shape)
   - `get_symbols_overview` to confirm PackageSummary includes a `license` field

7. **`common/src/model/paginated.rs`** (verify PaginatedResults wrapper)
   - `get_symbols_overview` to confirm response wrapper structure

8. **Backward compatibility check**:
   - `find_referencing_symbols` on the PackageService `list` method to identify all callers
   - `find_referencing_symbols` on the Query struct in list.rs to find all consumers

### Sibling file analysis (convention conformance)

- **Endpoint siblings**: `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/list.rs` -- examine Query struct pattern, error handling, response wrapping
- **Service siblings**: `modules/fundamental/src/advisory/service/advisory.rs`, `modules/fundamental/src/sbom/service/sbom.rs` -- examine how filters are plumbed through service methods

### Test convention analysis

- **Test siblings**: `tests/api/advisory.rs`, `tests/api/sbom.rs` -- examine assertion patterns, setup/teardown, naming conventions

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root using `mcp__serena_backend__list_dir` or Glob. If found, read and extract CI check commands and code generation commands.

### Documentation file identification

- `README.md` at repository root
- `docs/api.md` -- API reference documentation
- `docs/architecture.md` -- system architecture overview
- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration (may contain inline docs)

### Discovered conventions (expected from sibling analysis)

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query struct pattern**: Each list endpoint defines a `Query` struct with optional filter fields, extracted via Axum's `Query` extractor
- **Filter application**: Filters use `apply_filter` from `common/src/db/query.rs` which handles comma-separated parsing and SQL IN clause generation
- **Module structure**: `model/ + service/ + endpoints/` pattern per domain module
- **Testing**: Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**What exists**: A list handler for `GET /api/v2/package` with a `Query` struct for query parameter extraction and a handler function that calls `PackageService::list`.

**Changes**:

1. **Add `license` field to the `Query` struct**:
   - Add `pub license: Option<String>` to the existing Query struct
   - Follow the exact same pattern used for the `severity` field in the advisory list endpoint's Query struct

2. **Pass license filter to service layer**:
   - In the list handler function, extract `query.license` and pass it to `PackageService::list` as an additional parameter
   - The handler function signature and return type remain unchanged (`Result<Json<PaginatedResults<PackageSummary>>, AppError>`)

3. **Add input validation**:
   - Validate that if `license` is provided, its values are non-empty strings
   - Return 400 Bad Request for invalid values (empty strings, whitespace-only)
   - Follow the same validation pattern used in the advisory endpoint

**Reuse**: Follow the advisory `list.rs` Query struct pattern exactly. The Query struct field definition, extraction, and passing to the service layer should be structurally identical to how `severity` is handled there.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**What exists**: `PackageService` with a `list` method that queries the database for packages and returns `PaginatedResults<PackageSummary>`.

**Changes**:

1. **Add `license` parameter to the `list` method signature**:
   - Add `license: Option<String>` parameter
   - Follow the same parameter position pattern as advisory service's list method

2. **Add license filter logic using `apply_filter`**:
   - Import `apply_filter` from `common/src/db/query.rs`
   - Import the `package_license` entity from `entity/src/package_license.rs`
   - When `license` is `Some(value)`:
     - JOIN the `package_license` table to the package query
     - Use `apply_filter` to handle comma-separated values and generate the SQL `IN` clause against the license SPDX identifier column
   - When `license` is `None`, make no changes to the query (preserving backward compatibility)

3. **JOIN construction**:
   - Use SeaORM's `.join()` method to join `package` to `package_license` on the package ID foreign key
   - Add the filter condition on `package_license.license_id` (or equivalent SPDX column)
   - The `apply_filter` function handles splitting comma-separated values and generating the appropriate WHERE clause

**Reuse**:
- `common/src/db/query.rs::apply_filter` -- called directly with the license parameter value and the package_license column
- `entity/src/package_license.rs` -- used for the SeaORM JOIN definition rather than raw SQL

### File 3 (new): `tests/api/package_license_filter.rs`

**What to create**: Integration tests for the license filter feature.

**Tests to implement**:

1. **`test_package_list_filter_by_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status 200, all returned packages have MIT license, assert on specific package names/identifiers (value-based assertions, not just count)

2. **`test_package_list_filter_by_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status 200, returned packages have either MIT or Apache-2.0, assert specific packages are present and GPL-3.0 packages are absent

3. **`test_package_list_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status 200, all packages returned, response shape is `PaginatedResults<PackageSummary>`

4. **`test_package_list_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid (empty) license value returns 400 Bad Request.`
   - Given: Standard test database
   - When: `GET /api/v2/package?license=` (empty value)
   - Then: Response status 400 Bad Request

**Conventions to follow in tests**:
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Validate `total_count`, `items.len()`, and specific field values on items
- Include given-when-then section comments in each test body
- Follow `test_<endpoint>_<scenario>` naming convention
- Use the same test database setup/teardown pattern as `tests/api/advisory.rs` and `tests/api/sbom.rs`

### Module registration

- Add `mod package_license_filter;` to `tests/api/` module root (if one exists) or ensure Cargo.toml picks up the new test file
- No changes needed to `modules/fundamental/src/package/endpoints/mod.rs` route registration (the existing route handler is being modified, not a new route)

### Documentation impact

- If `docs/api.md` documents the `GET /api/v2/package` endpoint, add the new `license` query parameter to its documentation
- No architectural documentation changes needed (this is an additive parameter, not a new pattern)

## Step 7 -- Write Tests

Run `cargo test` after implementing tests. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_package_list_filter_by_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns either | Covered by `test_package_list_filter_by_multiple_licenses` |
| No license parameter returns all packages | Covered by `test_package_list_no_license_filter` |
| Response shape `PaginatedResults<PackageSummary>` unchanged | Verified by all tests deserializing the response |
| Invalid license values return 400 | Covered by `test_package_list_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `modules/fundamental/src/package/endpoints/list.rs` (modified)
  - `modules/fundamental/src/package/service/mod.rs` (modified)
  - `tests/api/package_license_filter.rs` (created)
- Any additional files would be flagged for user approval

### Untracked file check
- Check `git status --short` for `??` entries in modified directories
- Verify no untracked files are referenced by code

### Sensitive-pattern check
- Scan staged diff for passwords, API keys, secrets

### Data-flow trace
- Input: HTTP query parameter `license` extracted by Axum's `Query` extractor in `list.rs`
- Processing: Passed to `PackageService::list`, which uses `apply_filter` to generate SQL JOIN + IN clause
- Output: Filtered `PaginatedResults<PackageSummary>` returned as JSON response
- All stages connected -- COMPLETE

### Contract & sibling parity
- Query struct follows same pattern as advisory endpoint
- PackageService::list signature change is backward-compatible (new optional parameter)
- All callers of PackageService::list identified via `find_referencing_symbols` and updated

### Duplication check
- No new utility functions created; reusing existing `apply_filter`
- No risk of duplication

### Cross-section reference consistency
- `modules/fundamental/src/package/service/mod.rs` referenced consistently in both "Files to Modify" and "Implementation Notes"
- `common/src/db/query.rs::apply_filter` referenced consistently across "Implementation Notes" and "Reuse Candidates"

### CI checks
- Run any CI check commands from CONVENTIONS.md
- Run `cargo build`, `cargo clippy`, `cargo fmt --check` as fallback

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license query parameter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value filtering by
SPDX license identifier. Reuses the existing apply_filter utility
and follows the advisory severity filter pattern.

Implements TC-9203"

git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

PR description would include:
- Summary of changes
- `Implements [TC-9203](<webUrl>)` with clickable link
- Closes reference if GitHub Issue custom field had a value

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
2. Add comment with PR link, summary of changes, and confirmation of no deviations
3. Transition TC-9203 to "In Review"
