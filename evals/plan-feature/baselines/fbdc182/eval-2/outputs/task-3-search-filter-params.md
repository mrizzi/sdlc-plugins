## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint to accept optional filter query parameters (`severity` and `license`), and update `SearchService` to apply those filters as additive (AND) predicates when present. This implements the "Add filters" MVP requirement from TC-9002.

**Assumptions pending clarification**:
- Filterable fields are `severity` (on advisory, matching `AdvisorySummary.severity` from `modules/fundamental/src/advisory/model/summary.rs`) and `license` (on package, matching `PackageSummary.license` from `modules/fundamental/src/package/model/summary.rs`). No other filter fields are assumed without further specification.
- Filter values are exact string matches (case-insensitive). Range-based or multi-value filter syntax is out of scope until specified.
- Filters are additive: `?severity=critical&license=Apache-2.0` means results must match BOTH conditions.
- If a filter narrows results to a single entity type (e.g. `?severity=critical` only applies to advisories), results for other entity types that don't carry that field are excluded from the filtered response. This behavior must be confirmed with the product owner.
- No frontend query parameter contract has been specified; the parameter names `severity` and `license` are chosen to match existing field names in the entity models.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add `severity: Option<String>` and `license: Option<String>` to the query parameter struct for `GET /api/v2/search`; pass them to `SearchService`
- `modules/search/src/service/mod.rs` — add filter predicate logic: when `severity` is `Some`, add `WHERE advisory.severity ILIKE $n` to advisory queries; when `license` is `Some`, add `WHERE package_license.license ILIKE $n` to package queries

## Implementation Notes
The endpoint handler in `modules/search/src/endpoints/mod.rs` uses Axum's `Query<T>` extractor. Add the filter fields to the existing query parameter struct (or create one if the current handler uses individual `Query<String>` extractors). Pattern:

```rust
#[derive(Debug, Deserialize)]
struct SearchQuery {
    q: String,
    limit: Option<u64>,
    offset: Option<u64>,
    severity: Option<String>,
    license: Option<String>,
}
```

In `SearchService`, extend the method signature to accept `severity: Option<&str>` and `license: Option<&str>`. Apply them as conditional SQL fragments appended to the WHERE clause of the relevant sub-query. Use parameterized values (not string interpolation) to avoid SQL injection — pass them as additional bind parameters in `Statement::from_sql_and_values`.

For the `severity` filter, join or reference the `advisory` table's `severity` column (see `entity/src/advisory.rs` for the SeaORM entity field name). For the `license` filter, join the `package_license` table (see `entity/src/package_license.rs`).

Use `common/src/db/query.rs` conventions for building the WHERE clause extensions, staying consistent with how the existing list endpoints in `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/package/endpoints/list.rs` handle optional filter parameters.

All errors from invalid filter values should surface as `AppError` variants from `common/src/error.rs`, not as 500s.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers; inspect for existing `filter_by` or `apply_filter` utilities before writing new predicate-building code
- `modules/fundamental/src/advisory/endpoints/list.rs` — reference for how optional filter query params are extracted and forwarded to the service layer in a list endpoint
- `modules/fundamental/src/package/endpoints/list.rs` — same pattern for package list with `license` field filtering
- `entity/src/advisory.rs` — SeaORM column names for `severity` field
- `entity/src/package_license.rs` — SeaORM entity for the package-to-license mapping, needed for the license filter join

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `severity=<string>` and `license=<string>`; when provided, results are filtered to entities matching those field values (AND logic); unrecognized filter values return an empty result set, not an error

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=log4j&severity=critical` returns only advisories with `severity = "critical"` matching the search query
- [ ] `GET /api/v2/search?q=curl&license=Apache-2.0` returns only packages with `license = "Apache-2.0"` matching the query
- [ ] `GET /api/v2/search?q=example` (no filters) continues to return results from all entity types, unchanged from Task 2 behavior
- [ ] `GET /api/v2/search?q=example&severity=nonexistent` returns an empty result set with HTTP 200, not an error
- [ ] The endpoint compiles and the project builds without warnings

## Test Requirements
- [ ] Add integration tests to `tests/api/search.rs` for each new filter parameter: seed the test database with known data, apply each filter, assert that only matching entities are returned
- [ ] Test that combining `severity` and `license` filters in one request applies both predicates
- [ ] Test that omitting a filter returns the same results as before this change (regression test)
- [ ] Test that an unknown filter value returns HTTP 200 with an empty result list, not HTTP 400 or 500

## Verification Commands
- `cargo test -p tests search` — all search integration tests (including new filter tests) pass
- `cargo build` — project compiles without warnings

## Documentation Updates
- `README.md` — update the API reference section (if present) to document the new `severity` and `license` query parameters on `GET /api/v2/search`

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use ranked full-text search (filter logic extends the refactored service)
