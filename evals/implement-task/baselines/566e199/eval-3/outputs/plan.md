# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value
and comma-separated multi-value filtering by SPDX license identifier. The implementation
reuses existing query infrastructure and follows the established filter pattern from the
advisory module.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add `license` query parameter extraction and filtering to the package list endpoint.

**Changes:**

- Add an optional `license` field (type `Option<String>`) to the query parameter struct
  (following the same pattern as the `severity` field in
  `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, when the `license` query parameter is present, call
  `common/src/db/query.rs::apply_filter` to parse the parameter value (which handles
  both single-value like `MIT` and comma-separated multi-value like `MIT,Apache-2.0`)
  and produce the appropriate SQL `IN` clause or equality condition.
- Pass the parsed filter to `PackageService::list()` so it can be applied to the database
  query. The filter should join through `entity/src/package_license.rs` to resolve
  package-to-license relationships.
- Return `400 Bad Request` for invalid license values using the existing `AppError`
  error handling pattern (all handlers return `Result<T, AppError>` with `.context()`).

**Reuse:** Directly reuse `apply_filter` from `common/src/db/query.rs` for comma-separated
parameter parsing — do NOT write new parsing logic. Follow the structural pattern from
`modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter) as a template
for how to wire the query parameter into the handler and pass it to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filter support to the `PackageService` list method.

**Changes:**

- Modify the `list` method signature to accept an optional license filter parameter
  (matching the pattern used by `AdvisoryService` in
  `modules/fundamental/src/advisory/service/advisory.rs` for the severity filter).
- When the license filter is present, add a JOIN to the `package_license` table using
  the SeaORM entity defined in `entity/src/package_license.rs`. This entity already
  maps packages to licenses — use it for the JOIN rather than writing raw SQL.
- Apply the filter condition to restrict results to packages whose associated license
  records match the requested SPDX identifier(s).
- Ensure the `PaginatedResults<PackageSummary>` response shape is unchanged — only the
  query is modified, not the output structure.

**Reuse:** Use `entity/src/package_license.rs` (the existing SeaORM entity for the
package-license join table) to build the JOIN query. Do NOT write raw SQL or create a
new entity for this relationship.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on the package list endpoint.

**Changes:**

- Follow the test conventions observed in sibling test files (`tests/api/advisory.rs`,
  `tests/api/sbom.rs`): use `assert_eq!(resp.status(), StatusCode::OK)` for status
  checks, deserialize response bodies, and validate both the item count and specific
  field values.
- Add a doc comment (`///`) before each test function explaining what it verifies.
- Use given-when-then section comments (`// Given`, `// When`, `// Then`) for non-trivial
  tests.

**Test cases:**

1. **`test_list_packages_filter_single_license`** — Verify that `GET /api/v2/package?license=MIT`
   returns only packages with an MIT license. Assert on specific package fields, not just count.

2. **`test_list_packages_filter_multi_license`** — Verify that
   `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
   Assert that all returned packages have one of the two requested licenses.

3. **`test_list_packages_no_license_filter`** — Verify that `GET /api/v2/package` without
   the license parameter returns all packages unchanged (no regression).

4. **`test_list_packages_invalid_license`** — Verify that an invalid license value returns
   `400 Bad Request` with an appropriate error message.

---

## Files NOT Modified (out of scope)

The following files are explicitly not touched by this task:

- `modules/fundamental/src/package/endpoints/mod.rs` — route registration does not change;
  the existing route for `list.rs` already handles `GET /api/v2/package`.
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct is unchanged;
  only the input accepts a new parameter, not the output.
- `entity/src/package_license.rs` — used as-is for the JOIN; no modifications needed.
- `common/src/db/query.rs` — `apply_filter` is reused as-is; no modifications needed.

---

## Implementation Approach

### Step-by-step

1. **Inspect the advisory filter pattern**: Read the severity filter implementation in
   `modules/fundamental/src/advisory/endpoints/list.rs` to understand the exact struct
   field declaration, handler wiring, and service call pattern.

2. **Inspect `apply_filter`**: Read `common/src/db/query.rs::apply_filter` to confirm it
   handles comma-separated values and produces the correct SQL filter (IN clause for
   multiple values, equality for single value).

3. **Inspect `package_license` entity**: Read `entity/src/package_license.rs` to understand
   the SeaORM entity columns and relationships for building the JOIN.

4. **Modify `list.rs` (endpoints)**: Add the `license` field to the Query struct and call
   `apply_filter` in the handler, following the advisory severity pattern exactly.

5. **Modify `mod.rs` (service)**: Add the license filter parameter to `PackageService::list()`
   and build the JOIN query using `package_license` entity.

6. **Create integration tests**: Write the four test cases in
   `tests/api/package_license_filter.rs` following sibling test conventions.

7. **Run tests**: Execute `cargo test` to verify all new tests pass and no existing tests
   regress.

8. **Verify acceptance criteria**: Confirm each criterion is satisfied by the implementation
   and test results.

### Convention conformance

- **Error handling**: Use `Result<T, AppError>` with `.context()` wrapping (matches all
  handlers in the codebase).
- **Naming**: Follow `verb_noun` pattern for service methods.
- **Response type**: Return `PaginatedResults<PackageSummary>` unchanged.
- **Query helpers**: Use shared `apply_filter` from `common/src/db/query.rs`.
- **Testing**: Follow `assert_eq!(resp.status(), ...)` pattern from sibling test files.
