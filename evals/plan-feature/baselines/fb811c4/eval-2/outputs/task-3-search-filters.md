## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow results by entity type, severity, and date range. This addresses the "add filters" requirement, which specifies "some kind of filtering capability" without further detail.

Assumption (pending clarification): The feature does not specify which filters to add. This task implements three filters based on the data model visible in the repository: entity type (sbom/advisory/package), advisory severity, and date range. Additional filters (e.g., license, package ecosystem) may be needed but are not included without explicit requirements.

Assumption (pending clarification): Filters are assumed to be combinable with AND logic (all filters must match). The feature does not specify AND vs OR semantics for combining filters.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameters for filters (entity_type, severity, date_from, date_to) to the GET /api/v2/search endpoint
- `modules/search/src/service/mod.rs` — Accept filter parameters in the search method and apply them to the database query
- `common/src/db/query.rs` — Add shared filter builder types for severity enum filtering and date range filtering

## Implementation Notes
In `modules/search/src/endpoints/mod.rs`:
- Add optional query parameters to the search endpoint handler: `entity_type` (enum: sbom, advisory, package), `severity` (string matching advisory severity values), `date_from` and `date_to` (ISO 8601 date strings)
- Parse and validate filter parameters, returning `AppError` for invalid values
- Pass validated filters to SearchService

In `modules/search/src/service/mod.rs`:
- Define a `SearchFilters` struct to encapsulate all filter parameters
- Modify the search query to apply WHERE clauses based on provided filters
- When `entity_type` is specified, restrict search to only that entity's table
- When `severity` is specified, filter advisory results by the severity field (from `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary)
- When date range is specified, filter by creation/modification timestamp

In `common/src/db/query.rs`:
- Add reusable filter types that can be applied to any query using the existing query builder pattern
- Ensure date range filters handle timezone-aware timestamps correctly

Assumption (pending clarification): Severity filter values are assumed to match whatever enum/string values are stored in the advisory entity's severity column (referenced in `entity/src/advisory.rs`). The actual valid values should be verified.

Per CONVENTIONS.md §Query helpers: Extend shared filtering infrastructure in `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the shared query helper convention.

Per CONVENTIONS.md §Endpoint registration: Register new query parameters in `modules/search/src/endpoints/mod.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the endpoint convention.

Per CONVENTIONS.md §Response types: Filtered results must still return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies search endpoint matching the response type convention.

Per CONVENTIONS.md §Error handling: Filter validation errors must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` and `modules/search/src/service/mod.rs` matching the error handling convention.

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type` query parameter to filter by entity type
- [ ] GET /api/v2/search accepts optional `severity` query parameter to filter advisory results by severity
- [ ] GET /api/v2/search accepts optional `date_from` and `date_to` query parameters for date range filtering
- [ ] All filter parameters are optional — omitting them returns unfiltered results (backward compatible)
- [ ] Multiple filters can be combined (AND logic) (note: AND semantics assumed, pending clarification)
- [ ] Invalid filter values return appropriate error responses
- [ ] Response format remains `PaginatedResults<T>`

## Test Requirements
- [ ] Integration test: search with entity_type filter returns only matching entity type
- [ ] Integration test: search with severity filter returns only advisories matching severity
- [ ] Integration test: search with date range returns only results within the range
- [ ] Integration test: search with combined filters applies all filters
- [ ] Integration test: search with no filters returns same results as before (backward compatibility)
- [ ] Integration test: invalid filter values return 400 error

## Dependencies
- Depends on: Task 1 — search-index-migration (B-tree indexes on severity and other filterable columns)

[sdlc-workflow] Description digest: sha256-md:de8d317f73cee21729fabb88960b7f993c7009075f536fa0d5ad12c8696fb182
