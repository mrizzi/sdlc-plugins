# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: present with `trustify-backend` entry (Serena instance: `serena_backend`, path: `./`)
- Jira Configuration: present with Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present with tool naming convention and `serena_backend` instance

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description for TC-9203:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a `license` query parameter to `GET /api/v2/package` for filtering packages by SPDX license identifier. Support single-value and comma-separated multi-value filtering. |
| Dependencies | None |
| Bookend Type | (not present) |
| Target PR | (not present) |

**Files to Modify:**
1. `modules/fundamental/src/package/endpoints/list.rs` -- add license query parameter extraction and filtering
2. `modules/fundamental/src/package/service/mod.rs` -- add license filter to PackageService list method

**Files to Create:**
1. `tests/api/package_license_filter.rs` -- integration tests for the license filter

**API Changes:**
- `GET /api/v2/package?license=MIT` -- add optional `license` query parameter for filtering
- `GET /api/v2/package?license=MIT,Apache-2.0` -- support comma-separated license values

**Acceptance Criteria:**
1. `GET /api/v2/package?license=MIT` returns only packages with MIT license
2. `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license
3. `GET /api/v2/package` without license parameter returns all packages (no regression)
4. Response shape (`PaginatedResults<PackageSummary>`) remains unchanged
5. Invalid license values return 400 Bad Request

**Test Requirements:**
1. Test single license filter returns only matching packages
2. Test comma-separated license filter returns packages matching any listed license
3. Test no license filter returns all packages unchanged
4. Test invalid license value returns 400

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would transition TC-9203 to In Progress and assign to current user via Jira API. (Skipped per eval instructions -- no external service calls.)

## Step 4 -- Understand the Code

### Files to inspect (using Serena instance `serena_backend`)

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to see the current query struct and handler function structure.
   - Use `mcp__serena_backend__find_symbol` with `include_body=true` on the handler function and query struct to read the current implementation.

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify)
   - Use `mcp__serena_backend__get_symbols_overview` to see the PackageService methods.
   - Use `mcp__serena_backend__find_symbol` on the `list` method to understand its current signature and query construction.

3. **`common/src/db/query.rs`** (reuse candidate)
   - Use `mcp__serena_backend__find_symbol` on `apply_filter` to understand its signature, parameters, and how it handles comma-separated values and SQL IN clause generation.

4. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate / sibling)
   - Use `mcp__serena_backend__get_symbols_overview` to see the advisory list query struct (which includes the `severity` filter field).
   - Use `mcp__serena_backend__find_symbol` on the query struct and handler to understand the pattern for optional filter fields.

5. **`entity/src/package_license.rs`** (reuse candidate)
   - Use `mcp__serena_backend__get_symbols_overview` to see the entity struct and its SeaORM column definitions, which are needed for the JOIN query.

6. **`modules/fundamental/src/package/model/summary.rs`** -- verify `PackageSummary` struct has a `license` field (mentioned in repo structure).

7. **`modules/fundamental/src/package/endpoints/mod.rs`** -- verify route registration pattern to confirm no changes needed there.

### Sibling analysis for convention conformance

**Production code siblings:**
- `modules/fundamental/src/advisory/endpoints/list.rs` -- structurally identical endpoint (list with optional filter). Examine the Query struct pattern, how `severity` is extracted, how the filter is threaded from handler to service.
- `modules/fundamental/src/sbom/endpoints/list.rs` -- another list endpoint sibling for cross-referencing patterns.

**Expected discovered conventions (based on repo documentation):**
- Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping
- Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`
- Framework: Axum for HTTP, SeaORM for database
- Module pattern: `model/ + service/ + endpoints/` structure

### Test sibling analysis

**Test siblings to examine:**
- `tests/api/advisory.rs` -- advisory endpoint integration tests (closest analogue since advisory has a filter)
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- search endpoint tests

**Expected discovered test conventions:**
- Assertion style: `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Response validation: list endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Error cases: tests include status code assertions for error responses (e.g., 400, 404)
- Test naming: `test_<endpoint>_<scenario>` pattern
- Test setup: tests hit a real PostgreSQL test database

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (check for CI commands and verification commands)
- `docs/api.md` -- REST API reference (may need updating for new query parameter)

### CONVENTIONS.md lookup

Would read `CONVENTIONS.md` at the repository root to extract:
- CI check commands (for Step 9 verification)
- Code generation commands
- Project-specific conventions

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

1. **Add `license` field to the Query struct**: Following the pattern from `modules/fundamental/src/advisory/endpoints/list.rs` where the `severity` query parameter is defined as an optional field in the Query struct, add:

   ```rust
   /// Optional license filter. Supports single SPDX identifier or comma-separated list.
   pub license: Option<String>,
   ```

2. **Extract and validate the license parameter in the handler function**: In the list handler, after extracting the query parameters, check if `license` is provided. If provided, validate the value (non-empty string after splitting on commas; return 400 Bad Request for empty/invalid values).

3. **Pass the license filter to the service layer**: Call `PackageService::list()` with the new license filter parameter, threading it through from the handler to the service.

4. **Reuse `apply_filter` from `common/src/db/query.rs`**: Use the `apply_filter` function to handle parsing the comma-separated values and generating the SQL IN clause. This function already handles both single-value and multi-value comma-separated parameters, so no new parsing logic is needed.

### File 2: `modules/fundamental/src/package/service/mod.rs`

**Changes:**

1. **Add `license` parameter to the `list` method signature**: Add an `Option<String>` parameter for the license filter.

2. **Build the license filter query**: When the license parameter is provided:
   - Join the `package` table with the `package_license` table using the entity defined in `entity/src/package_license.rs` (SeaORM entity).
   - Use `apply_filter` from `common/src/db/query.rs` to generate the filter condition (IN clause for comma-separated values, equality for single value).
   - Apply the filter condition to the existing query.

3. **Preserve existing behavior**: When the license parameter is `None`, the query remains unchanged (no JOIN, no filter), ensuring no regression for the existing endpoint behavior.

4. **Use `find_referencing_symbols` on the `list` method** before modifying its signature to identify all callers and ensure the signature change does not break them. Update all call sites to pass the new parameter (likely passing `None` where no license filter is needed).

### File 3 (new): `tests/api/package_license_filter.rs`

**Changes:**

1. **Register the new test file**: Add `mod package_license_filter;` to `tests/api/mod.rs` (or however the test modules are registered -- verify from sibling test structure).

2. **Create four test functions** following the test conventions discovered from sibling analysis:

   ```rust
   /// Verifies that filtering by a single license returns only packages with that license.
   #[tokio::test]
   async fn test_list_packages_filter_single_license() {
       // Given a database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
       // When requesting GET /api/v2/package?license=MIT
       // Then only packages with MIT license are returned
       // Assert: resp.status() == StatusCode::OK
       // Assert: all returned items have license == "MIT"
       // Assert: specific expected package names/ids are present (value-based assertions)
   }

   /// Verifies that filtering by comma-separated licenses returns packages matching any listed license.
   #[tokio::test]
   async fn test_list_packages_filter_multiple_licenses() {
       // Given a database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
       // When requesting GET /api/v2/package?license=MIT,Apache-2.0
       // Then packages with either MIT or Apache-2.0 license are returned
       // Assert: resp.status() == StatusCode::OK
       // Assert: returned items have license in ["MIT", "Apache-2.0"]
       // Assert: no GPL-3.0 packages are returned
   }

   /// Verifies that omitting the license parameter returns all packages unchanged.
   #[tokio::test]
   async fn test_list_packages_no_license_filter() {
       // Given a database seeded with packages having various licenses
       // When requesting GET /api/v2/package (no license parameter)
       // Then all packages are returned regardless of license
       // Assert: resp.status() == StatusCode::OK
       // Assert: total_count matches expected total
       // Assert: packages with different licenses are all present
   }

   /// Verifies that an invalid license value returns a 400 Bad Request response.
   #[tokio::test]
   async fn test_list_packages_invalid_license_filter() {
       // Given a running server
       // When requesting GET /api/v2/package?license=<invalid-value>
       // Then a 400 Bad Request is returned
       // Assert: resp.status() == StatusCode::BAD_REQUEST
   }
   ```

### Documentation impact

- `docs/api.md` should be updated to document the new `license` query parameter on the `GET /api/v2/package` endpoint, including:
  - Parameter name: `license`
  - Type: string (optional)
  - Description: filter by SPDX license identifier; supports comma-separated values for OR matching
  - Examples: `?license=MIT`, `?license=MIT,Apache-2.0`

### Cross-section reference consistency

- Entity `PackageService` list method: referenced in both Files to Modify (`service/mod.rs`) and Implementation Notes -- paths are consistent.
- Entity `apply_filter`: referenced in Implementation Notes (`common/src/db/query.rs`) and Reuse Candidates -- paths are consistent.
- Entity `package_license`: referenced in Implementation Notes (`entity/src/package_license.rs`) and Reuse Candidates -- paths are consistent.
- No cross-section mismatches detected.

## Step 7 -- Write Tests

See File 3 above. Tests follow sibling conventions from `tests/api/advisory.rs`:
- Use `assert_eq!(resp.status(), ...)` for status code checks
- Deserialize response body and validate `total_count`, `items.len()`, and specific field values
- Value-based assertions (check actual license values, not just counts)
- Document every test function with `///` doc comments
- Include given-when-then section comments for non-trivial tests

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Covered by `test_list_packages_filter_single_license` |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Covered by `test_list_packages_filter_multiple_licenses` |
| No license parameter returns all packages (no regression) | Covered by `test_list_packages_no_license_filter` |
| Response shape (`PaginatedResults<PackageSummary>`) unchanged | Verified by not modifying the response type; tests deserialize into same type |
| Invalid license values return 400 | Covered by `test_list_packages_invalid_license_filter` |

## Step 9 -- Self-Verification

### Scope containment
Expected modified files:
- `modules/fundamental/src/package/endpoints/list.rs` (in scope)
- `modules/fundamental/src/package/service/mod.rs` (in scope)
- `tests/api/package_license_filter.rs` (in scope -- Files to Create)

Potentially out-of-scope files that may need changes:
- `tests/api/mod.rs` or `tests/Cargo.toml` -- to register the new test module (would flag and ask user approval)
- `docs/api.md` -- documentation update for the new parameter (would flag and ask user approval)

### Data-flow trace
- `GET /api/v2/package?license=MIT` --> handler extracts `license` from Query struct --> validates non-empty --> passes to `PackageService::list()` --> service JOINs `package_license` table using SeaORM entity --> `apply_filter` generates IN clause --> query executes --> results returned as `PaginatedResults<PackageSummary>` --> response serialized to JSON -- **COMPLETE**

### Contract & sibling parity
- `PackageService::list()` -- signature change adds optional parameter; all existing callers updated to pass `None`
- Sibling parity with `AdvisoryService::list()` which has `severity` filter -- same pattern followed
- Error handling: same `Result<T, AppError>` with `.context()` pattern as siblings

### Duplication check
- No new utility functions created; reusing existing `apply_filter` from `common/src/db/query.rs`
- No new entity definitions; reusing existing `package_license` entity from `entity/src/package_license.rs`

## Step 10 -- Commit and Push

```
git add modules/fundamental/src/package/endpoints/list.rs \
       modules/fundamental/src/package/service/mod.rs \
       tests/api/package_license_filter.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that filters
packages by SPDX license identifier. Supports both single-value and
comma-separated multi-value filtering using the existing apply_filter utility.

Implements TC-9203"
```

Then:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" --body "..."
```

## Step 11 -- Update Jira

- Set `customfield_10875` (Git Pull Request) to the PR URL using ADF inlineCard format
- Add comment summarizing changes: added license filter parameter, reused apply_filter and package_license entity, all tests passing
- Transition TC-9203 to In Review
