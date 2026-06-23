# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation follows the existing advisory severity filter pattern and reuses the shared `apply_filter` query helper.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` requests with pagination and sorting but no license filtering.

**Changes:**

- **Add `license` field to the `PackageListQuery` struct** (or equivalent query parameter struct): Add an `Option<String>` field named `license` to the query extraction struct. This mirrors the `severity` field in the advisory endpoint's query struct at `modules/fundamental/src/advisory/endpoints/list.rs`.

- **Extract and pass the license parameter to the service layer:** In the handler function, extract `query.license` and pass it to `PackageService::list()` as a new parameter. If `license` is `None`, no filtering is applied (preserving backward compatibility).

- **Validate the license parameter:** Before passing to the service, validate that any provided license values are non-empty strings. Return `400 Bad Request` (using `AppError`) for invalid/empty license values. Follow the existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService` has a `list` method that queries packages with pagination and sorting but no license filtering.

**Changes:**

- **Add license filter parameter to the `list` method signature:** Add an `Option<String>` parameter (or accept it via a query/filter struct) for the license filter.

- **Implement license filtering using `apply_filter` from `common/src/db/query.rs`:** When the license parameter is `Some`, call `apply_filter` to parse the comma-separated values and generate the appropriate SQL `IN` clause. This is the same function used by the advisory service for severity filtering.

- **Join through the `package_license` entity:** Use the `package_license` entity from `entity/src/package_license.rs` to join the package table with the license table. Apply the filter condition on the license SPDX identifier column via this join. Use SeaORM's relation/join API rather than raw SQL, consistent with existing query patterns in the codebase.

- **Preserve the existing return type:** The method must continue to return `PaginatedResults<PackageSummary>` — only the query logic changes, not the response shape.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Structure:** Follow the test conventions observed in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases
- Use `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` for error cases
- Validate response body by deserializing into `PaginatedResults<PackageSummary>`
- Assert on specific field values (license identifiers) rather than just collection lengths
- Follow `test_<endpoint>_<scenario>` naming convention
- Add `///` doc comments on every test function
- Use given-when-then section comments (`// Given`, `// When`, `// Then`) for non-trivial tests

**Test cases:**

1. **`test_list_packages_filter_single_license`** — Seed packages with MIT and Apache-2.0 licenses. Request `GET /api/v2/package?license=MIT`. Assert only MIT-licensed packages are returned. Verify returned items have `license == "MIT"`.

2. **`test_list_packages_filter_multiple_licenses`** — Seed packages with MIT, Apache-2.0, and GPL-3.0 licenses. Request `GET /api/v2/package?license=MIT,Apache-2.0`. Assert packages with MIT or Apache-2.0 are returned, but not GPL-3.0. Verify each returned item's license value.

3. **`test_list_packages_no_license_filter`** — Seed packages with various licenses. Request `GET /api/v2/package` (no license parameter). Assert all packages are returned. Verify the total count matches the seeded count.

4. **`test_list_packages_invalid_license_value`** — Request `GET /api/v2/package?license=` (empty value). Assert `400 Bad Request` is returned.

**Integration with test infrastructure:** The test file needs to be registered in `tests/api/` (add a `mod package_license_filter;` declaration if there is a `mod.rs` or ensure it is picked up by the test harness via `Cargo.toml` configuration in the `tests/` directory).

## Module Registration

No changes to `modules/fundamental/src/package/endpoints/mod.rs` or `server/src/main.rs` are needed — the endpoint path (`GET /api/v2/package`) already exists and is registered. The changes are additive to the existing handler (adding a query parameter), not a new route.

## API Changes

- `GET /api/v2/package` — MODIFY: add optional `license` query parameter
  - `?license=MIT` — filter to packages with MIT license (exact SPDX match)
  - `?license=MIT,Apache-2.0` — filter to packages matching any of the listed licenses
  - No `license` parameter — return all packages (existing behavior, no regression)
  - Empty/invalid `license` value — return `400 Bad Request`

The response shape `PaginatedResults<PackageSummary>` remains unchanged.

## Implementation Order

1. Modify `modules/fundamental/src/package/service/mod.rs` — add the filtering logic at the service layer first
2. Modify `modules/fundamental/src/package/endpoints/list.rs` — wire the query parameter to the service
3. Create `tests/api/package_license_filter.rs` — write and run integration tests
4. Run `cargo test` to verify all tests pass
5. Verify acceptance criteria
6. Self-verification checks (scope containment, duplication check, data-flow trace)
