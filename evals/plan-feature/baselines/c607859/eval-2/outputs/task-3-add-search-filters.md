# Task 3 — Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint to accept filter query parameters,
allowing users to narrow search results by entity type, severity, and date
range. This addresses the TC-9002 requirement "Add filters — Some kind of
filtering capability."

The filters should be applied in combination with the full-text search query
so that users can both search and filter simultaneously.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameter parsing
  to the `GET /api/v2/search` handler; pass filters to `SearchService`
- `modules/search/src/service/mod.rs` — extend search method signature to
  accept filter parameters and apply them as SQL WHERE clauses

## Files to Create
- `modules/search/src/model/mod.rs` — define `SearchFilters` struct with
  optional fields for entity type, severity, and date range
- `modules/search/src/model/` — (directory) search-specific models

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional): filter by entity type (`sbom`, `advisory`, `package`)
  - `severity` (string, optional): filter advisories by severity level
  - `date_from` (ISO 8601 date, optional): filter to entities created/modified after this date
  - `date_to` (ISO 8601 date, optional): filter to entities created/modified before this date

## Implementation Notes
- Parse filter parameters using Axum's `Query<SearchFilters>` extractor,
  following the pattern used in list endpoints (see
  `modules/fundamental/src/sbom/endpoints/list.rs` for the list SBOM handler
  and how it parses query parameters).
- Define `SearchFilters` as a struct with all fields as `Option<T>` so that
  filters are individually optional:
  ```
  pub struct SearchFilters {
      pub entity_type: Option<String>,
      pub severity: Option<String>,
      pub date_from: Option<chrono::NaiveDate>,
      pub date_to: Option<chrono::NaiveDate>,
  }
  ```
- Apply filters as additional SQL WHERE clauses on top of the full-text search
  query. Use the shared query builder in `common/src/db/query.rs` for filter
  composition if applicable.
- Entity type filter should restrict which tables are searched (e.g., if
  `entity_type=advisory`, only search the advisory table).
- Severity filter only applies when searching advisories — use the `severity`
  field on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- Date range filters apply to all entity types using their creation/modification
  timestamps.
- Maintain backward compatibility: when no filters are provided, the endpoint
  behaves exactly as before.
- Per constraints.md §5.1: changes must be scoped to the listed files.
- Per constraints.md §5.4: reuse existing filtering utilities from
  `common/src/db/query.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers;
  reuse for composing filter SQL clauses
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query
  parameter parsing pattern with Axum extractors
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary`
  struct with `severity` field; reference for filter values
- `common/src/model/paginated.rs` — `PaginatedResults<T>` for consistent
  response format

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` filters by date range
- [ ] Filters can be combined with text search query
- [ ] Multiple filters can be applied simultaneously
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Omitting all filters preserves existing behavior (backward compatible)

## Test Requirements
- [ ] Test entity type filter returns only matching entity types
- [ ] Test severity filter narrows advisory results correctly
- [ ] Test date range filter returns only results within the specified range
- [ ] Test combined filters (e.g., entity_type + severity + query)
- [ ] Test that no filters returns all results (backward compatibility)
- [ ] Test invalid filter values return 400 error
- [ ] Test edge cases: date_from > date_to, unknown entity type

## Dependencies
- Depends on: Task 2 — Implement Ranked Full-Text Search in SearchService
