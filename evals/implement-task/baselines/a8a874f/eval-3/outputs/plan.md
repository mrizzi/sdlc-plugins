# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages
by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and
comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape
(`PaginatedResults<PackageSummary>`) remains unchanged.

## Target Repository

trustify-backend (Serena instance: `serena_backend`)

## Target Branch

main

## Branch Name

TC-9203

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** This file implements the `GET /api/v2/package` list endpoint handler.
It currently accepts pagination and sorting query parameters but has no license filtering.

**Changes:**

- **Add `license` field to the query parameter struct:** Following the pattern in
  `modules/fundamental/src/advisory/endpoints/list.rs` (which has a `severity` optional
  field on its query struct), add an `Option<String>` field named `license` to the
  existing query parameters struct used by the list handler. Apply the same
  deserialization attributes (e.g., `#[serde(default)]`) as the advisory endpoint's
  severity field.

- **Pass the license filter to the service layer:** In the handler function, extract
  `query.license` and pass it to `PackageService::list()` as an additional parameter.
  If the value is `None`, no filtering is applied (preserving backward compatibility).

- **Input validation:** Before passing to the service, validate that if a license value
  is provided, it is non-empty after splitting on commas. If validation fails, return a
  `400 Bad Request` using the existing `AppError` enum from `common/src/error.rs`.

**Reuse:** The query struct pattern is reused directly from the advisory list endpoint's
severity filter implementation. The same struct field pattern, serde attributes, and
extraction flow are followed.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` contains a `list` method that queries packages with
pagination and sorting but no license filtering.

**Changes:**

- **Add license filter parameter:** Extend the `list` method signature to accept an
  `Option<String>` for the license filter (or an `Option<Vec<String>>` after parsing).

- **Build the filter query:** When the license parameter is `Some`, use
  `common/src/db/query.rs::apply_filter` to parse the comma-separated string and
  generate a SQL `IN` clause. This function already handles splitting on commas and
  producing the correct SQL predicate for both single and multi-value inputs.

- **Join through `package_license` entity:** Use the SeaORM entity defined in
  `entity/src/package_license.rs` to join the `package` table with the
  `package_license` table. Apply the `IN` filter on the license identifier column
  of the `package_license` entity. This avoids writing raw SQL and stays within the
  SeaORM query builder pattern used throughout the codebase.

- **Preserve existing behavior:** When the license parameter is `None`, skip the join
  and filter entirely so that the query performance and results are unchanged for
  callers that do not use the new parameter.

**Reuse:** `apply_filter` from `common/src/db/query.rs` is reused directly for
comma-separated value parsing and SQL IN clause generation. The `package_license`
entity from `entity/src/package_license.rs` is reused for the join rather than
writing raw SQL.

---

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter on `GET /api/v2/package`.

**Test functions (following the `test_<endpoint>_<scenario>` naming convention from
sibling test files like `tests/api/advisory.rs`):**

1. **`test_list_packages_filter_single_license`**
   - Doc comment: `/// Verifies that filtering by a single license returns only packages with that license.`
   - Given: seed the test database with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT`
   - Then: assert response status is 200; assert all returned `PackageSummary` items have
     `license == "MIT"`; assert on specific package names/identifiers (value-based, not
     just count).

2. **`test_list_packages_filter_multiple_licenses`**
   - Doc comment: `/// Verifies that comma-separated license filter returns packages matching any of the listed licenses.`
   - Given: seed with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - When: `GET /api/v2/package?license=MIT,Apache-2.0`
   - Then: assert response status is 200; assert returned items have licenses that are
     either MIT or Apache-2.0; assert GPL-3.0 packages are excluded; assert on specific
     values.

3. **`test_list_packages_no_license_filter`**
   - Doc comment: `/// Verifies that omitting the license parameter returns all packages unchanged.`
   - Given: seed with packages having various licenses.
   - When: `GET /api/v2/package` (no license parameter)
   - Then: assert response status is 200; assert total count matches the full set of seeded
     packages.

4. **`test_list_packages_invalid_license`**
   - Doc comment: `/// Verifies that an invalid license value returns 400 Bad Request.`
   - Given: no special setup needed.
   - When: `GET /api/v2/package?license=` (empty string after parsing)
   - Then: assert response status is 400.

**Conventions followed:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests.
- Body deserialization into `PaginatedResults<PackageSummary>`.
- Validate `total_count`, `items.len()`, and at least one item's key fields.
- Include given-when-then section comments.
- Each test function has a doc comment.

**Integration with test suite:** Add `mod package_license_filter;` to `tests/api/mod.rs`
(or the test module root) so the test file is discovered by `cargo test`.

---

## Module Registration

No new routes are being added; only an additional query parameter is being accepted on the
existing `GET /api/v2/package` route. Therefore:
- No changes to `modules/fundamental/src/package/endpoints/mod.rs` route registration.
- No changes to `server/src/main.rs`.

---

## Data-Flow Trace

1. **Input:** HTTP request arrives at `GET /api/v2/package?license=MIT` ->
   Axum extracts query parameters including the new `license` field.
2. **Validation:** The handler validates the license value (non-empty after split) ->
   returns 400 if invalid.
3. **Processing:** Handler calls `PackageService::list()` with the license filter ->
   service uses `apply_filter` to build SQL IN clause -> joins through `package_license`
   entity -> executes query against PostgreSQL.
4. **Output:** Service returns `PaginatedResults<PackageSummary>` -> handler serializes
   as JSON response with status 200.

All stages are connected; no gaps in the data flow.

---

## Acceptance Criteria Verification Plan

| Criterion | How Verified |
|---|---|
| `?license=MIT` returns only MIT packages | Test `test_list_packages_filter_single_license` + manual trace through service layer |
| `?license=MIT,Apache-2.0` returns matching packages | Test `test_list_packages_filter_multiple_licenses` |
| No license parameter returns all packages | Test `test_list_packages_no_license_filter` |
| Response shape unchanged | Tests deserialize into `PaginatedResults<PackageSummary>` — would fail if shape changed |
| Invalid license returns 400 | Test `test_list_packages_invalid_license` |

---

## CI and Verification

- Run `cargo test` to verify all new and existing tests pass.
- Run `cargo clippy` and `cargo fmt --check` if listed in CONVENTIONS.md.
- Verify no new compiler warnings are introduced.

---

## Commit Plan

```
feat(api): add license filter to package list endpoint

Add optional `license` query parameter to GET /api/v2/package for
filtering packages by SPDX license identifier. Supports single-value
and comma-separated multi-value filtering using the existing
apply_filter utility.

Implements TC-9203
```

Trailer: `Assisted-by: Claude Code`

---

## PR Plan

- Base branch: `main`
- Head branch: `TC-9203`
- Title: `feat(api): add license filter to package list endpoint`
- Description includes: Implements [TC-9203](<jira-web-url>), summary of changes,
  test coverage summary.
