# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, allowing consumers to filter packages by their declared license (SPDX identifier). Support both single-value and comma-separated multi-value filtering.

## Project Configuration Validation (Step 0)

- Repository Registry: `trustify-backend` with Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID present
- Code Intelligence: Serena instance `serena_backend` with `rust-analyzer`

All required sections are present. Proceed.

## Code Understanding (Step 4)

### Files to Inspect

Inspect the following existing files to understand current patterns before making changes:

1. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- The severity filter implementation is the structural template for the license filter. Inspect the `Query` struct to understand how optional filter fields are declared, how the query parameter is extracted from the Axum handler, and how `apply_filter` is called to build the SQL clause.

2. **`common/src/db/query.rs`** -- Read the `apply_filter` function signature and implementation. Understand its inputs (column reference, comma-separated string value) and outputs (SeaORM condition). This function already handles parsing comma-separated values and generating SQL `IN` clauses.

3. **`entity/src/package_license.rs`** -- Understand the SeaORM entity definition for the package-license join table. Identify the column names (likely `package_id` and `license` or `license_id`) to use in the JOIN query.

4. **`modules/fundamental/src/package/endpoints/list.rs`** -- Current state of the file to be modified. Understand the existing handler function signature, the existing `Query` struct (if any), and how the handler calls `PackageService`.

5. **`modules/fundamental/src/package/service/mod.rs`** -- Current state of `PackageService::list`. Understand the existing query builder, return type, and how other filters (if any) are applied.

6. **`modules/fundamental/src/package/model/summary.rs`** -- Understand `PackageSummary` struct to confirm the license field exists and the response shape.

7. **`entity/src/package.rs`** -- Package entity definition, needed to understand the primary key column for JOINs.

### Sibling Files for Convention Analysis

- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint with severity filter
- `modules/fundamental/src/sbom/endpoints/list.rs` -- sibling list endpoint for SBOMs
- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- sibling integration tests

### Discovered Conventions (expected from sibling analysis)

- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Query parameters:** List endpoints use a `Query` struct with `#[derive(Deserialize)]` for optional filter fields, extracted via Axum's `Query` extractor
- **Filter application:** Optional filter fields are checked with `if let Some(value) = query.field`, then `apply_filter` from `common/src/db/query.rs` is called
- **Response type:** All list endpoints return `PaginatedResults<T>`
- **Service methods:** Follow `verb_noun` pattern (e.g., `list_packages`)
- **Testing:** Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern, tests hit a real PostgreSQL test database

### Documentation Files Identified

- `docs/api.md` -- REST API reference (may need update for new query parameter)
- `CONVENTIONS.md` -- repository root conventions

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add the `license` query parameter extraction and filtering logic to the package list endpoint handler.

**Changes:**

1. **Add import for `apply_filter`**: Add `use common::db::query::apply_filter;` (or the appropriate module path based on existing imports in the file).

2. **Add import for `package_license` entity**: Add `use entity::package_license;` to access the join table entity for SeaORM queries.

3. **Extend the `Query` struct** (or create one if it does not exist yet): Add an optional `license` field following the exact same pattern used in the advisory list endpoint's `Query` struct for the `severity` field.

   ```rust
   #[derive(Deserialize)]
   pub struct Query {
       // ... existing fields (pagination, sorting, etc.)
       /// Optional license filter -- supports single value or comma-separated values (e.g., "MIT" or "MIT,Apache-2.0")
       pub license: Option<String>,
   }
   ```

4. **Apply the filter in the handler function**: After extracting the query parameters, check if `query.license` is `Some`, and if so, call `apply_filter` from `common/src/db/query.rs` to generate the SQL condition. This reuses the existing `apply_filter` function directly -- do NOT create a new utility function for parsing or filtering.

   ```rust
   if let Some(ref license) = query.license {
       // Reuse apply_filter which handles comma-separated parsing and IN clause generation
       let condition = apply_filter(package_license::Column::License, license);
       // Apply the condition via a JOIN on the package_license table
       // ... (join package_license on package.id = package_license.package_id, then filter)
   }
   ```

   The exact join mechanism depends on how SeaORM queries are structured in the existing codebase (likely using `.join()` or `.find_also_related()` on the query builder), following the pattern established in the advisory severity filter.

5. **Pass the filter to the service layer**: Pass the constructed filter condition (or the raw `Option<String>` license value) to `PackageService::list` so the service can incorporate it into the database query. Follow whichever pattern the advisory severity filter uses -- if the advisory endpoint passes the raw string to the service, do the same; if it builds the condition in the endpoint and passes a `Condition`, do that instead.

6. **Validate input**: If the license value is provided but empty or contains invalid characters, return a 400 Bad Request using the `AppError` pattern. Follow the validation approach used in the advisory severity filter.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering capability to the `PackageService::list` method.

**Changes:**

1. **Add import for `package_license` entity**: Add `use entity::package_license;` if not already imported.

2. **Add import for `apply_filter`**: Add `use common::db::query::apply_filter;` if the filtering is done at the service layer (depends on the pattern observed in the advisory service).

3. **Extend the `list` method signature**: Add an optional `license: Option<String>` parameter (or accept a filter struct, depending on the existing pattern in `AdvisoryService::list`).

4. **Apply the license filter in the query builder**: When `license` is `Some`:
   - JOIN the `package_license` entity table on `package.id = package_license.package_id`
   - Use `apply_filter(package_license::Column::License, &license)` to generate the WHERE condition for the joined table
   - This reuses `apply_filter` directly from `common/src/db/query.rs` -- the same function that handles comma-separated values and builds SQL IN clauses

   ```rust
   if let Some(ref license_filter) = license {
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
           .filter(apply_filter(package_license::Column::License, license_filter));
   }
   ```

5. **Ensure DISTINCT results**: When joining through `package_license`, a package with multiple matching licenses could appear multiple times. Add `.distinct()` or `GROUP BY` to the query to deduplicate results, following how the advisory severity filter handles similar join scenarios.

6. **Preserve response shape**: The return type remains `PaginatedResults<PackageSummary>` -- no changes to the response structure.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests verifying the license filter on `GET /api/v2/package`.

**Changes:**

Create a new test file following the patterns observed in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`). The tests should use the same test harness setup (PostgreSQL test database, HTTP client) as the sibling tests.

**Test functions to implement:**

1. **`test_filter_single_license`**: 
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT`
   - Then: response status is 200, response body contains only MIT-licensed packages, assert on specific package names/identifiers (not just count)

2. **`test_filter_comma_separated_licenses`**:
   - Doc comment: `/// Verifies that comma-separated license values return packages matching any listed license.`
   - Given: test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: response status is 200, response body contains packages with MIT or Apache-2.0 licenses (but not GPL-3.0), assert on specific values

3. **`test_no_license_filter_returns_all`**:
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: test database seeded with packages having various licenses
   - When: `GET /api/v2/package` (no license parameter)
   - Then: response status is 200, response includes all seeded packages, assert on total count and specific items

4. **`test_invalid_license_returns_400`**:
   - Doc comment: `/// Verifies that an invalid license value returns a 400 Bad Request response.`
   - Given: test database with any seeded data
   - When: `GET /api/v2/package?license=` (empty value or invalid format)
   - Then: response status is 400

**Test conventions to follow:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` / `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` pattern
- Deserialize response body as `PaginatedResults<PackageSummary>` and assert on `total_count`, `items.len()`, and specific item field values
- Use given-when-then section comments inside each test body
- Follow the `test_<endpoint>_<scenario>` naming convention

**Module registration:** Register the new test file in `tests/api/` module (add `mod package_license_filter;` to the appropriate `mod.rs` or `main.rs` test runner).

---

## Reuse Strategy Summary

| Reuse Candidate | How It Is Reused | Where Applied |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly to parse comma-separated license values and generate SQL IN clause | `list.rs` endpoint handler and/or `service/mod.rs` list method |
| `modules/fundamental/src/advisory/endpoints/list.rs` severity filter pattern | Follow the same Query struct pattern (optional field + conditional filter application) | `list.rs` Query struct definition and filter application logic |
| `entity/src/package_license.rs` | Use as the SeaORM entity for the JOIN query between packages and licenses | `service/mod.rs` JOIN clause in the list query builder |

No new utility functions are created. All filtering logic reuses `apply_filter` directly.

---

## Acceptance Criteria Verification Plan

| Criterion | Verification |
|---|---|
| GET /api/v2/package?license=MIT returns only MIT packages | `test_filter_single_license` integration test |
| GET /api/v2/package?license=MIT,Apache-2.0 returns matching packages | `test_filter_comma_separated_licenses` integration test |
| GET /api/v2/package without license returns all packages | `test_no_license_filter_returns_all` integration test |
| Response shape (PaginatedResults<PackageSummary>) unchanged | All tests deserialize response as PaginatedResults<PackageSummary> |
| Invalid license values return 400 | `test_invalid_license_returns_400` integration test |

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` -> Axum extracts `Query { license: Some("MIT") }` -> handler calls `apply_filter` to build condition -> passes to `PackageService::list` -> service JOINs `package_license` table and applies filter -> returns `PaginatedResults<PackageSummary>` -> serialized as JSON response -- **COMPLETE**

## Commit Plan

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package supporting
single and comma-separated SPDX identifier filtering. Reuses apply_filter
from common query helpers and joins through the existing package_license
entity.

Implements TC-9203
```
