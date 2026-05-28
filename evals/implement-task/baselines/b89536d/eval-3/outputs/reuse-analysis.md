# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Summary

Three reuse candidates were identified in the task description. All three would be used directly during implementation, avoiding any duplication of existing logic.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source:** `common/src/db/query.rs`

**What it provides:**
- Parses comma-separated multi-value query parameter strings (e.g., `"MIT,Apache-2.0"`) into a vector of individual values
- Generates SQL `IN` clause for multi-value filters
- Handles single-value filtering as a degenerate case of multi-value (no special-casing needed)

**How it would be reused:**

The `apply_filter` function would be called directly in `modules/fundamental/src/package/service/mod.rs` within the `PackageService::list()` method. When the `license` query parameter is present (i.e., `Some(license_value)`), the service would call `apply_filter(query_builder, package_license::Column::License, &license_value)` to apply the filter condition to the SeaORM query.

This eliminates the need to:
- Write custom comma-separated string parsing logic
- Manually construct SQL `IN` clauses or `WHERE` conditions
- Handle the single-vs-multi value distinction

**Reuse type:** Direct invocation (no modification to `apply_filter` needed)

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**Source:** `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:**
- A structural template for adding an optional filter query parameter to a list endpoint
- The pattern includes: (1) adding an `Option<String>` field to the query struct, (2) passing it through the handler to the service layer, (3) applying it via `apply_filter` in the service

**How it would be reused:**

The advisory severity filter pattern would be replicated structurally in the package endpoint and service:

1. **Query struct pattern** -- In `modules/fundamental/src/package/endpoints/list.rs`, the existing query parameter struct would be extended with a `license: Option<String>` field, mirroring how `severity: Option<String>` is defined in the advisory list query struct.

2. **Handler plumbing** -- The handler function in `list.rs` would extract `query.license` and pass it to `PackageService::list()`, following the same flow as the advisory handler passes `query.severity` to `AdvisoryService::list()`.

3. **Service-layer filter application** -- In `modules/fundamental/src/package/service/mod.rs`, the `list` method would accept the license filter and conditionally apply it using `apply_filter`, following the same conditional pattern used in the advisory service for severity.

This is not a copy-paste reuse but a structural reuse: the advisory implementation serves as a proven reference architecture, and the package implementation follows the same design decisions and code organization.

**Reuse type:** Structural pattern replication (same architecture, different domain entity)

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source:** `entity/src/package_license.rs`

**What it provides:**
- A SeaORM entity definition for the `package_license` join table
- Maps the relationship between packages and their declared licenses
- Includes column definitions (at minimum `package_id` and `license`) and relation definitions to the `package` entity

**How it would be reused:**

The `package_license` entity would be used in `modules/fundamental/src/package/service/mod.rs` to build the database JOIN when applying the license filter:

1. **JOIN construction** -- When the `license` filter is present, the SeaORM query on the `package` entity would add a `.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())` (or equivalent) to join through the `package_license` table. This uses SeaORM's relation-based join API rather than raw SQL.

2. **Column reference for filtering** -- The `apply_filter` call would reference `package_license::Column::License` as the column to filter on, using the entity's typed column enum rather than a raw string.

This eliminates the need to:
- Write raw SQL `JOIN` statements
- Hardcode table or column names as strings
- Define new entity or model types for the join table

**Reuse type:** Direct entity usage (no modification to `package_license.rs` needed)

---

## Additional Reuse (discovered during analysis)

Beyond the three explicitly listed reuse candidates, the implementation would also reuse:

- **`common/src/model/paginated.rs::PaginatedResults<T>`** -- The response wrapper for list endpoints. The license filter changes the query but not the response shape, so `PaginatedResults<PackageSummary>` is used unchanged.

- **`common/src/error.rs::AppError`** -- The error type for returning 400 Bad Request on invalid license values. The existing `AppError` enum already includes variants for bad request errors, so no new error types are needed.

- **Axum `Query<T>` extractor** -- The framework-provided query parameter deserialization, which automatically handles the new `license` field added to the query struct. No custom deserialization logic needed.

---

## What is NOT reused (and why new code is necessary)

The following logic is genuinely new and cannot be reused from existing code:

1. **License-specific validation** -- While `apply_filter` handles parsing and SQL generation, validation of whether a license string is a valid SPDX identifier (if required) would need new validation logic. However, the task's acceptance criteria suggest exact-match filtering, so basic non-empty validation (reusing the `AppError` pattern) may suffice.

2. **Test fixtures** -- The integration tests need package fixture data seeded with known licenses. While the test setup pattern (database seeding, HTTP client creation) would follow sibling test conventions, the specific fixture data for license-bearing packages is new.

3. **The `license` field in the query struct** -- Adding the field itself is a one-line addition, but it is genuinely new code (not reusable from elsewhere).
