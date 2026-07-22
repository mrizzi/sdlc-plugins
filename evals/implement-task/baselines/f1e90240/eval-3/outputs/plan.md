# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` that supports single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses the existing filter infrastructure already proven in the advisory module.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- Add an optional `license` field (type `Option<String>`) to the `Query` struct used for extracting query parameters from the request. This follows the exact same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, pass the extracted `license` value from the query struct down to `PackageService::list()`.
- Add input validation: if the `license` parameter is present but contains invalid values (e.g., empty segments after splitting on commas), return a `400 Bad Request` using the existing `AppError` enum from `common/src/error.rs`.

**How (reuse-based approach):**

- Mirror the `Query` struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs`. The advisory endpoint has an optional `severity` field that is structurally identical to the `license` field needed here. Copy the field declaration pattern, including any serde attributes.
- Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate the SQL `IN` clause. Do NOT write custom parsing or SQL generation logic.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- Modify the `list` method on `PackageService` to accept an optional `license` filter parameter (e.g., `license: Option<String>`).
- When the `license` parameter is `Some`, use the `apply_filter` helper from `common/src/db/query.rs` to build a filter condition. Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license SPDX identifiers.
- When the `license` parameter is `None`, the query remains unchanged (no regression).

**How (reuse-based approach):**

- Call `apply_filter` with the license value string. This function already handles: (a) splitting comma-separated values, (b) generating a SQL `IN` clause for multi-value, and (c) generating a simple equality check for single-value. No custom parsing needed.
- Use the SeaORM `package_license` entity from `entity/src/package_license.rs` to construct the JOIN between the `package` table and the `package_license` table. This avoids raw SQL and stays consistent with the project's SeaORM convention.
- Follow the same service-layer filter pattern used in `AdvisoryService` for severity filtering (in `modules/fundamental/src/advisory/service/advisory.rs`), adapting it for the license domain.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**What it contains:**

Integration tests for the license filter on `GET /api/v2/package`. Following the test conventions observed in sibling files (`tests/api/advisory.rs`, `tests/api/sbom.rs`):

- **Assertion style:** Use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization into `PaginatedResults<PackageSummary>`.
- **Response validation:** Validate `total_count`, `items.len()`, and assert on specific item field values (not just counts).
- **Test naming:** Follow `test_<endpoint>_<scenario>` pattern.
- **Documentation:** Every test function gets a `///` doc comment explaining what it verifies.
- **Structure:** Non-trivial tests use `// Given`, `// When`, `// Then` section comments.

**Test cases:**

1. `test_list_packages_filter_single_license` -- Verify `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on specific package names/identifiers in the response, not just the count.

2. `test_list_packages_filter_multiple_licenses` -- Verify `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that returned packages have either MIT or Apache-2.0 as their license.

3. `test_list_packages_no_license_filter` -- Verify `GET /api/v2/package` (no license parameter) returns all packages unchanged. Compare against a baseline count to confirm no regression.

4. `test_list_packages_invalid_license` -- Verify that an invalid license value returns `400 Bad Request`. Assert on `StatusCode::BAD_REQUEST`.

**Test module registration:** Add `mod package_license_filter;` to `tests/api/mod.rs` (or the appropriate test module file) so the new test file is included in the test suite. If `tests/api/` does not have a `mod.rs`, register it in `tests/Cargo.toml` or the top-level test harness as appropriate per sibling test conventions.

## Files NOT Modified (scope containment)

The following files are explicitly out of scope and will not be touched:

- `modules/fundamental/src/package/endpoints/mod.rs` -- Route registration does not need to change; the existing route for `GET /api/v2/package` already maps to `list.rs`. Only the handler and its query struct change.
- `modules/fundamental/src/package/model/summary.rs` -- The `PackageSummary` response struct already includes a `license` field. The response shape does not change.
- `entity/src/package_license.rs` -- Used as-is for the JOIN query; no modifications needed.
- `common/src/db/query.rs` -- The `apply_filter` function is used as-is; no modifications needed.
- Any OpenAPI or API documentation files -- The task description does not list them in Files to Modify or Files to Create.

## Implementation Sequence

1. Modify `modules/fundamental/src/package/service/mod.rs` first -- add the license filter parameter and query logic to the service layer.
2. Modify `modules/fundamental/src/package/endpoints/list.rs` -- add the query parameter to the handler's Query struct and pass it to the service.
3. Create `tests/api/package_license_filter.rs` -- write the integration tests.
4. Run `cargo test` to verify all tests pass.
5. Run any CI checks from CONVENTIONS.md (formatting, linting, clippy).
6. Verify acceptance criteria against the implementation.

## Data-Flow Trace

- `GET /api/v2/package?license=MIT` request arrives at the Axum handler in `list.rs`
- The handler extracts the `license` field from the `Query` struct (Axum query parameter extraction)
- The handler passes the license value to `PackageService::list()`
- The service calls `apply_filter()` from `common/src/db/query.rs` to parse the comma-separated value and build a SQL filter condition
- The service JOINs through `package_license` entity to match packages by license
- The query executes against PostgreSQL and returns matching rows
- Results are wrapped in `PaginatedResults<PackageSummary>` and returned as JSON
- **COMPLETE**: all stages connected from input to output

## Commit Message

```
feat(api): add license filter to GET /api/v2/package

Support single-value and comma-separated multi-value filtering
by SPDX license identifier on the package list endpoint.

Implements TC-9203
```
