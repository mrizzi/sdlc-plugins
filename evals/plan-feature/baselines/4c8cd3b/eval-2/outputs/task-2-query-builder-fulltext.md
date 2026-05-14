## Repository
trustify-backend

## Target Branch
main

## Description
Extend the shared query builder in `common/src/db/query.rs` with full-text search filtering and relevance ranking utilities. This provides reusable query-building functions that the SearchService and individual entity list endpoints can use for full-text search with ts_rank scoring and filter parameter parsing.

## Files to Modify
- `common/src/db/query.rs` -- Add full-text search query helpers: a function to apply a `plainto_tsquery` filter against a tsvector column, a function to add `ts_rank` ordering, and filter parameter parsing for entity type, severity, license, and date range
- `common/src/db/mod.rs` -- Export new full-text search query symbols if needed

## Implementation Notes
- The existing `common/src/db/query.rs` already contains shared query builder helpers for filtering, pagination, and sorting. Add new functions alongside the existing ones, following the same patterns (function signatures returning query builder types, error handling with `AppError`).
- Implement a `apply_fulltext_filter` function that takes a SeaORM `SelectStatement` (or equivalent query builder), a search query string, and a column reference to the tsvector column, and appends a `WHERE search_vector @@ plainto_tsquery('english', $query)` condition.
- Implement an `add_relevance_ordering` function that adds `ORDER BY ts_rank(search_vector, plainto_tsquery('english', $query)) DESC` to the query, so results are sorted by relevance score.
- Implement filter parameter parsing functions for:
  - `entity_type` filter: accepts a comma-separated string of entity types (e.g., "sbom,advisory") and maps to the appropriate table(s)
  - `severity` filter: applies to advisory queries, filters by severity field on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`)
  - `license` filter: applies to package queries, filters by license field on `PackageSummary` (see `modules/fundamental/src/package/model/summary.rs`)
  - `date_from` / `date_to` filters: applies date range filtering on creation/modification timestamps
- All filter parameters should be optional -- when omitted, no filtering is applied (preserving backward compatibility).
- Follow the error handling pattern in `common/src/error.rs` -- return `Result<T, AppError>` and use `.context()` for error wrapping.
- Per constraints doc section 5.4: reuse existing query builder utilities in `common/src/db/query.rs` rather than duplicating pagination or sorting logic.

## Reuse Candidates
- `common/src/db/query.rs` -- existing filtering, pagination, and sorting helpers that should be extended rather than duplicated
- `common/src/model/paginated.rs::PaginatedResults<T>` -- the response wrapper that search results will be returned in
- `common/src/error.rs::AppError` -- the error enum that all query functions must use

## Acceptance Criteria
- [ ] `apply_fulltext_filter` function correctly appends tsvector matching conditions to queries
- [ ] `add_relevance_ordering` function correctly adds ts_rank-based ORDER BY clause
- [ ] Filter parameter parsing handles entity_type, severity, license, and date range filters
- [ ] All filter parameters are optional and omitting them preserves existing query behavior
- [ ] New functions follow the same patterns and return types as existing query builder helpers
- [ ] Error handling uses `AppError` with `.context()` wrapping

## Test Requirements
- [ ] Unit tests for `apply_fulltext_filter` verifying correct SQL generation with various query strings
- [ ] Unit tests for `add_relevance_ordering` verifying correct ORDER BY clause generation
- [ ] Unit tests for each filter parameter parser (entity_type, severity, license, date range)
- [ ] Test that omitting all filters produces an unmodified query (backward compatibility)
- [ ] Test that invalid filter values return appropriate `AppError` responses

## Dependencies
- Depends on: Task 1 -- Add full-text search migration (tsvector columns must exist for the query helpers to target)
