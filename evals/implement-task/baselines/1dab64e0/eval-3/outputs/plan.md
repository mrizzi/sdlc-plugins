# Implementation Plan: TC-9203 -- Add Package License Filter to List Endpoint

## Overview

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering via exact match.

## Step 0 -- Validate Project Configuration

CLAUDE.md contains the required sections:
- Repository Registry: `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: project key TC, Cloud ID, feature issue type ID
- Code Intelligence: Serena with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Parse Task

- **Repository**: trustify-backend
- **Target Branch**: main
- **Dependencies**: None
- **Bookend Type**: None
- **Target PR**: None

Standard implementation flow applies.

## Step 4 -- Understand the Code

### Files to Inspect

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** (Reuse Candidate -- sibling pattern)
   - Inspect the `Query` struct to see how `severity` is declared as an optional field
   - Inspect the handler function to see how the severity filter is extracted from query params and passed to the service layer
   - This is the structural template for the license filter

2. **`common/src/db/query.rs`** (Reuse Candidate -- shared utility)
   - Inspect the `apply_filter` function signature, parameters, and behavior
   - Confirm it handles comma-separated string parsing and SQL IN clause generation
   - Understand how it integrates with SeaORM query builders

3. **`entity/src/package_license.rs`** (Reuse Candidate -- existing entity)
   - Inspect the entity definition: table name, columns, relations
   - Identify the foreign key linking packages to licenses (likely `package_id` and a license identifier column)
   - Understand how to JOIN through this table in SeaORM

4. **`modules/fundamental/src/package/endpoints/list.rs`** (File to Modify)
   - Inspect current `Query` struct and handler to understand existing parameters
   - Identify where to add the new `license` field

5. **`modules/fundamental/src/package/service/mod.rs`** (File to Modify)
   - Inspect the `PackageService::list` method signature and query construction
   - Identify where to add the filter condition

6. **`modules/fundamental/src/package/model/summary.rs`**
   - Confirm `PackageSummary` includes a `license` field (per repo docs)
   - Verify response shape will not change

7. **Sibling test files**: `tests/api/sbom.rs`, `tests/api/advisory.rs`
   - Inspect test patterns: assertion style, response validation, error case coverage, naming conventions
   - Use as template for new test file

### Convention Conformance Analysis

Based on repo conventions:
- **Framework**: Axum for HTTP, SeaORM for database
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Response types**: List endpoints return `PaginatedResults<T>`
- **Query helpers**: Shared filtering via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database

### Documentation Files

- `README.md` at repo root
- `CONVENTIONS.md` at repo root
- `docs/api.md` -- REST API reference (may need updating to document new query parameter)

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implement Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

**Changes:**

1. **Add `license` field to the `Query` struct:**
   Follow the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`. Add an optional `license` field:

   ```rust
   #[derive(Debug, Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter. Supports single SPDX identifier or comma-separated list.
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer:**
   In the handler function, extract `query.license` and pass it to `PackageService::list()`. Follow the same extraction pattern used for the advisory severity filter -- pass it as an `Option<String>` to the service method.

3. **Add input validation:**
   If `license` is provided but contains empty strings after splitting on comma (e.g., `?license=,` or `?license=MIT,,Apache-2.0`), return a 400 Bad Request using `AppError`. Follow the same validation pattern used in sibling endpoints.

**Reuse:**
- Pattern from `modules/fundamental/src/advisory/endpoints/list.rs` for the Query struct field declaration and handler extraction (Reuse Candidate 2)

### File 2: `modules/fundamental/src/package/service/mod.rs` (MODIFY)

**Changes:**

1. **Update the `list` method signature** to accept an optional license filter parameter:

   ```rust
   pub async fn list(
       &self,
       // ... existing parameters
       license: Option<String>,
   ) -> Result<PaginatedResults<PackageSummary>, AppError> {
   ```

2. **Add the license filter to the database query:**
   - Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated license string and generate the appropriate SQL IN clause
   - JOIN through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license identifiers
   - The JOIN uses SeaORM's relation API, linking through the `package_license` table's foreign keys

   ```rust
   if let Some(license_param) = license {
       // Use apply_filter from common/src/db/query.rs to handle
       // comma-separated values and generate IN clause
       let query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(apply_filter("license_identifier", &license_param));
   }
   ```

3. **Ensure the response shape remains `PaginatedResults<PackageSummary>`** -- no changes to the return type or serialization.

**Reuse:**
- `common/src/db/query.rs::apply_filter` for comma-separated parsing and SQL IN clause generation (Reuse Candidate 1)
- `entity/src/package_license.rs` entity for the JOIN query (Reuse Candidate 3)
- Pattern from advisory service's severity filter for the conditional filter application structure (Reuse Candidate 2)

### File 3: `tests/api/package_license_filter.rs` (CREATE)

**Changes:**

Create integration tests following the patterns observed in `tests/api/advisory.rs` and `tests/api/sbom.rs`:

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: assert response status is 200, assert all returned items have license == "MIT", assert on specific expected package names/identifiers (value-based assertions, not just count)

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: seed database with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert response status is 200, assert returned items have license in ["MIT", "Apache-2.0"], assert GPL-3.0 packages are excluded, assert on specific expected values

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: seed database with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: assert response status is 200, assert total count matches expected count of all seeded packages, assert response shape is `PaginatedResults<PackageSummary>`

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: any database state
   - When: `GET /api/v2/package?license=,` (empty after split)
   - Then: assert response status is 400

**Test conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Deserialize response body and validate `total_count`, `items.len()`, and item field values
- Include given-when-then section comments for all tests
- Test naming: `test_list_packages_<scenario>`

### Module Registration

- Add `mod package_license_filter;` to `tests/api/mod.rs` (or the test harness entry point) so the new test file is compiled and run.

### Documentation Impact

- Update `docs/api.md` to document the new `license` query parameter on `GET /api/v2/package`, including:
  - Parameter name, type (string), optionality (optional)
  - Single-value and comma-separated multi-value usage examples
  - 400 response for invalid values

## Step 7 -- Write Tests

Run `cargo test` after creating tests. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Test 1 covers this |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns matching packages | Test 2 covers this |
| No license parameter returns all packages | Test 3 covers this |
| Response shape unchanged | Tests validate PaginatedResults deserialization |
| Invalid license returns 400 | Test 4 covers this |

## Step 9 -- Self-Verification

### Scope Containment
Expected modified/created files:
- `modules/fundamental/src/package/endpoints/list.rs` (in Files to Modify)
- `modules/fundamental/src/package/service/mod.rs` (in Files to Modify)
- `tests/api/package_license_filter.rs` (in Files to Create)
- Possible: `tests/api/mod.rs` or equivalent (module registration -- out of scope, requires user approval)
- Possible: `docs/api.md` (documentation update -- out of scope, requires user approval)

### Data-Flow Trace
- `GET /api/v2/package?license=MIT` -> Axum extracts `Query` struct with `license: Some("MIT")` -> handler passes to `PackageService::list()` -> service calls `apply_filter` to parse value and build IN clause -> SeaORM JOINs `package_license` table and filters -> returns `PaginatedResults<PackageSummary>` -> serialized as JSON response -- **COMPLETE**

### Duplication Check
No new utility functions are created. All filtering logic reuses `apply_filter` from `common/src/db/query.rs`. No duplication risk.

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that
supports single-value and comma-separated multi-value SPDX license
filtering. Reuses apply_filter from common/src/db/query.rs and joins
through the existing package_license entity.

Implements TC-9203"
```

Then push and create PR targeting `main`:
```
git push -u origin TC-9203
gh pr create --base main --title "feat(api): add license filter to package list endpoint" ...
```
