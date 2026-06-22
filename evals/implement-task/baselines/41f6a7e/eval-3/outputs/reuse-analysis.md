# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task's "Reuse Candidates" section identifies three existing code artifacts to reuse. This analysis details how each one is used in the implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates the appropriate SQL filter -- an equality condition for single values or an `IN (...)` clause for multiple values.

**How it is reused:** This function is called directly in `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) to process the `license` query parameter value. Instead of writing custom string-splitting logic or manual SQL condition building for the license filter, the implementation passes the raw license string to `apply_filter` along with the target column from the `package_license` entity.

**What is NOT done:** No new utility function is created for parsing comma-separated values or generating SQL filter clauses. The `apply_filter` function already provides this exact functionality, so creating a new helper would be pure duplication. The implementation reuses `apply_filter` as-is without wrapping or reimplementing it.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint implements a `severity` query parameter using a pattern that is structurally identical to what the license filter needs. Specifically:
- A Query struct with an optional field for the filter parameter (e.g., `severity: Option<String>`)
- Extraction of the filter value from the query struct in the handler function
- Forwarding the filter value to the service layer for database query construction

**How it is reused:** The implementation in `modules/fundamental/src/package/endpoints/list.rs` follows this same structural pattern exactly:
- The package endpoint's Query struct receives a new `license: Option<String>` field, mirroring how the advisory endpoint's Query struct declares `severity: Option<String>`
- The handler extracts `query.license` and passes it to the service method, exactly as the advisory handler extracts `query.severity`
- The overall request-handling flow (extract from query -> validate -> pass to service -> return paginated results) matches the advisory endpoint's approach

This is pattern reuse -- the advisory endpoint serves as the structural template, and the package endpoint follows the same architecture rather than inventing a new approach.

---

### 3. `entity/src/package_license.rs` (package_license entity)

**What it provides:** The existing SeaORM entity that maps the `package_license` database join table, which associates packages with their declared licenses. This entity defines the table columns, relations, and SeaORM model required for querying the package-license relationship.

**How it is reused:** In `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`), when the license filter is present, the implementation joins the `package` table with `package_license` using this existing entity and its defined relations. The join uses SeaORM's standard relation-based join API rather than writing raw SQL. The `apply_filter` function then applies the filter condition against the license column from this entity.

**What is NOT done:** No raw SQL join is written. No new entity or migration is created. The existing `package_license` entity already provides the complete schema definition needed for the filter join.

---

## Summary

| Reuse Candidate | Reuse Type | Location Used |
|---|---|---|
| `apply_filter` from `query.rs` | Direct function call | `modules/fundamental/src/package/service/mod.rs` |
| Severity filter pattern from advisory `list.rs` | Structural pattern (Query struct, handler flow) | `modules/fundamental/src/package/endpoints/list.rs` |
| `package_license` entity | SeaORM entity for JOIN query | `modules/fundamental/src/package/service/mod.rs` |

All three reuse candidates listed in the task are utilized. No new utility functions are created that would duplicate the functionality of `apply_filter` or any other existing shared code. The implementation follows established patterns rather than introducing new approaches.
