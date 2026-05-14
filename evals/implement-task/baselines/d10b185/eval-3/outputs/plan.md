# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) remains unchanged.

## Target Branch

main

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add `license` query parameter extraction and pass it to the service layer.

**Changes**:
- Add an optional `license: Option<String>` field to the `Query` struct (the query-parameter extraction struct for the list endpoint). This follows the identical pattern used in `modules/fundamental/src/advisory/endpoints/list.rs`, where the `severity` query parameter is declared as an optional field on the advisory list Query struct.
- In the handler function, pass the extracted `license` value to `PackageService::list()` so the service layer can apply the filter.
- Add input validation: if the `license` parameter is present but contains empty or whitespace-only segments after splitting on commas, return a `400 Bad Request` via `AppError`.

**Reuse**:
- Mirror the Query struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (Reuse Candidate). The advisory endpoint's `severity` optional field and how it is threaded into the service call is structurally identical to what is needed here for `license`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Accept the license filter in `PackageService::list()` and apply it to the database query.

**Changes**:
- Update the `list` method signature to accept an additional parameter: `license: Option<String>`.
- When `license` is `Some(value)`, call `apply_filter` from `common/src/db/query.rs` (Reuse Candidate), passing the raw comma-separated string. `apply_filter` handles splitting the string on commas and generating a SQL `IN` clause.
- The filter must JOIN through the `package_license` entity (`entity/src/package_license.rs`, Reuse Candidate) to match packages whose associated license SPDX identifier is in the provided set. Use SeaORM's relation-based join via the `package_license` entity rather than writing raw SQL.
- When `license` is `None`, skip the join and filter entirely, preserving existing behavior (no regression).

**Reuse**:
- `common/src/db/query.rs::apply_filter` -- reuse directly for comma-separated parsing and SQL IN clause generation. Do NOT create a new parsing or filtering utility.
- `entity/src/package_license.rs` -- use the existing SeaORM entity for the package-license join table. Do NOT write raw SQL joins.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests for the new license filter on the package list endpoint.

**Changes**:
- Follow the test conventions observed in existing files such as `tests/api/advisory.rs` and `tests/api/sbom.rs`: hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` pattern, and set up test data via ingestion helpers.
- Implement the following test cases:

  1. **`test_single_license_filter`**: Insert test packages with distinct licenses (e.g., MIT, Apache-2.0, GPL-3.0). Call `GET /api/v2/package?license=MIT`. Assert only MIT-licensed packages are returned. Verify `PaginatedResults` shape is intact.

  2. **`test_multi_license_filter`**: Call `GET /api/v2/package?license=MIT,Apache-2.0`. Assert packages with either MIT or Apache-2.0 are returned. Assert GPL-3.0 packages are excluded.

  3. **`test_no_license_filter`**: Call `GET /api/v2/package` with no `license` parameter. Assert all packages are returned (no regression).

  4. **`test_invalid_license_value`**: Call `GET /api/v2/package?license=` (empty string) or `GET /api/v2/package?license=,,,`. Assert `400 Bad Request` is returned.

- Register this test file in `tests/Cargo.toml` if the test harness requires explicit registration (follow existing pattern from other test files like `sbom.rs`).

---

## Implementation Order

1. **Modify service layer** (`modules/fundamental/src/package/service/mod.rs`) -- add the license filter logic using `apply_filter` and the `package_license` entity join. This is the core data-access change.
2. **Modify endpoint** (`modules/fundamental/src/package/endpoints/list.rs`) -- add the `license` field to the Query struct, add validation, and pass the value to the updated service method.
3. **Create integration tests** (`tests/api/package_license_filter.rs`) -- write and run all four test cases.
4. **Verify** -- run the full test suite to confirm no regressions and all new tests pass.

## Scope Boundary

No other files are modified or created. Specifically:
- `common/src/db/query.rs` is reused as-is; no changes needed.
- `entity/src/package_license.rs` is reused as-is; no changes needed.
- The response type `PaginatedResults<PackageSummary>` is unchanged.
- Route registration in `modules/fundamental/src/package/endpoints/mod.rs` does not need changes since the list handler already exists; we are only adding a query parameter to it.
