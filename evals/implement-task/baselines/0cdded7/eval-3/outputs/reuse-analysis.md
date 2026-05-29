# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate identified in the task description is applied in the implementation, avoiding duplication of existing functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It accepts a raw string value (e.g., `"MIT,Apache-2.0"`), splits on commas, and produces the appropriate SeaORM condition -- a single `=` for one value, or an `IN (...)` clause for multiple values.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, when the `license` filter parameter is `Some`, `apply_filter` is called directly with the raw license string and the target column (the license identifier column from the `package_license` entity). This handles all parsing and SQL generation for both single-value and multi-value cases.

**What is NOT done**: No new utility function, helper, or custom parsing logic is written for splitting comma-separated values or building SQL filter conditions. The `apply_filter` function is the single source of truth for this behavior across the codebase, and the license filter reuses it identically to how other filters (e.g., the advisory severity filter) use it.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint (`GET /api/v2/advisory`) implements a `severity` query parameter using a Query struct pattern. The struct has an optional `severity: Option<String>` field, the handler extracts it from the query string, and passes it to the service layer. This is the established structural pattern for optional list filters in this codebase.

**How it is reused**: The implementation in `modules/fundamental/src/package/endpoints/list.rs` follows the identical structural pattern:

1. **Query struct**: Add a `license: Option<String>` field to the package list endpoint's query parameter struct, mirroring how `severity: Option<String>` is defined in the advisory list Query struct.
2. **Handler flow**: Extract the `license` field from the deserialized query struct and pass it to `PackageService::list()`, following the same data flow as the advisory handler passes `severity` to `AdvisoryService::list()`.
3. **Validation**: Apply the same validation pattern used for the severity field (rejecting empty values with a 400 status).

This is structural reuse -- the advisory endpoint serves as the template for how to add an optional filter parameter to any list endpoint in this codebase. No new patterns or abstractions are introduced.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity already defines the table schema, column enums, and relationships needed for querying the package-license association.

**How it is reused**: In `modules/fundamental/src/package/service/mod.rs`, the `package_license` entity is used to construct a SeaORM `.join()` call that connects the `package` table to the `package_license` table. The entity's `Column` enum provides the license identifier column used in the `apply_filter` call. The entity's `Relation` definitions provide the join condition.

**What is NOT done**:
- No raw SQL queries are written for the JOIN operation. The SeaORM entity and its relation definitions handle this declaratively.
- No new entity is created. The existing `package_license` entity in `entity/src/package_license.rs` already models this join table completely.
- No manual foreign key specifications are needed -- the entity's defined relations already encode the correct join semantics between `package` and `package_license`.

---

## Summary

All three Reuse Candidates are applied directly without modification. No new utility functions, entities, or parsing logic are introduced that would duplicate existing functionality. The implementation consists entirely of wiring existing infrastructure (the `apply_filter` helper, the advisory endpoint pattern, and the `package_license` entity) to support the new `license` query parameter.
