# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the GET /api/v2/search endpoint so users can narrow search results by entity type, severity, date range, and license. This addresses the MVP requirement "Add filters — some kind of filtering capability." Filters are implemented as optional query parameters that compose with the existing full-text search and pagination.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters (entity_type, severity, date_from, date_to, license) to the search handler; apply filters to the search query
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter criteria when building the search query
- `common/src/db/query.rs` — add shared filter builder helpers for date range and enum filtering if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `entity_type` (enum: sbom, advisory, package), `severity` (string, for advisories), `date_from` and `date_to` (ISO 8601 date strings), `license` (string, for packages). All parameters are optional; omitting them preserves current behavior.

## Implementation Notes
- Define a `SearchFilters` struct in the search module to deserialize filter query parameters using Axum's `Query` extractor. Use `Option<T>` for all fields since filters are optional.
- For `entity_type` filtering: when specified, restrict the search to only the matching entity table(s). When omitted, search across all entities (current behavior).
- For `severity` filtering: apply a WHERE clause on the advisory table's severity field. Only relevant when entity_type is `advisory` or unspecified.
- For date range filtering: use `>=` and `<=` comparisons on entity creation/publication timestamps. Reference how `common/src/db/query.rs` handles existing filtering patterns.
- For `license` filtering: apply a WHERE clause joining through the `package_license` entity. Only relevant when entity_type is `package` or unspecified.
- Follow the existing pattern in `common/src/db/query.rs` for building composable query filters. Use SeaORM's `Condition::all()` to chain multiple filter conditions.
- All filters must compose correctly with the full-text search from Task 2 and the pagination from `common/src/model/paginated.rs`.
- Per docs/constraints.md section 5 (Code Change Rules): do not duplicate existing filter logic in query.rs; reuse or extend existing helpers.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers that already implement filtering and pagination patterns; extend these rather than creating new filter logic in the search module
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct includes severity field; reference for severity filter values
- `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct includes license field; reference for license filter values
- `entity/src/package_license.rs` — Package-License mapping entity needed for license filtering joins

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional entity_type, severity, date_from, date_to, and license query parameters
- [ ] Each filter correctly narrows search results when provided
- [ ] Multiple filters compose correctly (AND logic)
- [ ] Omitting all filters preserves current search behavior (backward compatible)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOM results
- [ ] Integration test: filter by entity_type=advisory with severity returns only matching advisories
- [ ] Integration test: filter by date range returns only results within the range
- [ ] Integration test: combine multiple filters (e.g., entity_type + date range)
- [ ] Integration test: omitting all filters returns results from all entity types
- [ ] Integration test: invalid filter value returns 400 error

## Verification Commands
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Implement search result relevance ranking in SearchService
