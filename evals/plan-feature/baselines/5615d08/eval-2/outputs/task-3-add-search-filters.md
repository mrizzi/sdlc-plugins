## Repository
trustify-backend

## Description
Add filtering capabilities to the `GET /api/v2/search` endpoint so users can narrow search results by entity type, severity, and date range. The feature requirement says "add filters — some kind of filtering capability" but does not specify which fields are filterable, what filter types to support, or how filters combine (see Ambiguity A3 in impact-map.md). This task implements a concrete set of filters based on the existing entity model fields.

**Assumption (pending clarification):** The following filter dimensions are assumed based on fields available in the entity models. This should be validated with product before implementation:
- **Entity type filter**: filter results to only SBOMs, advisories, or packages (maps to the entity type returned by `SearchService`)
- **Severity filter**: filter advisory results by severity level (maps to the `severity` field in `entity/src/advisory.rs` / `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`)
- **Date range filter**: filter results by creation/modification date (maps to timestamp fields in entity tables)
- **Filter combination**: filters combine with AND logic (all specified filters must match)

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add optional query parameters for filters (`entity_type`, `severity`, `date_from`, `date_to`) to the `GET /api/v2/search` handler; deserialize and pass to `SearchService`
- `modules/search/src/service/mod.rs` — Accept filter parameters and apply them as WHERE clauses to the search query; integrate with the weighted scoring from Task 2
- `modules/search/src/lib.rs` — Re-export new filter types (e.g., `SearchFilters` struct) for use by the endpoint layer
- `common/src/db/query.rs` — Add reusable filter combinator methods (e.g., `apply_entity_type_filter`, `apply_date_range_filter`) that can be composed with existing filtering and pagination helpers

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional): one of `sbom`, `advisory`, `package`
  - `severity` (string, optional): severity level for advisory filtering (e.g., `critical`, `high`, `medium`, `low`)
  - `date_from` (ISO 8601 date, optional): include results created on or after this date
  - `date_to` (ISO 8601 date, optional): include results created on or before this date

## Implementation Notes
- The existing endpoint handler in `modules/search/src/endpoints/mod.rs` registers the `GET /api/v2/search` route. Add a query parameter struct (e.g., `SearchQuery`) using Axum's `Query<SearchQuery>` extractor. The struct should derive `Deserialize` with `serde` and use `Option<T>` for all filter fields to maintain backwards compatibility.
- The existing `apply_filtering` function in `common/src/db/query.rs` provides a pattern for applying filter conditions to SeaORM queries. Follow this pattern for the new filter methods. Use `Condition::all()` for AND combination of multiple filters.
- For the entity type filter, the `SearchService` likely queries multiple entity tables. The filter should control which tables are queried (skip query execution for excluded entity types) rather than filtering results after the fact, for performance.
- The severity filter applies only to advisory entities. When `severity` is specified without `entity_type=advisory`, it should implicitly restrict results to advisories only. Document this behavior in the endpoint.
- The date range filter should use indexed timestamp columns. Ensure the migration in Task 1 includes indexes on date columns if not already present.
- Reference the severity field in `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` to ensure the filter values match the domain model's severity representation.
- All new query parameters must be optional to preserve backwards compatibility (Ambiguity A4 / Assumption 4 in impact-map.md).

## Reuse Candidates
- `common/src/db/query.rs::apply_filtering` — Existing filtering helper; follow this pattern for new filter combinators
- `common/src/db/query.rs::apply_pagination` — Existing pagination helper; filters compose with pagination
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition; use to validate severity filter values

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters combine with AND logic (e.g., `entity_type=advisory&severity=high` returns only high-severity advisories)
- [ ] Omitting all filter parameters returns the same results as before (backwards compatible)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message using `AppError` from `common/src/error.rs`

## Test Requirements
- [ ] Integration test: filter by entity type returns only the specified type
- [ ] Integration test: filter by severity returns only matching advisories
- [ ] Integration test: filter by date range returns only results within the range
- [ ] Integration test: combined filters narrow results correctly
- [ ] Integration test: no filters returns all results (regression)
- [ ] Integration test: invalid filter value returns 400 error

## Dependencies
- Depends on: Task 1 — Optimize search query performance (indexes and query optimizations must be in place)
