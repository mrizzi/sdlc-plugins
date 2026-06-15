# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, enabling
consumers to filter packages by their declared license (exact match on the SPDX
identifier). Support both single-value and comma-separated multi-value filtering.

## Project Configuration Validation (Step 0)

The project CLAUDE.md contains all required sections:

- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
- **Code Intelligence**: Serena tool naming convention and `serena_backend` instance with `rust-analyzer`

All prerequisites satisfied — proceed with implementation.

## Task Description Parsing (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add `license` query parameter to `GET /api/v2/package` for filtering by SPDX identifier, with comma-separated multi-value support
- **Files to Modify**: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs`
- **Files to Create**: `tests/api/package_license_filter.rs`
- **API Changes**: `GET /api/v2/package?license=MIT` (single), `GET /api/v2/package?license=MIT,Apache-2.0` (multi)
- **Target PR**: none
- **Bookend Type**: none
- **Dependencies**: none
- **Linked Issues**: is incorporated by TC-9001

## Code Understanding Plan (Step 4)

### Files to Inspect via Serena (`mcp__serena_backend__<tool>`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current GET handler
   - Use `get_symbols_overview` to see the current Query struct and handler function signature
   - Use `find_symbol` with `include_body=true` on the handler function to read the current filtering logic

2. **`modules/fundamental/src/package/service/mod.rs`** — PackageService
   - Use `get_symbols_overview` to see `PackageService` methods
   - Use `find_symbol` on the `list` method to understand its current signature and query construction

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** — sibling pattern (Reuse Candidate)
   - Use `get_symbols_overview` to see the advisory Query struct with its `severity` field
   - Use `find_symbol` on the advisory handler to understand how it extracts and applies the severity filter — this is the structural template for the license filter

4. **`common/src/db/query.rs`** — shared query helpers (Reuse Candidate)
   - Use `find_symbol` on `apply_filter` to understand its signature, parameters, and how it handles comma-separated values and generates SQL IN clauses

5. **`entity/src/package_license.rs`** — package-license entity (Reuse Candidate)
   - Use `get_symbols_overview` to see the entity struct, its fields, and SeaORM relations
   - Understand the join path from Package to PackageLicense for the filter query

6. **`modules/fundamental/src/package/model/summary.rs`** — PackageSummary
   - Use `get_symbols_overview` to confirm the response type includes a `license` field and will not change

7. **`modules/fundamental/src/package/endpoints/mod.rs`** — route registration
   - Inspect to see how existing package routes are mounted; the list endpoint route should already exist

### Sibling Test Files to Inspect

8. **`tests/api/advisory.rs`** — sibling integration test
   - Use `get_symbols_overview` to understand test patterns: assertion style, setup, naming conventions
   - Use `find_symbol` on a filter-related test (e.g., `test_list_advisories_filtered`) to understand how filter tests are structured

9. **`tests/api/sbom.rs`** — additional sibling test
   - Confirm the testing pattern is consistent across modules

### Documentation Files to Check

10. **`CONVENTIONS.md`** at repository root — read for project conventions and CI check commands
11. **`docs/api.md`** — API documentation that may need updating for the new query parameter

### Convention Conformance Analysis

Discover conventions from siblings:

- **Error handling**: All handlers in `endpoints/` use `Result<T, AppError>` with `.context()` wrapping
- **Naming**: Service methods follow `verb_noun` pattern; query structs named `Query`
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query parameters**: Optional filter fields in the `Query` struct, deserialized by Axum's `Query` extractor
- **Filter application**: Filters use `apply_filter` from `common/src/db/query.rs`

### Test Convention Analysis

Expected conventions from sibling tests:

- **Assertion style**: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- **Response validation**: List tests validate `total_count`, `items.len()`, and key fields on items
- **Error cases**: Include 400 Bad Request tests for invalid parameters
- **Test naming**: `test_<endpoint>_<scenario>` pattern (e.g., `test_list_packages_license_filter`)

## Branch Creation (Step 5)

```
git checkout main
git pull
git checkout -b TC-9203
```

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes**:

- Add an `Option<String>` field named `license` to the existing `Query` struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`)
- In the handler function, extract the `license` value from the query parameters
- Pass the `license` filter value to `PackageService::list()` as a new parameter
- Add validation: if `license` is provided but contains only empty strings after splitting on commas, return a 400 Bad Request using `AppError`

**How (reusing existing code)**:

- Model the `license` field on the `severity` field in the advisory Query struct — same `Option<String>` type, same serde deserialization
- The handler logic for extracting and passing the filter follows the advisory handler's existing pattern exactly

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes**:

- Add a `license: Option<String>` parameter to the `list` method on `PackageService`
- When `license` is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and generate a SQL `IN` clause
- Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers
- When `license` is `None`, skip the filter entirely (existing behavior preserved)

**How (reusing existing code)**:

- Call `apply_filter(query, "license", license_value)` — this function already handles comma-separated parsing and IN clause generation
- Use the `package_license` SeaORM entity for the JOIN: `PackageLicense::find().filter(...)` or add a `.join()` clause to the existing query using SeaORM's relation model
- Follow the same query-building pattern used in the advisory service's `list` method for severity filtering

### 3. `modules/fundamental/src/package/endpoints/mod.rs` (potential — verify in Step 4)

- Confirm the route for `GET /api/v2/package` already passes through to `list.rs`. No change expected, but verify during code understanding.

## Files to Create

### 4. `tests/api/package_license_filter.rs`

**What to create**: Integration tests for the license filter feature.

**Test functions** (each with `///` doc comment and given-when-then structure where non-trivial):

1. **`test_list_packages_license_filter_single`**
   - Doc: "Verifies that filtering by a single license returns only packages with that license."
   - Setup: seed the test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - Action: `GET /api/v2/package?license=MIT`
   - Assert: response status is 200, `items` contains only MIT-licensed packages, assert on specific package names/identifiers (not just count)

2. **`test_list_packages_license_filter_multi`**
   - Doc: "Verifies that filtering by comma-separated licenses returns packages matching any listed license."
   - Setup: seed with MIT, Apache-2.0, and GPL-3.0 packages
   - Action: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert: response status is 200, `items` contains MIT and Apache-2.0 packages but not GPL-3.0, assert on specific values

3. **`test_list_packages_no_license_filter`**
   - Doc: "Verifies that omitting the license parameter returns all packages unchanged."
   - Setup: seed with multiple license types
   - Action: `GET /api/v2/package`
   - Assert: response status is 200, all seeded packages are present, response shape is `PaginatedResults<PackageSummary>`

4. **`test_list_packages_license_filter_invalid`**
   - Doc: "Verifies that an invalid license value returns 400 Bad Request."
   - Setup: standard seed
   - Action: `GET /api/v2/package?license=` (empty value)
   - Assert: response status is 400

5. **`test_list_packages_license_filter_no_match`**
   - Doc: "Verifies that filtering by a license with no matching packages returns an empty result set."
   - Setup: seed with MIT and Apache-2.0 packages
   - Action: `GET /api/v2/package?license=WTFPL`
   - Assert: response status is 200, `items` is empty, `total_count` is 0

**Module registration**: add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness's module file) if the test crate uses explicit module declarations.

## API Changes

- `GET /api/v2/package` — add optional `license` query parameter
  - Single value: `?license=MIT`
  - Multi-value: `?license=MIT,Apache-2.0`
  - No change to response shape (`PaginatedResults<PackageSummary>`)

## Acceptance Criteria Verification Plan (Step 8)

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | `test_list_packages_license_filter_single` |
| GET /api/v2/package?license=MIT,Apache-2.0 returns either | `test_list_packages_license_filter_multi` |
| GET /api/v2/package without license returns all packages | `test_list_packages_no_license_filter` |
| PaginatedResults<PackageSummary> response shape unchanged | All tests deserialize response as PaginatedResults<PackageSummary> |
| Invalid license values return 400 | `test_list_packages_license_filter_invalid` |

## Self-Verification Plan (Step 9)

1. **Scope containment**: `git diff --name-only` must list only the 2 modified files and 1 created file (plus potentially `tests/api/mod.rs` for module registration — an expected out-of-scope file that is necessary for the test to compile)
2. **Untracked file check**: verify `tests/api/package_license_filter.rs` is staged
3. **Sensitive-pattern check**: grep staged diff for secrets/credentials
4. **Documentation currency**: check if `docs/api.md` needs updating for the new query parameter
5. **Duplication check**: grep for any pre-existing license filter logic
6. **CI checks**: run commands from CONVENTIONS.md if found; otherwise `cargo build && cargo test`
7. **Data-flow trace**: request (`license` query param) -> extraction (handler) -> parsing (apply_filter) -> SQL JOIN + IN clause (service) -> filtered results (response) — verify all stages connected
8. **Contract & sibling parity**: verify PackageService::list matches sibling service patterns; verify handler follows advisory handler pattern

## Commit and PR (Step 10)

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value filtering by
SPDX license identifier. Reuses apply_filter from common/src/db/query.rs
and joins through the package_license entity.

Implements TC-9203"
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Jira Update (Step 11)

- Update custom field `customfield_10875` with PR URL (ADF format with inlineCard)
- Add comment with PR link, summary of changes, and confirmation of no deviations
- Transition TC-9203 to In Review
