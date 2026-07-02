# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared license (exact match on the SPDX identifier). Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Project Configuration Validation (Step 0)

Verified from `claude-md-mock.md`:
- Repository Registry: present, lists `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present with project key TC, Cloud ID, Feature issue type ID
- Code Intelligence: present with `serena_backend` instance using rust-analyzer

## Task Parsing (Step 1)

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None (standard implementation flow)
- **Target PR**: None (new branch and PR)

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state**: This file contains the handler for `GET /api/v2/package`. It has a Query struct for extracting query parameters and a handler function that calls `PackageService::list()`.

**Changes**:

1. **Add `license` field to the Query struct**: Add an `Option<String>` field named `license` to the existing query parameter extraction struct, following the same pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`. The field should be optional so that omitting it returns all packages (no regression).

2. **Validate the license parameter**: If the `license` parameter is present, validate that each comma-separated value is a non-empty string. If any value is empty or contains invalid characters, return a 400 Bad Request error using `AppError` from `common/src/error.rs`. This satisfies the acceptance criterion for invalid license values.

3. **Pass the license filter to the service layer**: Extract the `license` field from the query struct and pass it to `PackageService::list()` as an additional parameter (or as part of a filter/options struct, depending on the existing method signature pattern). Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string into individual values — do NOT reimplement the parsing logic.

4. **Preserve the response shape**: The handler must continue to return `PaginatedResults<PackageSummary>`. No changes to the response type.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state**: This file contains `PackageService` with `fetch` and `list` methods. The `list` method queries the package table and returns paginated results.

**Changes**:

1. **Accept the license filter parameter**: Modify the `list` method signature to accept an optional license filter parameter (e.g., `license: Option<Vec<String>>` or similar, depending on what `apply_filter` produces).

2. **Build the filter query using `apply_filter`**: Use `common/src/db/query.rs::apply_filter` to construct the SQL IN clause for license filtering. This function already handles both single and multi-value comma-separated parameters, so reuse it directly rather than writing custom parsing or SQL generation.

3. **Join through `package_license` entity**: When a license filter is present, add a JOIN to the `package_license` table (using the SeaORM entity from `entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers. This is a conditional join — only added when the license parameter is provided, so unfiltered queries are not penalized.

4. **Ensure DISTINCT results**: When joining through `package_license`, a package with multiple licenses could appear multiple times. Add a DISTINCT clause or use SeaORM's deduplication to ensure each package appears only once in the results.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the license filter on `GET /api/v2/package`.

**Conventions to follow** (from sibling test analysis of `tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`):
- Use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- Hit a real PostgreSQL test database
- Follow `test_<endpoint>_<scenario>` naming convention
- Validate `total_count`, `items.len()`, and key fields of returned items (value-based assertions, not just length checks)
- Add `///` doc comments before every test function
- Add `// Given`, `// When`, `// Then` section comments inside non-trivial tests

**Test functions to implement**:

1. **`test_list_packages_filter_single_license`**
   - Doc: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status 200, all returned packages have MIT license, packages with other licenses are excluded. Assert on specific package names/identifiers, not just count.

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status 200, returned packages have either MIT or Apache-2.0 license, GPL-3.0 packages excluded. Assert on specific values.

3. **`test_list_packages_no_license_filter`**
   - Doc: `/// Verifies that omitting the license parameter returns all packages unchanged (no regression).`
   - Given: seed database with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: response status 200, all packages returned, `total_count` matches expected count. Verify response shape is `PaginatedResults<PackageSummary>`.

4. **`test_list_packages_invalid_license`**
   - Doc: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: no special seeding needed
   - When: `GET /api/v2/package?license=` (empty value) or other invalid input
   - Then: response status 400 Bad Request

**Module registration**: Add `mod package_license_filter;` to the test module declaration (likely `tests/api/mod.rs` or the test crate root).

## API Changes

- `GET /api/v2/package` — add optional `license` query parameter
  - Single value: `?license=MIT`
  - Multi-value: `?license=MIT,Apache-2.0`
  - Omitted: returns all packages (existing behavior preserved)
  - Invalid: returns 400 Bad Request
  - Response shape `PaginatedResults<PackageSummary>` is unchanged

## Convention Conformance

Based on sibling analysis (advisory endpoints, sbom endpoints):

- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Service methods**: Follow `verb_noun` pattern (e.g., `list_packages`)
- **Query helpers**: Use shared filtering via `common/src/db/query.rs`
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: `model/ + service/ + endpoints/` structure

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` -> extract query params (endpoints/list.rs) -> validate license param -> pass to `PackageService::list()` (service/mod.rs) -> `apply_filter` parses comma-separated values (common/src/db/query.rs) -> JOIN `package_license` entity (entity/src/package_license.rs) -> SQL query with IN clause -> return `PaginatedResults<PackageSummary>` -> HTTP 200 response -- **COMPLETE**

## Scope

All changes are strictly within the files listed in the task:
- Modify: `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs`
- Create: `tests/api/package_license_filter.rs`

No out-of-scope files will be modified. The response shape remains unchanged. No new utility functions will be created — all filtering logic reuses `apply_filter` from `common/src/db/query.rs`.
