# Task 3: Extend Query Builder with Full-Text Search Helpers

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the shared query builder in `common/src/db/query.rs` with helper functions for PostgreSQL full-text search. These helpers will provide reusable building blocks for constructing `ts_query` expressions, applying `ts_rank` for relevance scoring, and integrating with the existing filtering and pagination infrastructure. This decouples the FTS logic from the search service, making it available to any module that needs text search.

**Ambiguity note:** The feature description says "results should be more relevant" but does not define a ranking algorithm. This task assumes PostgreSQL `ts_rank` with default weights is sufficient (pending clarification on whether custom weighting or boosting is needed).

## Files to Modify
- `common/src/db/query.rs` — Add full-text search helper functions: `apply_fts_filter` (adds `WHERE search_vector @@ to_tsquery(...)` clause), `apply_fts_ranking` (adds `ORDER BY ts_rank(...)` clause), and `parse_search_query` (converts user input to a `tsquery` string with sanitization)
- `common/src/db/mod.rs` — Export new FTS helper functions if needed

## Implementation Notes
- The existing `common/src/db/query.rs` already contains shared query builder helpers for filtering, pagination, and sorting. Add the FTS helpers alongside these existing functions to maintain the pattern.
- `parse_search_query` should sanitize user input to prevent tsquery syntax errors: strip special characters, split on whitespace, join with `&` (AND semantics) for multi-word queries.
- `apply_fts_filter` takes a SeaORM `SelectStatement` (or equivalent) and a search string, and appends a `WHERE search_vector @@ to_tsquery('english', ?)` condition.
- `apply_fts_ranking` adds `ts_rank(search_vector, to_tsquery('english', ?))` as a sort expression for relevance ordering.
- These may need to use SeaORM's `Expr::cust_with_values()` for raw SQL expressions since `tsvector` operations are not natively supported by SeaORM's query builder.
- Per CONVENTIONS.md: follow existing query builder patterns.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing filtering and pagination helpers to follow as structural examples
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints; FTS results should be compatible with this

## Acceptance Criteria
- [ ] `parse_search_query` correctly converts user input to a valid tsquery string
- [ ] `parse_search_query` handles edge cases: empty input, special characters, single words, multi-word phrases
- [ ] `apply_fts_filter` appends the correct `WHERE` clause to a SeaORM query
- [ ] `apply_fts_ranking` appends relevance-based ordering to a SeaORM query
- [ ] All helpers are exported from `common/src/db/mod.rs`
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit test: `parse_search_query` with various inputs (empty, single word, multiple words, special characters)
- [ ] Unit test: `apply_fts_filter` produces the expected SQL clause
- [ ] Unit test: `apply_fts_ranking` produces the expected ORDER BY clause

---

`[sdlc-workflow] Description digest: sha256-md:c4e8f2a6d1b73c9e5f0a2d4b8c6e1f3a7d9b2c4e6f8a0c2d4e6b8a1c3f5d7e9`
