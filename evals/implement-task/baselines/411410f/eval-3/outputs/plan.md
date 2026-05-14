# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with existing query parameters (pagination, sorting) but no license filter.

**Changes:**
- Add an optional `license: Option<String>` field to the query parameter extraction struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- After extracting the query parameters, pass the `license` value to the `PackageService::list` method.
- Add input validation: if `license` is provided but contains invalid/empty segments after splitting on commas, return `400 Bad Request` via the `AppError` enum from `common/src/error.rs`.

**Reuse:** Follow the exact pattern used by the advisory list endpoint's `severity` query parameter struct. Use the same `Option<String>` field pattern and the same way it passes the filter value to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** Contains `PackageService` with `fetch` and `list` methods. The `list` method builds a query and returns `PaginatedResults<PackageSummary>`.

**Changes:**
- Add a `license: Option<String>` parameter to the `list` method signature (or add it to an existing query/filter struct if one is used).
- When the `license` parameter is present, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and generate a SQL `IN` clause.
- Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers. Use the SeaORM entity relation rather than raw SQL.
- When the `license` parameter is absent, the query remains unchanged (no regression).

**Reuse:**
- Call `apply_filter` from `common/src/db/query.rs` directly — it already handles comma-separated multi-value parsing and SQL `IN` clause generation.
- Use the `package_license` SeaORM entity for the JOIN — it already maps the package-license relationship.
- Follow the same filtering pattern used in `AdvisoryService` for the severity filter.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the `GET /api/v2/package` endpoint.

**Test cases (following the conventions from sibling test files `tests/api/advisory.rs`, `tests/api/sbom.rs`):**

1. **`test_list_packages_filter_single_license`** — Verify that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on specific package fields (not just count) to ensure correct filtering.

2. **`test_list_packages_filter_multi_license`** — Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that returned packages have one of the specified licenses.

3. **`test_list_packages_no_license_filter`** — Verify that `GET /api/v2/package` without a license parameter returns all packages unchanged. Compare against a known test dataset to confirm no regression.

4. **`test_list_packages_invalid_license`** — Verify that an invalid license value returns `400 Bad Request`. Assert on `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions to follow (from sibling test analysis):**
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Deserialize response body and validate `total_count`, `items.len()`, and key fields of returned items
- Use real PostgreSQL test database (integration test pattern)
- Follow `test_<endpoint>_<scenario>` naming pattern
- Add `///` doc comments before each test function
- Use given-when-then section comments (`// Given`, `// When`, `// Then`) for non-trivial tests

**Module registration:** Add `mod package_license_filter;` to `tests/api/` module file (or `tests/Cargo.toml` test entries) so the new test file is discovered.

## Files NOT Modified (scope containment)

The following files are explicitly out of scope:
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` already includes a `license` field; no changes needed
- `modules/fundamental/src/package/endpoints/mod.rs` — route registration does not change (same `GET /api/v2/package` endpoint, just new query param)
- `entity/src/package_license.rs` — used as-is for the JOIN, no modifications needed
- `common/src/db/query.rs` — `apply_filter` is reused directly, no modifications needed
- `server/src/main.rs` — no new routes or modules to mount

## Data-Flow Trace

```
Request: GET /api/v2/package?license=MIT,Apache-2.0
  → Endpoint handler (list.rs): extract license query param ✓
  → Validate license values ✓
  → Pass to PackageService::list() ✓
  → apply_filter() parses comma-separated values into Vec ✓
  → SeaORM query JOINs package_license table ✓
  → Filter with IN clause on license SPDX identifier ✓
  → Return PaginatedResults<PackageSummary> (shape unchanged) ✓
```

**COMPLETE** — all stages connected from input to output.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` — add the license filter to the service layer first (the foundational change)
2. Modify `modules/fundamental/src/package/endpoints/list.rs` — add query parameter extraction, validation, and wire it to the service
3. Create `tests/api/package_license_filter.rs` — write and run integration tests
4. Run `cargo test` to verify all tests pass (existing + new)
5. Verify acceptance criteria against the test results
6. Self-verification: scope containment, sensitive-pattern check, duplication check
