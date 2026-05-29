## Repository
trustify-backend

## Target Branch
main

## Description
Extend the shared query builder module with reusable helpers for full-text search queries and filter composition. These helpers will be used by the SearchService (Task 2) and the filter implementation (Task 4) to construct search queries consistently. This prevents duplication of query-building logic across modules and follows the existing pattern of shared query utilities.

## Files to Modify
- `common/src/db/query.rs` — add full-text search helper functions: `apply_fulltext_filter()` for tsvector/tsquery matching, `apply_relevance_sort()` for ts_rank ordering, and generic filter composition helpers for combining multiple filter predicates with AND logic

## Implementation Notes
- The existing `common/src/db/query.rs` already contains shared query builder helpers for filtering, pagination, and sorting — inspect the current code to understand the existing patterns and extend them rather than creating parallel abstractions
- Add a `apply_fulltext_filter(query, search_term, vector_column)` helper that wraps the `to_tsquery`/`plainto_tsquery` construction and `@@` operator application
- Add a `apply_relevance_sort(query, vector_column, search_term)` helper that adds `ORDER BY ts_rank_cd(vector_column, to_tsquery(search_term)) DESC`
- Add a `apply_filter(query, column, value)` generic filter helper and a `compose_filters(filters)` combinator that applies multiple filters with AND semantics
- Follow the existing function signatures and return types in `query.rs` — all helpers should be generic over the query builder type used by SeaORM
- Ensure helpers handle edge cases: empty search terms (skip filter), special characters in search input (sanitize for tsquery), and NULL column values
- Per docs/constraints.md §5.4: this task specifically creates shared utilities to prevent duplication across the search and filter features
- Per docs/constraints.md §2 (Commit Rules): use Conventional Commits format with Jira issue ID in footer

## Reuse Candidates
- `common/src/db/query.rs` — the target file itself; existing filtering, pagination, and sorting helpers serve as the pattern to follow for the new full-text search helpers
- `common/src/db/limiter.rs` — connection pool limiter; review for any query-level patterns that should be respected

## Acceptance Criteria
- [ ] `apply_fulltext_filter()` correctly applies tsvector/tsquery matching to a query
- [ ] `apply_relevance_sort()` correctly orders results by ts_rank_cd score
- [ ] Filter composition helpers combine multiple predicates with AND logic
- [ ] Helpers handle edge cases (empty search terms, special characters, NULL values)
- [ ] Existing query builder usage across the codebase is not broken

## Test Requirements
- [ ] Unit test: `apply_fulltext_filter` produces correct SQL with a valid search term
- [ ] Unit test: `apply_fulltext_filter` skips filter when search term is empty
- [ ] Unit test: filter composition combines multiple filters with AND
- [ ] All existing tests pass (no regression from modifying `query.rs`)

## Verification Commands
- `cargo test -p common` — common crate unit tests pass
- `cargo test --test api` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (helpers reference tsvector column types)

[sdlc-workflow] Description digest: sha256:964da82c2cab1b1e0d0e96bfa346685f1c477a8f7e5895f5c42aa2bed24eb6d0
