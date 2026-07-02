# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering.

## Step 0 -- Project Configuration Validation

The project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena with rust-analyzer

## Step 1 -- Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **No Target PR**: standard flow (create new branch)
- **No Bookend Type**: standard implementation
- **Dependencies**: None

## Step 4 -- Code Understanding

### Files to Inspect

1. **`modules/fundamental/src/package/endpoints/list.rs`** (file to modify) -- current package list endpoint handler. Inspect its `Query` struct (or equivalent request-parameter struct) and handler function to understand how query parameters are currently extracted.

2. **`modules/fundamental/src/package/service/mod.rs`** (file to modify) -- `PackageService` with its `list` method. Understand its current signature, what filters it accepts, and how it builds database queries.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (reuse candidate / sibling) -- the advisory list endpoint already implements a `severity` query parameter filter using the same structural pattern we need. Inspect its `Query` struct to see how the optional `severity` field is defined, how it is extracted from the request, and how it is passed to the service layer.

4. **`common/src/db/query.rs`** (reuse candidate) -- shared query builder helpers. Inspect the `apply_filter` function signature to understand its input parameters (column reference, filter value string) and how it generates SQL `IN` clauses from comma-separated values.

5. **`entity/src/package_license.rs`** (reuse candidate) -- SeaORM entity for the package-license join table. Inspect the entity struct, its `Relation` definitions, and column names to understand how to join packages to licenses.

6. **Sibling endpoint files** -- inspect `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for convention conformance (error handling patterns, response types, import organization).

7. **Sibling test files** -- inspect `tests/api/advisory.rs` and `tests/api/sbom.rs` for test conventions (assertion style, setup patterns, naming conventions).

### Convention Expectations (from repo key conventions)

- Framework: Axum for HTTP, SeaORM for database
- All handlers return `Result<T, AppError>` with `.context()` wrapping
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Shared filtering via `common/src/db/query.rs`
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)`

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 -- Implementation Changes

### File 1: `modules/fundamental/src/package/endpoints/list.rs`

**What to change:**

1. **Add `license` field to the `Query` struct** -- following the exact same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`. Add an `Option<String>` field named `license` to the query parameter struct:

   ```rust
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       pub license: Option<String>,
   }
   ```

2. **Pass the license filter to the service layer** -- in the handler function, extract `query.license` and pass it to `PackageService::list()`. Follow the same parameter-passing pattern used by the advisory endpoint for its severity filter.

3. **Validate license values** -- if `license` is provided, validate that each comma-separated value is a non-empty string. Return `400 Bad Request` via `AppError` for invalid values (empty strings, whitespace-only values). Follow the existing error handling pattern (`Result<T, AppError>` with `.context()`).

**Reuse applied:**
- Follow the `Query` struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate 2)
- Do NOT create a new query parameter parsing function; the `apply_filter` function in `common/src/db/query.rs` (Reuse Candidate 1) handles comma-separated parsing downstream

### File 2: `modules/fundamental/src/package/service/mod.rs`

**What to change:**

1. **Add `license` parameter to the `list` method** -- add an `Option<String>` parameter (or incorporate it into an existing filter/options struct if one exists) to `PackageService::list()`.

2. **Build the filter query using `apply_filter`** -- when the `license` parameter is `Some`, use `common::db::query::apply_filter` to generate the SQL `IN` clause. This function handles parsing the comma-separated string into individual values and generating the appropriate `WHERE ... IN (...)` clause. Call it with the `package_license` table's license column as the target.

3. **Join through `package_license` entity** -- use the `entity::package_license` SeaORM entity (Reuse Candidate 3) to perform the JOIN between the `package` table and the `package_license` table. Use SeaORM's relation-based join API (e.g., `.join()` with the relation defined on the entity) rather than writing raw SQL. The join should be:
   - `package` JOIN `package_license` ON `package.id = package_license.package_id`
   - WHERE `package_license.license` IN (parsed values from `apply_filter`)

4. **Conditional join** -- only add the JOIN and WHERE clause when the `license` parameter is `Some`. When `None`, the query remains unchanged (no regression for existing callers).

5. **Deduplicate results** -- since a package can have multiple licenses, the JOIN may produce duplicate package rows when filtering. Apply `DISTINCT` or use SeaORM's `.distinct()` on the query to ensure each package appears only once in results.

**Reuse applied:**
- Use `common::db::query::apply_filter` directly for comma-separated parsing and IN clause generation (Reuse Candidate 1)
- Use `entity::package_license` entity for the JOIN rather than writing raw SQL (Reuse Candidate 3)
- Follow the same service-layer filter pattern as `AdvisoryService` (Reuse Candidate 2)

### No other files to modify

- **Response shape unchanged**: `PaginatedResults<PackageSummary>` is not modified
- **Route registration unchanged**: the existing route in `modules/fundamental/src/package/endpoints/mod.rs` already points to the list handler; adding an optional query parameter does not require route changes
- **No documentation updates needed**: no Documentation Updates section in the task, and the change is a backward-compatible optional parameter addition

## Step 7 -- Write Tests

### File to Create: `tests/api/package_license_filter.rs`

Following the test conventions from sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

1. **`test_filter_packages_by_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: seed the test database with packages having different licenses (MIT, Apache-2.0, GPL-3.0)
   - When: `GET /api/v2/package?license=MIT`
   - Then: `assert_eq!(resp.status(), StatusCode::OK)`, deserialize response as `PaginatedResults<PackageSummary>`, assert all returned packages have license `MIT`, assert on specific expected package names/identifiers (value-based assertions, not just count)

2. **`test_filter_packages_by_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any listed license.`
   - Given: seed the test database with packages having different licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert status OK, assert returned packages have either MIT or Apache-2.0 license, assert specific expected packages are present, assert GPL-3.0-only packages are excluded

3. **`test_list_packages_without_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged (no regression).`
   - Given: seed the test database with packages having different licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: assert status OK, assert all seeded packages are returned regardless of license

4. **`test_filter_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: test database is available
   - When: `GET /api/v2/package?license=` (empty value) or other invalid input
   - Then: `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`

Each non-trivial test includes `// Given`, `// When`, `// Then` section comments.

Register the new test file in `tests/Cargo.toml` or the test module's `mod.rs` if the project uses explicit test module registration.

## Step 8 -- Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| `?license=MIT` returns only MIT packages | `test_filter_packages_by_single_license` |
| `?license=MIT,Apache-2.0` returns matching packages | `test_filter_packages_by_multiple_licenses` |
| No license param returns all packages | `test_list_packages_without_license_filter` |
| Response shape unchanged | All tests deserialize as `PaginatedResults<PackageSummary>` |
| Invalid license returns 400 | `test_filter_packages_invalid_license` |

## Step 9 -- Self-Verification Checklist

- **Scope containment**: only `list.rs`, `service/mod.rs`, and new test file are touched -- all within Files to Modify / Files to Create
- **Sensitive-pattern check**: no secrets, credentials, or .env values introduced
- **Duplication check**: no new utility functions created -- all parsing/filtering logic reuses `apply_filter` from `common/src/db/query.rs`
- **Data-flow trace**: request parameter (`license` query string) -> endpoint extraction (Query struct) -> service layer (PackageService::list) -> database query (apply_filter + package_license JOIN) -> filtered results returned as PaginatedResults -- complete path
- **Contract & sibling parity**: handler follows same `Result<T, AppError>` return type as siblings; service method follows same filter parameter pattern as AdvisoryService

## Step 10 -- Commit and Push

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(api): add license filter to package list endpoint

Add optional 'license' query parameter to GET /api/v2/package that supports
single-value and comma-separated multi-value filtering by SPDX license
identifier. Reuses apply_filter from common query helpers and joins through
the existing package_license entity.

Implements TC-9203"
```

Then push and create PR with `--base main`.
