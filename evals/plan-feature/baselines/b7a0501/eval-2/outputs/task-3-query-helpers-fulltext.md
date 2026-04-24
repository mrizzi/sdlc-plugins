# Task 3 — Extend Query Helpers with Full-Text Search and Filter Predicates

## Repository
trustify-backend

## Description
Extend the shared query builder helpers in `common/src/db/query.rs` to support PostgreSQL full-text search operations (`tsvector`/`tsquery` matching, relevance ranking via `ts_rank`) and new filter predicates (entity type, severity, date range, license). These shared helpers will be consumed by the `SearchService` to build efficient, ranked search queries with filtering.

## Files to Modify
- `common/src/db/query.rs` — Add full-text search query building functions (tsquery construction, ts_rank ordering) and filter predicate builders for severity, entity type, date range, and license

## Implementation Notes
- Follow the existing query builder helper patterns in `common/src/db/query.rs` — the file already has shared filtering, pagination, and sorting helpers
- Add a function to construct a `tsquery` from a user search string, handling:
  - Tokenizing the input into terms
  - Combining terms with `&` (AND) for multi-word queries
  - Sanitizing input to prevent SQL injection via `plainto_tsquery()` or `websearch_to_tsquery()` (preferred for natural language input)
- Add a function to apply `ts_rank(search_vector, tsquery)` as an ORDER BY clause for relevance ranking
- Add filter predicate builders:
  - `filter_by_entity_type(entity_type: &str)` — filter results to specific entity types (sbom, advisory, package)
  - `filter_by_severity(severity: &str)` — filter advisories by severity level
  - `filter_by_date_range(from: Option<DateTime>, to: Option<DateTime>)` — filter by creation/modification date
  - `filter_by_license(license: &str)` — filter packages by license
- Ensure all new helpers integrate with the existing `PaginatedResults<T>` pattern from `common/src/model/paginated.rs`
- Per constraints doc section 5.4: reuse existing filtering and pagination helpers rather than duplicating them

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering, pagination, and sorting — extend these rather than creating parallel implementations
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper that search results must use

## Acceptance Criteria
- [ ] Full-text search query builder function exists that constructs proper `tsquery` from user input
- [ ] Relevance ranking function applies `ts_rank` ordering to search queries
- [ ] Entity type filter predicate is implemented
- [ ] Severity filter predicate is implemented
- [ ] Date range filter predicate is implemented
- [ ] License filter predicate is implemented
- [ ] All helpers integrate with existing pagination and sorting infrastructure
- [ ] Input sanitization prevents SQL injection in search terms

## Test Requirements
- [ ] Unit tests for `tsquery` construction from various input patterns (single word, multi-word, special characters, empty string)
- [ ] Unit tests for each filter predicate builder
- [ ] Test that relevance ranking orders results correctly (exact match ranked higher than partial match)

## Dependencies
- Depends on: Task 1 — Add Database Migration for Search Indexes and Full-Text Search Support
