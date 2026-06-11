# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint in trustify-backend.
This allows consumers to filter packages by their declared SPDX license identifier, supporting
both single-value and comma-separated multi-value filtering.

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, custom fields
3. **Code Intelligence** -- present with tool naming convention `mcp__serena_backend__<tool>` and rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed task sections:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add `license` query parameter to `GET /api/v2/package` for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering.
- **Files to Modify**:
  - `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
  - `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method
- **Files to Create**:
  - `tests/api/package_license_filter.rs` -- integration tests for the license filter
- **API Changes**:
  - `GET /api/v2/package?license=MIT` -- add optional `license` query parameter
  - `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated values
- **Implementation Notes**: Follow advisory severity filter pattern, use `apply_filter` from `common/src/db/query.rs`, join through `package_license` entity
- **Acceptance Criteria**: 5 criteria (see task description)
- **Test Requirements**: 4 test cases
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **Linked Issues**: is incorporated by TC-9001

No missing sections. Proceed with default flow.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9203, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9203)` to In Progress

## Step 4 -- Understand the Code

### Serena instance

Use `mcp__serena_backend__<tool>` for all code intelligence operations.

### Files to inspect

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to understand the current structure
   - Use `mcp__serena_backend__find_symbol` on the handler function and the query struct to read their bodies
   - Identify the existing Query struct (or equivalent parameter extraction struct)
   - Understand how existing query parameters (pagination, sorting) are extracted

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to see PackageService methods
   - Use `mcp__serena_backend__find_symbol` on the `list` method to read its implementation
   - Understand how it currently builds the database query

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate -- sibling for convention analysis)
   - Use `mcp__serena_backend__get_symbols_overview` to see the advisory list handler structure
   - Use `mcp__serena_backend__find_symbol` on the severity filter-related code
   - This is the reference implementation for the filter pattern we need to follow

4. **`common/src/db/query.rs`** (reuse candidate)
   - Use `mcp__serena_backend__find_symbol` on `apply_filter` to understand its signature and behavior
   - Confirm it handles comma-separated multi-value parsing and SQL IN clause generation

5. **`entity/src/package_license.rs`** (reuse candidate)
   - Use `mcp__serena_backend__get_symbols_overview` to understand the entity structure
   - Identify the column names and relations for building the JOIN query

6. **`modules/fundamental/src/package/model/summary.rs`** (context -- verify response shape)
   - Use `mcp__serena_backend__get_symbols_overview` to confirm PackageSummary includes a license field
   - Verify the response shape will not change

7. **`modules/fundamental/src/package/endpoints/mod.rs`** (context -- route registration)
   - Understand how routes are registered, in case the list endpoint needs route changes

### Sibling files for convention conformance analysis

- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler (primary reference)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- another sibling endpoint handler
- `modules/fundamental/src/advisory/service/advisory.rs` -- sibling service for pattern comparison

### Test sibling files for test convention analysis

- `tests/api/advisory.rs` -- advisory endpoint integration tests (primary test reference)
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

### Documentation files to check

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (check for CI commands and conventions)
- `docs/api.md` -- API documentation that may need updating for the new query parameter

### CONVENTIONS.md lookup

Would check `./CONVENTIONS.md` in the trustify-backend repository root. If present, read it for:
- Naming rules, directory structure, code patterns, test conventions
- CI check commands (extract for Step 9)
- Code generation commands

### Expected discovered conventions (from sibling analysis)

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Query parameter extraction**: List endpoints use a Query struct (e.g., `PackageQuery` or similar) with `#[derive(Deserialize)]` for Axum query extraction
- **Filter pattern**: Optional filter fields in the Query struct, passed to service layer, applied via `apply_filter` from `common/src/db/query.rs`
- **Response type**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Service pattern**: Service methods accept filter parameters and build SeaORM queries with conditional joins/filters
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `list_packages`, `fetch_package`)

### Expected discovered test conventions

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List endpoint tests validate `total_count`, `items.len()`, and key fields
- **Error cases**: Tests include status code checks for error responses (e.g., `StatusCode::BAD_REQUEST`)
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_filter_by_license`)
- **Setup**: Tests use a real PostgreSQL test database with fixture data

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**Changes:**

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing query parameter struct (following the same pattern as the advisory endpoint's `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).

   ```rust
   /// Optional license filter. Accepts a single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Pass the license parameter to the service layer**: In the handler function, extract `query.license` and pass it to the `PackageService::list` method (or equivalent) as an additional parameter.

3. **Add input validation**: Before passing the license parameter to the service, validate the SPDX identifier format. If the value is invalid (e.g., empty string after splitting, or contains characters not valid in SPDX identifiers), return a 400 Bad Request response with a descriptive error message. Follow the existing error handling pattern using `AppError`.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add `license` parameter to the list method**: Modify the `list` method signature on `PackageService` to accept an optional license filter parameter (`Option<String>`).

2. **Build the filter query using `apply_filter`**: When the `license` parameter is `Some`, use the `apply_filter` function from `common/src/db/query.rs` to:
   - Parse the comma-separated string into individual license values
   - Generate a SQL `IN` clause for matching
   - Join through the `package_license` entity (from `entity/src/package_license.rs`) to connect packages to their declared licenses
   - Add the filter condition to the existing query builder

3. **Preserve existing query behavior**: When `license` is `None`, the query should behave exactly as before -- no join, no filter, all packages returned. This ensures backward compatibility.

   The implementation pattern follows the advisory severity filter:
   ```rust
   // Pseudocode following advisory severity filter pattern
   if let Some(license) = &license {
       // Use apply_filter to handle comma-separated values and generate IN clause
       // JOIN package_license table on package.id = package_license.package_id
       // WHERE package_license.license IN (parsed values)
       let filter = apply_filter(license);
       query = query.join(/* package_license entity */).filter(filter);
   }
   ```

4. **Use `find_referencing_symbols`** on the list method before modifying its signature to identify all callers and ensure none are broken by the added parameter.

### File 3: `tests/api/package_license_filter.rs` (NEW)

See Step 7 below for detailed test implementation.

### Documentation impact

- If `docs/api.md` exists and documents the `GET /api/v2/package` endpoint, add the new `license` query parameter to the documentation.
- The response shape (`PaginatedResults<PackageSummary>`) is unchanged, so response documentation does not need updating.

### Reuse approach

All new logic is built on top of existing infrastructure:

- **`apply_filter` from `common/src/db/query.rs`**: Reuse directly -- this function already handles comma-separated multi-value parsing and SQL IN clause generation. No modification needed.
- **Advisory severity filter pattern from `modules/fundamental/src/advisory/endpoints/list.rs`**: Follow the exact same structural pattern -- optional field in Query struct, pass to service, conditionally apply filter. No code copied; the pattern is replicated for the license domain.
- **`package_license` entity from `entity/src/package_license.rs`**: Use the existing SeaORM entity for the JOIN query. No modification needed.

No new utility functions or helpers are needed. The entire implementation composes existing pieces.

## Step 7 -- Write Tests

### File: `tests/api/package_license_filter.rs` (NEW)

Create integration tests following the patterns observed in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

**Test structure:**

```rust
/// Integration tests for the package license filter on GET /api/v2/package.

/// Verifies that filtering by a single license returns only packages with that license.
#[tokio::test]
async fn test_list_packages_filter_single_license() {
    // Given a database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
    // (set up test fixtures with known license values)

    // When requesting GET /api/v2/package?license=MIT

    // Then only packages with MIT license are returned
    // Assert response status is 200 OK
    // Assert all returned items have license == "MIT"
    // Assert on specific expected package names/identifiers, not just count
}

/// Verifies that filtering by comma-separated licenses returns packages matching any listed license.
#[tokio::test]
async fn test_list_packages_filter_multiple_licenses() {
    // Given a database with packages having MIT, Apache-2.0, and GPL-3.0 licenses

    // When requesting GET /api/v2/package?license=MIT,Apache-2.0

    // Then packages with either MIT or Apache-2.0 license are returned
    // Assert response status is 200 OK
    // Assert returned items have license in ["MIT", "Apache-2.0"]
    // Assert GPL-3.0 packages are not included
    // Assert on specific expected values, not just count
}

/// Verifies that omitting the license parameter returns all packages unchanged.
#[tokio::test]
async fn test_list_packages_no_license_filter() {
    // Given a database with packages having various licenses

    // When requesting GET /api/v2/package (no license parameter)

    // Then all packages are returned regardless of license
    // Assert response status is 200 OK
    // Assert total_count matches expected total
    // Assert specific known packages are present in the results
}

/// Verifies that an invalid license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_filter() {
    // Given a database with packages

    // When requesting GET /api/v2/package?license=<invalid-value>

    // Then a 400 Bad Request response is returned
    // Assert response status is 400 BAD_REQUEST
}
```

**Test conventions applied:**
- Each test function has a `///` documentation comment explaining what it verifies
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- Follow `test_<endpoint>_<scenario>` naming pattern
- Use `assert_eq!(resp.status(), StatusCode::OK)` (or BAD_REQUEST) for status checks
- Validate response body by deserializing and checking specific field values, not just counts
- Use real PostgreSQL test database (per project convention)

**Register the test module:** Add `mod package_license_filter;` to the appropriate test module file (likely `tests/api/mod.rs` or the test crate root) so the new test file is compiled and run.

After writing tests, run:
```
cargo test --test package_license_filter
```
Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| # | Criterion | How verified |
|---|-----------|-------------|
| 1 | GET /api/v2/package?license=MIT returns only MIT packages | `test_list_packages_filter_single_license` test |
| 2 | GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | `test_list_packages_filter_multiple_licenses` test |
| 3 | GET /api/v2/package without license returns all packages | `test_list_packages_no_license_filter` test |
| 4 | Response shape (PaginatedResults<PackageSummary>) unchanged | No structural changes to PackageSummary or PaginatedResults; tests deserialize response using existing types |
| 5 | Invalid license values return 400 Bad Request | `test_list_packages_invalid_license_filter` test |

## Step 9 -- Self-Verification

### Scope containment

Run `git diff --name-only` and verify all modified/created files are within scope:
- `modules/fundamental/src/package/endpoints/list.rs` -- in Files to Modify
- `modules/fundamental/src/package/service/mod.rs` -- in Files to Modify
- `tests/api/package_license_filter.rs` -- in Files to Create

Potential out-of-scope files that may need modification:
- `tests/api/mod.rs` or test crate root -- may need `mod package_license_filter;` declaration (would flag for user approval)
- `docs/api.md` -- if API documentation exists and needs updating (would flag for user approval)

### Untracked file check

Check `git status --short` for `??` entries. The new test file `tests/api/package_license_filter.rs` would appear as untracked and needs to be staged.

### Sensitive-pattern check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no secrets expected in this change.

### Data-flow trace

- `GET /api/v2/package?license=MIT` -> extract `license` from query params (input) -> pass to `PackageService::list` (processing) -> `apply_filter` builds SQL IN clause (processing) -> JOIN `package_license` table and filter (processing) -> return `PaginatedResults<PackageSummary>` (output) -- **COMPLETE**

### Contract & sibling parity

- The `list` handler continues to return `Result<T, AppError>` -- contract preserved
- The handler follows the same Query struct + service call pattern as advisory list -- sibling parity maintained
- `apply_filter` is called the same way as in advisory severity filter -- caller-site parity maintained

### Duplication check

No new utility functions created. All filtering logic reuses existing `apply_filter`. No duplication expected.

### CI checks

Run any CI commands extracted from `CONVENTIONS.md` (if present). At minimum:
- `cargo build` -- verify compilation
- `cargo test` -- verify all tests pass
- `cargo clippy` -- verify no new lint warnings
- `cargo fmt --check` -- verify formatting

## Step 10 -- Commit and Push

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
```

Then push and create PR:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

PR description would include:
- Summary of changes
- Implements [TC-9203](https://redhat.atlassian.net/browse/TC-9203) link
- Test plan referencing the 4 integration tests

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment summarizing: PR link, changes made (new license query parameter, reuse of apply_filter, integration tests), no deviations from plan
3. Transition TC-9203 to In Review
