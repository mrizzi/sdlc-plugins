## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search endpoint to support filter parameters, allowing users to narrow search results by entity type, date range, and severity. This addresses the MVP requirement for "some kind of filtering capability" by adding structured query parameters to `GET /api/v2/search` and integrating them into the search query pipeline.

## Files to Modify
- `modules/search/src/service/mod.rs` — add filter application logic to search queries, accepting filter parameters and constructing appropriate WHERE clauses
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter fields (entity_type, date_from, date_to, severity) and pass them to the SearchService
- `common/src/db/query.rs` — add shared filter builder helpers for date range and enum filtering if not already present

## Files to Create
- `modules/search/src/model/filter.rs` — define SearchFilters struct with optional fields: entity_type (enum: sbom, advisory, package), date_from (DateTime), date_to (DateTime), severity (Option<String>)

## API Changes
- `GET /api/v2/search` — MODIFY: add query parameters `entity_type` (optional, enum: sbom|advisory|package), `date_from` (optional, ISO 8601), `date_to` (optional, ISO 8601), `severity` (optional, string — applies only to advisory results)

## Implementation Notes
- Follow the existing query parameter extraction pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` and other list endpoints — use Axum's `Query<T>` extractor with serde deserialization
- Use the shared query builder helpers from `common/src/db/query.rs` for constructing filter conditions — extend the existing filter/pagination infrastructure rather than building a parallel system
- For `entity_type` filter: when specified, only search the tsvector column of the matching entity table; when not specified, search all three tables and union the results
- For `date_range` filter: apply a WHERE clause on the created/published date column, using `>=` for date_from and `<=` for date_to
- For `severity` filter: apply only to advisory results (use the severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`); ignore this filter for sbom and package results
- Validate that date_from <= date_to when both are provided; return 400 Bad Request if invalid
- All filter parameters are optional — when none are provided, behavior is identical to the unfiltered search

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering and pagination helpers; extend for date range and enum filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern with Axum
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct containing the severity field used for severity filtering

## Acceptance Criteria
- [ ] `entity_type` filter restricts results to the specified entity type
- [ ] `date_from` and `date_to` parameters filter results by creation/publication date
- [ ] `severity` filter applies to advisory results only and is ignored for other entity types
- [ ] All filters are optional and can be combined
- [ ] Invalid filter values (e.g., malformed dates, unknown entity types) return 400 Bad Request
- [ ] When no filters are applied, search behavior is unchanged from Task 2

## Test Requirements
- [ ] Test filtering by each entity type individually
- [ ] Test date range filtering with both bounds, only from, and only to
- [ ] Test severity filtering returns only matching advisories
- [ ] Test combining multiple filters simultaneously
- [ ] Test invalid filter values return 400 status codes
- [ ] Test that omitting all filters returns the same results as the unfiltered search

## Dependencies
- Depends on: Task 2 — Refactor SearchService for relevance ranking (builds on the refactored search pipeline)
