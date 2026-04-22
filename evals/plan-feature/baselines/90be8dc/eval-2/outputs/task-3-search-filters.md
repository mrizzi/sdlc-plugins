## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`). Users will be able to narrow search results by entity type, date range, and severity. This addresses the "Add filters" requirement. All filter parameters are optional and combinable using AND logic, preserving backward compatibility with existing API consumers.

**Assumption pending clarification:** The specific filter fields (entity type, date range, severity) are assumed based on the data model. The product owner should confirm which filters are needed for MVP and whether additional filters (e.g., license, package name) are required.

## Files to Create
- `modules/search/src/service/filter.rs` — Filter struct definitions and logic for parsing filter parameters and applying them as SQL WHERE clauses

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add optional query parameters to `GET /api/v2/search`: `type` (enum: sbom/advisory/package), `severity` (string), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)
- `modules/search/src/service/mod.rs` — Integrate filter application into the search query pipeline, calling filter logic after full-text matching
- `modules/search/src/lib.rs` — Register the new `filter` submodule

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `type` (filters by entity type: sbom, advisory, package), `severity` (filters advisories by severity level), `created_after` (ISO 8601 datetime, inclusive), `created_before` (ISO 8601 datetime, inclusive). All parameters are optional. When omitted, no filtering is applied (backward compatible).

## Implementation Notes
Follow the endpoint registration pattern in `modules/search/src/endpoints/mod.rs` and the query helper patterns in `common/src/db/query.rs`:

1. Define a `SearchFilters` struct in `modules/search/src/service/filter.rs` with optional fields: `entity_type: Option<EntityType>`, `severity: Option<String>`, `created_after: Option<DateTime>`, `created_before: Option<DateTime>`.
2. In the endpoint handler in `modules/search/src/endpoints/mod.rs`, deserialize filter parameters from query string using Axum's `Query<SearchFilters>` extractor.
3. In `modules/search/src/service/mod.rs`, apply filters as additional WHERE clauses on the search query. Use the shared filtering helpers from `common/src/db/query.rs` for pagination and sorting.
4. The `severity` filter only applies when searching advisories (the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field).
5. The `type` filter restricts which entity tables are queried.
6. Date filters apply to the creation timestamp of each entity.
7. Invalid filter values should return a 400 Bad Request with a descriptive error message via `AppError`.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; extend or reuse for search-specific filters
- `common/src/error.rs::AppError` — Error handling for invalid filter parameters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field structure

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=term&created_after=2024-01-01T00:00:00Z` returns only results created after that date
- [ ] Filters are combinable: `type=sbom&created_after=...` applies both filters
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return 400 Bad Request with descriptive error message

## Test Requirements
- [ ] Filtering by entity type returns only results of that type
- [ ] Filtering by severity returns only matching advisories
- [ ] Date range filtering works correctly for both `created_after` and `created_before`
- [ ] Combining multiple filters applies AND logic
- [ ] Omitting filters returns the same results as before (regression test)
- [ ] Invalid filter values produce a 400 error response

## Verification Commands
- `cargo test -p search` — All search tests pass
- `cargo clippy -p search` — No linting warnings

## Dependencies
- Depends on: Task 2 — Implement relevance-ranked search in SearchService
