# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to the `GET /api/v2/package` list endpoint,
supporting both single-value and comma-separated multi-value filtering by SPDX license
identifier. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Implements `GET /api/v2/package` with pagination and sorting but no
license filtering.

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern in
  `modules/fundamental/src/advisory/endpoints/list.rs`, add an optional `license: Option<String>`
  field to the existing query parameter struct used by the list handler. The advisory
  endpoint's `severity` field in its Query struct is the structural template for this
  addition.

- **Parse and apply the license filter:** In the handler function, extract the `license`
  value from the query parameters. Use `common/src/db/query.rs::apply_filter` to parse
  the comma-separated string into individual values and generate the appropriate SQL
  `IN` clause condition. Do NOT write a custom comma-splitting or filter-building
  function -- `apply_filter` already handles both single and multi-value cases.

- **Add JOIN through `package_license` entity:** Use the SeaORM entity defined in
  `entity/src/package_license.rs` to construct a JOIN from the `package` table to the
  `package_license` table. Apply the license filter condition on the joined
  `package_license` table's license column. This follows the same entity-based JOIN
  approach used elsewhere in the codebase rather than writing raw SQL.

- **Validate license values:** Add validation for the license parameter values. If any
  value is invalid (e.g., empty string after splitting), return a `400 Bad Request`
  using the `AppError` enum from `common/src/error.rs`.

- **Preserve existing behavior:** When the `license` parameter is absent (`None`), skip
  the JOIN and filter entirely so that the endpoint returns all packages unchanged (no
  regression).

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` with `fetch` and `list` methods. The `list` method
queries packages with pagination and sorting but has no license filter capability.

**Changes:**

- **Add license filter parameter to the `list` method:** Extend the method signature (or
  its options/query struct) to accept an optional license filter. Follow the same pattern
  used by `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
  for passing filter parameters from the endpoint handler to the service layer.

- **Apply filter in the query:** When a license filter is provided, use
  `common/src/db/query.rs::apply_filter` to apply the filter condition. JOIN through the
  `entity/src/package_license.rs` entity (the `package_license` SeaORM model) to filter
  packages by their associated license SPDX identifiers.

- **Return type unchanged:** The method continues to return
  `PaginatedResults<PackageSummary>` -- only the query logic changes internally.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test cases (following conventions from sibling test files `tests/api/advisory.rs` and
`tests/api/sbom.rs`):**

- **`test_package_list_filter_single_license`**: Verify that
  `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on
  specific package fields (not just count) to verify correct filtering. Use
  `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into
  `PaginatedResults<PackageSummary>`. Assert that every returned item's license field
  equals `"MIT"`.

- **`test_package_list_filter_multi_license`**: Verify that
  `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license.
  Assert that every returned item's license field is either `"MIT"` or `"Apache-2.0"`.
  Assert on specific values, not just the count.

- **`test_package_list_no_license_filter`**: Verify that `GET /api/v2/package` without
  the `license` parameter returns all packages unchanged (no regression). Compare against
  a known test dataset count and verify no filtering is applied.

- **`test_package_list_invalid_license`**: Verify that an invalid license value returns
  `400 Bad Request`. Assert `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.

**Test conventions to follow (from sibling analysis):**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- List endpoint tests validate `total_count`, `items.len()`, and at least one item's key fields
- Include error case test with appropriate status code assertion
- Follow `test_<endpoint>_<scenario>` naming pattern
- Each test function gets a `///` doc comment explaining what it verifies
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments

## Code Reuse Strategy

The implementation deliberately reuses three existing pieces of code rather than writing
new utilities:

1. **`common/src/db/query.rs::apply_filter`** -- Reuse directly for parsing the
   comma-separated `license` query parameter and generating the SQL `IN` clause. This
   function already handles both single-value and multi-value comma-separated inputs.
   No new parsing or filter-building utility functions should be created.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- Follow the same Query
   struct pattern with an optional filter field, the same handler flow for extracting
   and applying the filter, and the same error handling approach. The advisory endpoint's
   severity filter is structurally identical to the license filter needed here.

3. **`entity/src/package_license.rs`** -- Use this existing SeaORM entity for the JOIN
   query between packages and their licenses. No raw SQL or new entity definitions
   needed.

## Data Flow

```
HTTP Request (GET /api/v2/package?license=MIT,Apache-2.0)
  -> list.rs handler: extract Query { license: Some("MIT,Apache-2.0"), ... }
  -> apply_filter(): parse "MIT,Apache-2.0" -> vec!["MIT", "Apache-2.0"]
  -> PackageService::list(): build SeaORM query with JOIN on package_license entity
  -> SQL: SELECT ... FROM package JOIN package_license ON ... WHERE license IN ('MIT', 'Apache-2.0')
  -> PaginatedResults<PackageSummary> response (shape unchanged)
```

## Out of Scope

- No changes to the `PackageSummary` model or response shape
- No changes to other endpoints (`GET /api/v2/package/{id}`, etc.)
- No new utility functions that duplicate `apply_filter` functionality
- No changes to the `package_license` entity definition
- No migration changes
