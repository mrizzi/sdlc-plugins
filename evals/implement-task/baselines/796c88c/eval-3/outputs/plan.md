# Implementation Plan: TC-9203 — Add Package License Filter to List Endpoint

## Task Summary

Add a `license` query parameter to the `GET /api/v2/package` list endpoint that filters
packages by their declared SPDX license identifier. Support both single-value and
comma-separated multi-value filtering.

## Target Branch

main

## Dependencies

None.

## Step 0 — Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena tool naming convention documented

Configuration is valid. Proceed.

## Step 4 — Understand the Code

### Files to Inspect

1. **`modules/fundamental/src/package/endpoints/list.rs`** — current package list endpoint;
   understand the existing query parameter extraction, handler signature, and how it calls
   PackageService.

2. **`modules/fundamental/src/package/service/mod.rs`** — current PackageService `list`
   method; understand how it builds the database query, applies existing filters, and
   returns `PaginatedResults<PackageSummary>`.

3. **`modules/fundamental/src/advisory/endpoints/list.rs`** (sibling/reuse reference) —
   the advisory list endpoint with the `severity` filter; understand the Query struct
   pattern with the optional filter field, how it calls `apply_filter`, and how the
   filter is passed to AdvisoryService.

4. **`common/src/db/query.rs`** — the shared `apply_filter` function; understand its
   signature, how it parses comma-separated values, and how it generates SQL IN clauses.

5. **`entity/src/package_license.rs`** — the PackageLicense entity (SeaORM); understand
   the table structure, column definitions, and relationships to the Package entity.

6. **`modules/fundamental/src/package/model/summary.rs`** — PackageSummary struct;
   confirm it already includes a `license` field (per repo-backend.md comment).

7. **`entity/src/package.rs`** — Package entity; understand the primary key and columns
   for building JOINs.

### Sibling Convention Analysis

**Production code conventions (from advisory module sibling):**
- **Handler pattern:** Endpoint handlers in `endpoints/list.rs` extract query parameters
  into a Query struct, then pass that struct to the corresponding Service method.
- **Query struct:** Uses an Axum `Query` extractor with a struct containing optional
  filter fields (e.g., `severity: Option<String>`).
- **Filter application:** The service method calls `apply_filter` from
  `common/src/db/query.rs`, passing the optional filter value and the target column.
- **Error handling:** Handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Response type:** List endpoints return `PaginatedResults<T>` from
  `common/src/model/paginated.rs`.

**Test conventions (from `tests/api/advisory.rs` and `tests/api/sbom.rs` siblings):**
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` followed by body
  deserialization into the expected response type.
- **Response validation:** List tests validate `total_count`, `items.len()`, and key
  fields on returned items.
- **Error cases:** Tests include status code checks for 400/404 error responses.
- **Test naming:** `test_<endpoint>_<scenario>` pattern.
- **Test setup:** Tests use a real PostgreSQL test database with fixture data insertion.

### CONVENTIONS.md

Check for `CONVENTIONS.md` at the repository root. If present, read and extract CI
check commands and code generation commands. Follow all listed conventions.

### Documentation Files

- `docs/api.md` — may need updating to document the new `license` query parameter.
- `README.md` — unlikely to need changes for a query parameter addition.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What exists now:** A handler function for `GET /api/v2/package` that extracts query
parameters (likely pagination: page, limit, sort) into a Query struct, then calls
`PackageService::list()`.

**Changes:**

1. **Add `license` field to the Query struct:**
   Add an optional `license` field to the existing query parameter struct:
   ```rust
   /// Optional license SPDX identifier filter. Supports comma-separated values.
   pub license: Option<String>,
   ```
   This follows the same pattern as the `severity: Option<String>` field in
   `modules/fundamental/src/advisory/endpoints/list.rs`.

2. **Pass `license` filter to the service method:**
   In the handler function, pass `query.license` to `PackageService::list()` as an
   additional parameter (or as part of a filter struct, depending on the existing
   signature pattern discovered in the advisory sibling).

3. **Add input validation:**
   If the license parameter contains values that are not valid SPDX identifiers (empty
   strings after splitting on comma, or whitespace-only values), return a 400 Bad Request
   using `AppError`. Follow the existing validation patterns in sibling endpoints.

**Reuse:** Follow the exact pattern from `modules/fundamental/src/advisory/endpoints/list.rs`
for how the advisory list endpoint defines its Query struct with `severity` and passes it
to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What exists now:** `PackageService` with a `list` method that builds a SeaORM query,
applies pagination/sorting, executes the query, and returns
`PaginatedResults<PackageSummary>`.

**Changes:**

1. **Add `license` parameter to the `list` method signature:**
   Add an `Option<String>` parameter for the license filter (or add it to an existing
   filter/options struct if the service uses one).

2. **Apply the license filter using `apply_filter`:**
   When the `license` parameter is `Some`, call `apply_filter` from
   `common/src/db/query.rs` to parse the comma-separated values and generate the
   appropriate SQL IN clause. This reuses the existing shared helper rather than
   writing custom parsing or SQL.

3. **JOIN through `package_license` entity:**
   Add a JOIN to the `package_license` table (using the `entity::package_license`
   SeaORM entity from `entity/src/package_license.rs`) to filter packages by their
   associated license SPDX identifiers. The join links `package.id` to
   `package_license.package_id`, and the filter applies to `package_license.license`
   (or equivalent column).

4. **Ensure no duplicates:**
   When filtering with a JOIN, add `.distinct()` to the query to prevent duplicate
   package rows when a package has multiple licenses and matches more than one filter
   value.

**Reuse:**
- `common/src/db/query.rs::apply_filter` — call directly for comma-separated parsing
  and SQL IN clause generation.
- `entity/src/package_license.rs` — use the SeaORM entity for the JOIN rather than
  writing raw SQL.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test functions:**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: Test database seeded with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT`
   - Then: Response status is 200. Response body contains only packages with MIT license.
     Assert on specific package names/identifiers, not just count. Verify
     `PaginatedResults<PackageSummary>` shape is correct (total_count, items).

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any of the listed licenses.`
   - Given: Same seeded data.
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: Response status is 200. Response body contains packages with either MIT or
     Apache-2.0 license (but not GPL-3.0). Assert on specific items and total_count.

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: Same seeded data.
   - When: `GET /api/v2/package` (no license parameter)
   - Then: Response status is 200. All seeded packages are returned. total_count matches
     the full set. This is a regression check.

4. **`test_list_packages_invalid_license_returns_400`**
   - Doc comment: `/// Verifies that an invalid license value returns a 400 Bad Request response.`
   - Given: Any state.
   - When: `GET /api/v2/package?license=` (empty value) or an otherwise invalid value.
   - Then: Response status is 400.

**Test conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.
- Deserialize body into `PaginatedResults<PackageSummary>`.
- Follow `test_<endpoint>_<scenario>` naming convention.
- Assert on specific item values (license field, package identifier), not just lengths.
- Include given-when-then section comments in each test.
- Add doc comments to every test function.

**Integration:** Register this test file in `tests/Cargo.toml` or the test module
structure (e.g., add `mod package_license_filter;` in the test module's `mod.rs` or
add a `[[test]]` entry in `Cargo.toml` if tests are standalone binaries).

---

## Verification Checklist

### Acceptance Criteria Verification

- [ ] `GET /api/v2/package?license=MIT` returns only MIT packages — covered by test 1
      and by the service layer filter implementation using `apply_filter` + JOIN.
- [ ] `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either —
      covered by test 2 and by `apply_filter`'s built-in comma-separated parsing.
- [ ] `GET /api/v2/package` without `license` returns all packages — covered by test 3;
      the `license` field is `Option<String>`, so `None` means no filter applied.
- [ ] Response shape `PaginatedResults<PackageSummary>` remains unchanged — the
      implementation only adds a query parameter; the service return type is unchanged.
- [ ] Invalid license values return 400 — covered by test 4 and input validation in
      the endpoint handler.

### Scope Containment

Only the three files listed above are modified or created. No other files are touched:
- `modules/fundamental/src/package/endpoints/list.rs` — modify (in scope)
- `modules/fundamental/src/package/service/mod.rs` — modify (in scope)
- `tests/api/package_license_filter.rs` — create (in scope)

Shared code (`common/src/db/query.rs`, `entity/src/package_license.rs`) is reused but
not modified.

### Data-Flow Trace

`GET /api/v2/package?license=MIT`
1. **Input:** Axum extracts `license=MIT` into `Query.license = Some("MIT")` -- CONNECTED
2. **Processing:** Handler passes `query.license` to `PackageService::list()` -- CONNECTED
3. **Processing:** `PackageService::list()` calls `apply_filter()` with the license value
   and JOINs through `package_license` entity -- CONNECTED
4. **Output:** SeaORM query returns filtered results, wrapped in
   `PaginatedResults<PackageSummary>` and returned as JSON response -- CONNECTED

Data flow is **COMPLETE**.

### CI Checks

Run all CI check commands from `CONVENTIONS.md` (if present). At minimum:
- `cargo build` — verify compilation
- `cargo test` — verify all tests pass (including the new ones)
- `cargo clippy` — verify no lint warnings
- `cargo fmt --check` — verify formatting
