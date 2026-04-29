# Task 3 — Add Filtering Parameters to Search Endpoint

## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint `GET /api/v2/search`, allowing users to narrow search results by entity type, severity level, date range, and license. This addresses the MVP requirement "Add filters — some kind of filtering capability" by providing structured, combinable filter parameters that work alongside the full-text search query.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameter parsing for new filter fields (entity_type, severity, date_from, date_to, license); pass parsed filters to `SearchService`
- `modules/search/src/service/mod.rs` — extend search query construction to apply filter predicates as additional WHERE clauses alongside the full-text search condition
- `common/src/db/query.rs` — add shared filter-parsing helpers for the new filter types (enum filter, date range filter) if they don't already exist, making them reusable by other endpoints

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional) — filter by entity type: `sbom`, `advisory`, `package`
  - `severity` (string, optional) — filter advisories by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - `date_from` (ISO 8601 date, optional) — filter results created/modified on or after this date
  - `date_to` (ISO 8601 date, optional) — filter results created/modified on or before this date
  - `license` (string, optional) — filter packages by license identifier

## Implementation Notes
- The existing `common/src/db/query.rs` provides shared query builder helpers for filtering, pagination, and sorting. Review these helpers first to understand the established filter pattern, then extend with new filter types as needed rather than implementing filters from scratch in the search module.
- For entity type filtering, this likely translates to adding a discriminator to the search query that limits which entity tables are searched (e.g., only search the advisory table if `entity_type=advisory`).
- For severity filtering, reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` which includes a severity field — the filter should match against this field.
- For license filtering, reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which includes a license field, and the `package_license` entity in `entity/src/package_license.rs`.
- For date range filtering, use standard SQL `>=` and `<=` comparisons on timestamp columns. Ensure the date parsing validates ISO 8601 format and returns `AppError` with a clear message for invalid dates.
- All filters should be optional and combinable (AND logic). When no filters are provided, behavior is unchanged from Task 2.
- Follow the existing endpoint pattern: Axum extractors for query parameters, `Result<T, AppError>` return type.
- Per constraints doc section 5 (Code Change Rules): inspect existing code before modifying, reuse existing utilities in `common/src/db/query.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers; extend with new filter types rather than duplicating filter logic
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with severity field; reference for severity filter values
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct with license field; reference for license filter values
- `entity/src/package_license.rs` — Package-License mapping entity; may be needed for license filter joins
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing list endpoint with filtering; reference for how filters are parsed and applied in the codebase

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=term&date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] `GET /api/v2/search?q=term&license=MIT` returns only packages with MIT license
- [ ] Multiple filters can be combined (AND logic)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] When no filters are provided, search behavior is unchanged from Task 2

## Test Requirements
- [ ] Integration test: entity_type filter returns only the specified entity type
- [ ] Integration test: severity filter returns only advisories matching the severity level
- [ ] Integration test: date range filter returns only results within the specified range
- [ ] Integration test: license filter returns only packages matching the license
- [ ] Integration test: combined filters (e.g., entity_type + severity) narrow results correctly
- [ ] Integration test: invalid filter value returns 400 status code
- [ ] Integration test: no filters provided returns all results (backward compatibility)

## Verification Commands
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Implement Relevance-Based Search Ranking in SearchService
