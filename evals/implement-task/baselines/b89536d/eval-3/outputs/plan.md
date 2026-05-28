# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (`claude-md-mock.md`) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, tool naming convention `mcp__serena_backend__<tool>`, rust-analyzer configured

Configuration is valid. Proceeding.

## Step 1 -- Parse Jira Task (TC-9203)

### Parsed Fields

| Field | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add `license` query parameter to `GET /api/v2/package` supporting single and comma-separated multi-value filtering by SPDX license identifier |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` (add optional `license` param), `GET /api/v2/package?license=MIT,Apache-2.0` (comma-separated multi-value) |
| Target PR | None |
| Bookend Type | None |
| Dependencies | None |
| Linked Issues | is incorporated by TC-9001 |

### GitHub Issue Extraction

The GitHub Issue custom field (`customfield_10747`) would be read from the Jira API response. If populated, the GitHub issue reference would be extracted and stored for inclusion in the PR description's `Closes` line.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9203", assignee=<account-id>)` to assign the task
3. `jira.transition_issue("TC-9203")` to In Progress

## Step 4 -- Understand the Code

### 4.1 Inspect files to modify

**`modules/fundamental/src/package/endpoints/list.rs`** -- the existing package list endpoint handler. Would use `mcp__serena_backend__get_symbols_overview` to understand the current request struct (query parameters) and handler function. Key things to identify:
- The existing `PackageListQuery` struct (or equivalent) that defines accepted query parameters
- How query parameters are deserialized (likely via Axum's `Query<T>` extractor)
- How the handler calls `PackageService::list()`

**`modules/fundamental/src/package/service/mod.rs`** -- the `PackageService` with its `list` method. Would use `mcp__serena_backend__find_symbol` on `PackageService` and specifically `list` with `include_body=true` to understand:
- The method signature and parameters
- How filters are currently applied to the database query
- How results are returned as `PaginatedResults<PackageSummary>`

### 4.2 Inspect the advisory severity filter (structural template)

**`modules/fundamental/src/advisory/endpoints/list.rs`** -- this is the structural template cited in Implementation Notes. Would use `mcp__serena_backend__get_symbols_overview` to see its Query struct with the `severity` field, and `mcp__serena_backend__find_symbol` with `include_body=true` on the handler to see how `severity` is extracted, parsed, and passed to the service layer. This is the pattern we replicate for `license`.

**`modules/fundamental/src/advisory/service/advisory.rs`** (or `service/mod.rs`) -- would inspect how the advisory service receives the severity filter and builds the database query.

### 4.3 Inspect the query helper

**`common/src/db/query.rs`** -- would use `mcp__serena_backend__find_symbol` on `apply_filter` with `include_body=true` to understand:
- Its function signature (what parameters it accepts)
- How it parses comma-separated values
- How it generates SQL `IN` clauses
- Any validation or error handling it performs

### 4.4 Inspect the entity

**`entity/src/package_license.rs`** -- would use `mcp__serena_backend__get_symbols_overview` to see the SeaORM entity definition (columns, relations). Key fields to identify:
- The `package_id` column (for joining to the `package` table)
- The `license` column (for filtering by SPDX identifier)
- Any SeaORM `Relation` definitions to the `package` entity

### 4.5 Inspect the package model

**`modules/fundamental/src/package/model/summary.rs`** -- would verify that `PackageSummary` already has a `license` field (confirmed by repo structure notes), ensuring the response shape does not need modification.

### 4.6 Backward compatibility check

Would use `mcp__serena_backend__find_referencing_symbols` on:
- The `PackageService::list` method -- to identify all callers and ensure adding an optional parameter does not break them
- The package list handler's query struct -- to confirm no external references depend on the current field set

### 4.7 Convention conformance analysis (sibling files)

**Sibling endpoint files inspected:**
- `modules/fundamental/src/sbom/endpoints/list.rs` -- SBOM list endpoint
- `modules/fundamental/src/advisory/endpoints/list.rs` -- advisory list endpoint (also the structural template)

**Discovered conventions (from sibling analysis):**
- **Query struct pattern:** Each list endpoint defines a query parameter struct (e.g., `AdvisoryListQuery`) with optional filter fields, deserialized by Axum's `Query<T>` extractor
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Service call pattern:** Handlers call `<Entity>Service::list(db, &query)` passing the query struct or individual filter values
- **Response type:** All list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Filter plumbing:** Optional filter parameters are passed through to the service, which uses `apply_filter` from `common/src/db/query.rs` to build the SQL WHERE clause
- **Naming:** Service methods use `verb_noun` pattern (e.g., `list_packages`, `fetch_advisory`)

### 4.8 Test convention analysis

**Sibling test files inspected:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

**Discovered test conventions (from sibling test analysis):**
- **Assertion style:** Tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into typed structs
- **Response validation:** List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- **Error cases:** Tests include status code assertions for error responses (e.g., 400, 404)
- **Test naming:** Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered_by_severity`)
- **Test setup:** Tests seed a test database with known fixture data, then query against it
- **Parameterized tests:** Would check if sibling tests use `#[rstest]` -- if not, do not introduce parameterized tests

### 4.9 CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root. If present, read it and extract:
- CI check commands (formatting, linting, clippy, compilation)
- Code generation commands (if any)
- Any additional naming or structural conventions

### 4.10 Documentation file identification

Would identify:
- `README.md` at repo root
- `docs/api.md` -- REST API reference (may need updating to document the new `license` query parameter)
- `docs/architecture.md` -- unlikely to need changes for a filter addition

## Step 5 -- Create Branch

Would execute:
```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the query parameter struct.** Following the pattern from advisory's `list.rs`, add an optional `license` field of type `Option<String>` to the existing query struct (e.g., `PackageListQuery`). This mirrors how `severity` is defined in the advisory list query struct.

2. **Pass the `license` parameter to `PackageService::list()`.** In the handler function, extract `query.license` and pass it to the service method. Follow the same pattern used in the advisory handler: the optional string is forwarded as-is to the service layer, which handles parsing and filtering.

**Reuse:** The query struct pattern is directly copied from the advisory endpoint's approach. No new deserialization logic is needed -- Axum's `Query<T>` extractor handles it automatically.

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Add `license` filter parameter to the `list` method signature.** Add an `Option<String>` parameter (or extend an existing query/filter struct parameter) for the license filter. Follow the pattern from the advisory service's list method.

2. **Apply the license filter using `apply_filter` from `common/src/db/query.rs`.** This is the core reuse point. The `apply_filter` function already handles:
   - Parsing comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
   - Generating a SQL `IN` clause for multi-value filters
   - Handling the single-value case as a degenerate multi-value case
   
   Call `apply_filter` with the `license` parameter value and the `package_license` entity column.

3. **Join through `package_license` entity.** Use the `package_license` SeaORM entity (from `entity/src/package_license.rs`) to join the `package` table to the `package_license` table. This is necessary because the license data lives in a separate join table. The join would use SeaORM's `.join()` or `.find_also_related()` method on the query builder, filtering on `package_license::Column::License`.

4. **Add input validation.** Validate the license values before applying the filter. If any value is empty or contains invalid characters, return an `AppError` with a 400 Bad Request status. Follow the error handling pattern used in the advisory service (`.context()` wrapping).

**Reuse:** `apply_filter` is reused directly -- no reimplementation of comma-separated parsing or SQL IN clause generation. The `package_license` entity is reused for the join -- no raw SQL. The error handling pattern (`.context()` with `AppError`) follows existing conventions.

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create an integration test file with the following test functions, following the sibling test conventions discovered in Step 4:

1. **`test_list_packages_filter_by_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Seed test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0)
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200, `items` contains only MIT-licensed packages, assert on specific package fields (not just count)

2. **`test_list_packages_filter_by_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: Same fixture data
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200, `items` contains packages with MIT or Apache-2.0 licenses, assert on specific package identifiers

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages (no regression).`
   - Given: Same fixture data
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200, `items` contains all seeded packages, `total_count` matches expected total

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: Same fixture data
   - When: `GET /api/v2/package?license=` (empty value or invalid format)
   - Then: Response status is 400

**Test structure conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` or `StatusCode::BAD_REQUEST` pattern
- Deserialize response body into `PaginatedResults<PackageSummary>`
- Validate `total_count`, `items.len()`, and specific item field values
- Use given-when-then section comments inside each test body
- Each test function has a `///` doc comment

### Module registration

Would also check `tests/api/` for a `mod.rs` or any module declaration file that registers test submodules. If test files are auto-discovered (common in Rust workspaces with `tests/` directory), no registration is needed. If there is a `mod.rs`, would add `mod package_license_filter;` to it.

### Documentation impact

- `docs/api.md` -- would update the `GET /api/v2/package` section to document the new optional `license` query parameter, its accepted values (SPDX identifiers), and the comma-separated multi-value syntax
- No other documentation changes needed (this is a filter addition, not an architectural change)

## Step 7 -- Write Tests

Tests described above in Step 6, File 3. Would run `cargo test` after writing them and fix any failures.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | Covered by `test_list_packages_filter_by_single_license` |
| GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | Covered by `test_list_packages_filter_by_multiple_licenses` |
| GET /api/v2/package without license returns all packages | Covered by `test_list_packages_no_license_filter` |
| PaginatedResults<PackageSummary> response shape unchanged | Verified by deserialization in all tests; no changes to `PackageSummary` or `PaginatedResults` |
| Invalid license values return 400 | Covered by `test_list_packages_invalid_license_returns_400` |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs`, `tests/api/package_license_filter.rs`, and potentially `docs/api.md`
- First two are in Files to Modify, third is in Files to Create
- `docs/api.md` is out-of-scope but justified by documentation impact; would ask user approval

### Sensitive-pattern check
- No passwords, API keys, secrets, or `.env` files involved in this change

### Data-flow trace
- Input: `license` query parameter in HTTP request -> Axum `Query<T>` extraction in `list.rs`
- Processing: Passed to `PackageService::list()` -> `apply_filter()` parses comma-separated values -> SeaORM join through `package_license` table -> SQL `WHERE license IN (...)` clause
- Output: Filtered `PaginatedResults<PackageSummary>` returned as JSON response
- **COMPLETE** -- all stages connected

### Contract & sibling parity
- `PackageService::list()` signature change is backward-compatible (new optional parameter)
- Sibling parity with advisory severity filter: both use same query struct pattern, same `apply_filter` call, same service-layer plumbing
- No caller-site anomalies expected since this adds a new optional parameter

### Duplication check
- The `apply_filter` function is reused, not duplicated
- No new comma-separated parsing logic written
- No new SQL generation logic written

## Step 10 -- Commit and Push

Would execute:
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
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Step 11 -- Update Jira

Would execute:
1. Update `customfield_10875` (Git Pull Request) with PR URL in ADF format
2. Add Jira comment with PR link, summary of changes, and no deviations from plan
3. Transition TC-9203 to In Review
