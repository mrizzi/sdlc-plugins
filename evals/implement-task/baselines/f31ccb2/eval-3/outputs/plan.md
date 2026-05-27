# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support both single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses existing query infrastructure and follows established filter patterns in the codebase.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose**: Add `license` query parameter extraction and pass it to the service layer.

**Changes**:
- Add a `license` field (type `Option<String>`) to the query parameter struct used by the list endpoint handler. This follows the same pattern as the severity filter field in `modules/fundamental/src/advisory/endpoints/list.rs`, where optional filter parameters are declared as `Option<String>` fields on the query/request struct.
- In the handler function, extract the `license` value from the query struct and pass it through to `PackageService::list()` (or the equivalent service method) as an additional parameter.
- No new parsing logic is needed here — the raw `Option<String>` value (e.g., `"MIT,Apache-2.0"`) is forwarded to the service layer, where `apply_filter` from `common/src/db/query.rs` handles comma-separated parsing and SQL clause generation.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose**: Apply the license filter to the database query in the PackageService list method.

**Changes**:
- Update the `list` method signature to accept the new `license: Option<String>` parameter (or accept it via an expanded options/filter struct, depending on the existing method signature pattern).
- When `license` is `Some(value)`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string and generate the appropriate SQL `IN` clause condition. This is the same function used by the advisory module for its severity filter — it handles splitting on commas, trimming whitespace, and producing the correct Sea-ORM / Diesel filter expression.
- Add a JOIN to the `package_license` table using the entity defined in `entity/src/package_license.rs`. The join links packages to their declared licenses via the join table, allowing filtering on the license SPDX identifier column.
- If the `license` parameter is `None`, no join or filter is applied, preserving the existing behavior of returning all packages.
- Add validation: if the license parameter is present but contains empty or invalid values after parsing, return a 400 Bad Request error using the existing `AppError` pattern with `.context()`.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose**: Integration tests verifying the license filter behavior end-to-end.

**Test cases**:

1. **Single license filter** — `GET /api/v2/package?license=MIT`
   - Seed the database with packages having different licenses (MIT, Apache-2.0, GPL-3.0).
   - Assert the response contains only packages with the MIT license.
   - Assert the response shape is `PaginatedResults<PackageSummary>` (unchanged).

2. **Comma-separated multi-value filter** — `GET /api/v2/package?license=MIT,Apache-2.0`
   - Seed the database with packages having MIT, Apache-2.0, and GPL-3.0 licenses.
   - Assert the response contains packages matching either MIT or Apache-2.0.
   - Assert GPL-3.0 packages are excluded.

3. **No license filter** — `GET /api/v2/package`
   - Seed the database with packages having various licenses.
   - Assert the response returns all packages (no filtering applied).
   - Verify the total count matches the expected number of seeded packages.

4. **Invalid license value** — `GET /api/v2/package?license=`
   - Send a request with an empty or malformed license value.
   - Assert a 400 Bad Request response is returned.

The test file will follow existing integration test patterns in the `tests/api/` directory, using the same test harness setup (database seeding, HTTP client, assertion helpers).

---

## Reuse Strategy

This implementation deliberately avoids creating any new utility functions for query parameter parsing or filter clause generation. All such logic is handled by reusing existing code:

| Reuse Candidate | How It Is Reused |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in the service layer to parse the comma-separated `license` string and generate the SQL `IN` clause. No new parsing logic is written. |
| `modules/fundamental/src/advisory/endpoints/list.rs` | The severity filter pattern (Query struct field, handler extraction, service delegation) is followed identically for the license filter. |
| `entity/src/package_license.rs` | The existing entity is used in the service layer JOIN query to connect packages to their license records. No new entity or migration is created. |

---

## Scope Boundaries

- No database migrations are needed — the `package_license` table and entity already exist.
- No changes to the response shape (`PaginatedResults<PackageSummary>`).
- No changes to other endpoints or modules.
- The filter is exact-match on SPDX identifier, not substring or fuzzy match.
