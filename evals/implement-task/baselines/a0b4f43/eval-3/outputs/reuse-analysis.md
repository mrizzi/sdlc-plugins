# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This analysis covers all three Reuse Candidates identified in the task description and explains how each is applied in the implementation plan.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. Given a raw string like `"MIT,Apache-2.0"`, it splits on commas, validates each segment, and produces the corresponding SeaORM filter condition with an `IN` clause.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method calls `apply_filter` directly with the raw `license` query parameter string. This handles all parsing and SQL generation for both single-value (`?license=MIT`) and multi-value (`?license=MIT,Apache-2.0`) cases.

**What is NOT done**: No new utility function is written for parsing comma-separated values. No custom string splitting, no manual SQL `IN` clause construction. The existing `apply_filter` function covers this requirement completely, and duplicating any part of its functionality would violate constraint 5.4 (no duplication of existing utilities).

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides**: The advisory list endpoint already implements a query parameter filter (`severity`) using the same structural pattern needed for the license filter. Specifically:
- A `Query` struct with an `Option<String>` field for the filter value, deserialized by Axum's `Query` extractor.
- The handler passes the optional value through to the corresponding service method.
- The service method conditionally applies the filter only when the value is `Some`.

**How it is reused**: The implementation in `modules/fundamental/src/package/endpoints/list.rs` follows this pattern exactly:
1. Add an `Option<String>` field named `license` to the package list endpoint's Query struct, mirroring how `severity` is declared in the advisory Query struct.
2. The handler extracts the value and passes it to `PackageService::list()` in the same way the advisory handler passes `severity` to `AdvisoryService::list()`.
3. The conditional application of the filter in the service layer follows the same `if let Some(value)` pattern.

This structural reuse ensures consistency across the codebase and avoids inventing a different approach for what is fundamentally the same kind of operation.

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package_license entity)

**What it provides**: The `package_license` SeaORM entity defines the mapping between packages and their declared licenses. It includes the table schema, column definitions, and SeaORM relation definitions that link it to the `package` table.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when building the filtered query, the service uses `entity::package_license::Entity` and its relation definitions to construct a JOIN from the `package` table to the `package_license` table. The filter condition produced by `apply_filter` is then applied to the license identifier column defined in this entity.

**What is NOT done**: No raw SQL JOIN statements are written. No new entity or model is created for the package-license relationship. The existing entity's SeaORM relations provide everything needed for the JOIN, keeping the implementation consistent with how other entity relationships are queried throughout the codebase.

---

## Summary

All three Reuse Candidates from the task description are applied directly. The implementation introduces zero new utility functions and zero new entities. The only new code is:
- A new field on an existing Query struct (following the advisory severity pattern)
- A new parameter on an existing service method with a conditional filter block (calling `apply_filter` and using `package_license` entity)
- Integration tests in a new test file
