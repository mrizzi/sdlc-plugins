## Repository
trustify-backend

## Target Branch
main

## Description
Update the SearchService to use full-text search with relevance ranking and filtering. Replace or augment the existing search implementation with PostgreSQL tsvector-based full-text search, ts_rank-based relevance scoring, and support for the new filter parameters (entity type, severity, license, date range). This is the core backend logic change that makes search faster and more relevant.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Refactor `SearchService` to use the new full-text search query helpers from `common/src/db/query.rs` for tsvector matching, ts_rank ordering, and filter application across SBOM, advisory, and package entities
- `modules/search/src/endpoints/mod.rs` -- Update the `GET /api/v2/search` endpoint handler to accept new optional query parameters for filtering (entity_type, severity, license, date_from, date_to) and pass them to the SearchService

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters: `entity_type` (comma-separated: sbom, advisory, package), `severity` (string), `license` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). Response shape remains `PaginatedResults<T>` but results are now ordered by relevance score when a search query is provided.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Modify it to:
  1. Use `apply_fulltext_filter` from `common/src/db/query.rs` to filter against the `search_vector` tsvector column instead of any existing LIKE/ILIKE queries.
  2. Use `add_relevance_ordering` from `common/src/db/query.rs` to sort results by `ts_rank` score when a search query is provided.
  3. Apply entity type filtering to restrict results to specific entity types when the `entity_type` parameter is provided.
  4. Apply severity, license, and date range filters using the filter parameter parsers from `common/src/db/query.rs`.
- In `modules/search/src/endpoints/mod.rs`, update the handler to deserialize the new optional query parameters from the URL. Follow the existing endpoint pattern: use Axum extractors for query parameters and return `Result<Json<PaginatedResults<SearchResult>>, AppError>`.
- When no search query is provided (empty `q` parameter), fall back to listing all entities with optional filtering but without relevance ordering (use default sort order).
- Preserve backward compatibility: existing API calls without the new filter parameters must return the same results as before (minus the ordering change from relevance ranking).
- Follow the endpoint registration pattern in `modules/search/src/endpoints/mod.rs` for route setup.
- Follow the caching pattern from the Key Conventions: configure `tower-http` caching middleware appropriately for search results (short TTL or no cache for personalized/filtered results).
- Per constraints doc section 5.1: keep changes scoped to the search module files listed above.

## Reuse Candidates
- `common/src/db/query.rs` -- full-text search helpers added in Task 2 (apply_fulltext_filter, add_relevance_ordering, filter parsers)
- `common/src/model/paginated.rs::PaginatedResults<T>` -- existing response wrapper to use for search results
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- existing service pattern showing how to build filtered queries against entities with SeaORM
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of a list endpoint with query parameter extraction and pagination

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsvector/tsquery) instead of LIKE/ILIKE
- [ ] Search results are ordered by ts_rank relevance score when a search query is provided
- [ ] Entity type filter correctly restricts results to specified entity types
- [ ] Severity filter correctly filters advisory results by severity
- [ ] License filter correctly filters package results by license
- [ ] Date range filters correctly restrict results by creation/modification date
- [ ] All filter parameters are optional -- omitting them returns unfiltered results
- [ ] Response shape remains `PaginatedResults<T>` (backward compatible)
- [ ] Existing search API calls without new parameters continue to work

## Test Requirements
- [ ] Integration test: search with a query string returns results ordered by relevance (verify ordering)
- [ ] Integration test: search with entity_type=sbom returns only SBOM results
- [ ] Integration test: search with entity_type=advisory returns only advisory results
- [ ] Integration test: search with severity filter returns only advisories matching the severity
- [ ] Integration test: search with license filter returns only packages matching the license
- [ ] Integration test: search with date_from and date_to returns only results within the date range
- [ ] Integration test: search with multiple filters combined returns correct intersection of results
- [ ] Integration test: search without any filters returns all entity types (backward compatibility)
- [ ] Integration test: empty search query with filters returns filtered results without relevance ordering

## Dependencies
- Depends on: Task 1 -- Add full-text search migration (tsvector columns and GIN indexes must exist)
- Depends on: Task 2 -- Extend query builder with full-text search support (query helpers must be available)
