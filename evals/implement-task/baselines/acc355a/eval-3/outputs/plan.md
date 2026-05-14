# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The response shape (`PaginatedResults<PackageSummary>`) must remain unchanged.

---

## Files to Modify

### 1. modules/fundamental/src/package/endpoints/list.rs

**Purpose:** Add the `license` query parameter to the package list endpoint's query struct and wire it into the service call.

**Changes:**

- **Extend the `Query` struct** (or whatever the existing query-parameter extraction struct is named) with a new optional field:
  ```rust
  pub license: Option<String>,
  ```
  This follows the exact pattern used in `modules/fundamental/src/advisory/endpoints/list.rs` where the severity filter is declared as an optional `String` field on the advisory `Query` struct.

- **Pass the `license` field to `PackageService::list`** (or the equivalent service method) so the service layer can apply the filter. No parsing happens in the endpoint layer — the raw query string value (e.g., `"MIT,Apache-2.0"`) is forwarded as-is to the service, which delegates parsing to `apply_filter` from `common/src/db/query.rs`.

- **Validation:** If the endpoint layer performs input validation (as indicated by the 400 Bad Request acceptance criterion for invalid license values), add validation logic consistent with how the advisory endpoint validates its filter parameters. If validation is handled downstream by `apply_filter`, no additional code is needed here.

### 2. modules/fundamental/src/package/service/mod.rs

**Purpose:** Apply the license filter in the `PackageService` list method by joining through the `package_license` entity and using `apply_filter` for comma-separated value parsing.

**Changes:**

- **Accept the new `license: Option<String>` parameter** in the list method signature (or via the query struct passed into the method).

- **Conditionally join the `package_license` table** when a license filter is provided. Use the existing entity defined in `entity/src/package_license.rs` to construct the JOIN — do NOT write raw SQL or create a new entity. The join links the package table to the package_license table on the package ID foreign key.

- **Apply the filter using `common/src/db/query.rs::apply_filter`** to handle:
  - Parsing comma-separated values (e.g., `"MIT,Apache-2.0"` becomes `["MIT", "Apache-2.0"]`)
  - Generating the appropriate SQL `IN` clause for multi-value filters, or an `=` clause for single values
  
  This reuses the existing `apply_filter` function directly rather than writing any new parsing or filter-building logic. The advisory list endpoint's severity filter in `modules/fundamental/src/advisory/endpoints/list.rs` demonstrates this exact pattern.

- **Ensure no regression** when the `license` parameter is absent — the JOIN and filter must only be applied conditionally.

---

## Files to Create

### 3. tests/api/package_license_filter.rs

**Purpose:** Integration tests verifying the license filter behavior end-to-end.

**Test cases:**

1. **Single license filter** — `GET /api/v2/package?license=MIT`
   - Seed the database with packages having different licenses (MIT, Apache-2.0, GPL-3.0).
   - Assert that only packages with `MIT` license are returned.
   - Assert the response shape is `PaginatedResults<PackageSummary>` (unchanged).

2. **Comma-separated multi-value filter** — `GET /api/v2/package?license=MIT,Apache-2.0`
   - Assert that packages matching either `MIT` or `Apache-2.0` are returned.
   - Assert that packages with other licenses (e.g., GPL-3.0) are excluded.

3. **No license filter** — `GET /api/v2/package`
   - Assert that all packages are returned regardless of license.
   - This is a regression test to confirm the new parameter does not change default behavior.

4. **Invalid license value** — `GET /api/v2/package?license=!!!invalid`
   - Assert that the endpoint returns `400 Bad Request`.

**Structure:** Follow the existing integration test patterns in the `tests/api/` directory for setup, database seeding, HTTP client construction, and assertion style.

---

## Reuse Strategy

| Reuse Candidate | How It Is Used |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in `PackageService` to parse the comma-separated license string and generate the SQL filter clause. No new parsing logic is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Used as the structural template for the `Query` struct field addition and the endpoint-to-service wiring. The severity filter pattern is followed exactly. |
| `entity/src/package_license.rs` | Used to construct the JOIN between the package table and the license table in the service query. No raw SQL or new entities are created. |

---

## Constraints Adherence

- **5.1 (Scope):** All modified files (`list.rs`, `service/mod.rs`) and the created file (`package_license_filter.rs`) are within the task's declared Files to Modify / Files to Create sections.
- **5.4 (No duplication):** No new utility functions are created that duplicate `apply_filter` functionality. The existing `apply_filter` from `common/src/db/query.rs` is reused directly for all comma-separated multi-value query parameter parsing.
- Response shape is preserved — no fields are added or removed from `PaginatedResults<PackageSummary>`.
