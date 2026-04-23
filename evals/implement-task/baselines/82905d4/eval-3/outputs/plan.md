# Implementation Plan -- TC-9203: Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing infrastructure throughout: the `apply_filter` function for query parameter parsing, the advisory severity filter as a structural template, and the `package_license` entity for the JOIN.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- **Add a `license` field to the query/params struct:** Following the same pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`, add an `Option<String>` field named `license` to the existing query parameter struct (e.g., `PackageQuery` or equivalent). This field captures the raw query string value from the `?license=...` parameter.

- **Pass the license parameter to the service layer:** In the list handler function, extract `query.license` and pass it through to `PackageService`'s list method. This mirrors exactly how the advisory list endpoint extracts the severity parameter and forwards it to its service layer.

- **No new parsing logic:** The raw comma-separated string is passed as-is to the service layer, where `apply_filter` from `common/src/db/query.rs` handles all parsing and SQL generation. The endpoint layer does not split commas or validate license values -- that responsibility belongs to the shared `apply_filter` utility.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- **Accept the license filter parameter:** Modify the `PackageService` list method signature to accept an optional license filter parameter (e.g., `license: Option<String>`).

- **Build a JOIN through `package_license` entity:** When the `license` parameter is present, add a JOIN from the package table to the `package_license` table (using the entity defined in `entity/src/package_license.rs`). This uses SeaORM's relation/join API with the existing entity rather than writing raw SQL.

- **Apply the filter using `apply_filter`:** Call `common::db::query::apply_filter` (or the equivalent shared filtering function) to handle the comma-separated license string. `apply_filter` parses the comma-delimited value into individual terms and generates the appropriate SQL `IN` clause (or equality check for single values). This is the same function used by the advisory severity filter, so the behavior is identical: single values produce `WHERE license = ?`, comma-separated values produce `WHERE license IN (?, ?, ...)`.

- **Return 400 on invalid input:** If `apply_filter` or the validation layer rejects the license values (e.g., empty string after comma splitting), return a 400 Bad Request. Follow the same error handling pattern used by the advisory severity filter.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**What it contains:**

Integration tests for the license filter on `GET /api/v2/package`. Each test function will have a doc comment and, where non-trivial, given-when-then inline comments.

**Test cases:**

1. **`test_filter_single_license`** -- Verify that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Seeds the database with packages having different licenses, queries with a single license value, and asserts only matching packages are returned (value-based assertions on package fields, not just count).

2. **`test_filter_comma_separated_licenses`** -- Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Seeds packages with MIT, Apache-2.0, and GPL-3.0, queries with the comma-separated parameter, and asserts that MIT and Apache-2.0 packages appear while GPL-3.0 does not.

3. **`test_no_license_filter_returns_all`** -- Verify that `GET /api/v2/package` (no license parameter) returns all packages without regression. Seeds the database and queries without the license parameter, asserting the full set is returned.

4. **`test_invalid_license_returns_400`** -- Verify that an invalid license value results in a 400 Bad Request response. Sends a request with an invalid/malformed license parameter and asserts the response status code is 400.

**Conventions to follow:**
- Match sibling test files in `tests/api/` for assertion style, setup/teardown patterns, and naming conventions.
- Use the same test infrastructure (test server setup, database seeding, HTTP client) as other integration tests in the directory.
- Use doc comments on every test function.
- Use given-when-then comments on non-trivial tests (tests 1, 2, and 3).

---

## Reuse Strategy

This implementation is built entirely on existing infrastructure with zero new utility functions:

| Reuse Candidate | How It Is Reused |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in the service layer to parse comma-separated license values and generate SQL `IN` clauses. No new parsing or SQL generation code is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as the structural template: the `license` field is added to the query struct following the same `Option<String>` pattern as `severity`; the handler passes it to the service in the same way. |
| `entity/src/package_license.rs` | Used for the JOIN query in the service layer via SeaORM relations. No raw SQL or new entity definitions are created. |

No new utility functions, parsing helpers, or entity definitions are introduced. The only new code is the glue that connects the query parameter to the existing filtering infrastructure.
