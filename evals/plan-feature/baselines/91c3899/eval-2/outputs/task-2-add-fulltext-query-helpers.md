## Repository
trustify-backend

## Target Branch
main

## Description
Add shared query builder helpers for PostgreSQL full-text search and filtering to the common module. These helpers will be consumed by the search service to construct weighted `ts_query` searches and apply filter predicates, keeping search logic reusable across entity types.

**ASSUMPTION pending clarification:** The relevance ranking approach uses PostgreSQL `ts_rank_cd` with field weights. The exact weighting scheme should be validated with the product owner once baseline search metrics are available.

## Files to Modify
- `common/src/db/query.rs` — Add full-text search helper functions: `build_tsquery` (converts user input to `tsquery`), `apply_fulltext_rank` (adds `ts_rank_cd` ordering to a query), and `apply_filters` (applies typed filter predicates to a SeaORM query)
- `common/src/db/mod.rs` — Export new full-text search and filter helper symbols if needed

## Implementation Notes
- Extend the existing query builder helpers in `common/src/db/query.rs` which already provide shared filtering, pagination, and sorting functionality
- `build_tsquery` should handle:
  - Splitting user input into lexemes
  - Combining with `&` (AND) operator for multi-word queries
  - Sanitizing input to prevent tsquery syntax errors
- `apply_fulltext_rank` should:
  - Add a `ts_rank_cd(search_vector, query)` expression to the SELECT
  - Order results by rank descending
  - Accept weight configuration parameter for per-entity customization
- `apply_filters` should:
  - Accept a generic filter struct with optional fields (entity_type, severity, date_from, date_to)
  - Apply each non-None filter as a WHERE clause
  - Compose with existing pagination from `common/src/model/paginated.rs`
- Per Key Conventions §Error handling: all helper functions should return `Result<T, AppError>` for consistency with the error handling pattern. Applies: task modifies `common/src/db/query.rs` matching the convention's Rust source file scope.
- Per Key Conventions §Query helpers: extend the existing shared query infrastructure rather than creating parallel helpers. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering, pagination, and sorting; extend these rather than duplicating
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper; full-text search results should compose with this existing pagination model
- `common/src/error.rs` — `AppError` enum for consistent error handling

## Acceptance Criteria
- [ ] `build_tsquery` converts user search input into a valid PostgreSQL `tsquery`
- [ ] `build_tsquery` sanitizes input to prevent injection or syntax errors
- [ ] `apply_fulltext_rank` adds ts_rank_cd ordering to a SeaORM select
- [ ] `apply_filters` applies optional filter predicates (entity type, severity, date range) to a query
- [ ] All helpers compose with existing pagination and sorting from `common/src/db/query.rs`
- [ ] Helper functions return `Result<T, AppError>` following the project error handling convention

## Test Requirements
- [ ] Unit test: `build_tsquery` correctly converts single-word input
- [ ] Unit test: `build_tsquery` correctly converts multi-word input with AND semantics
- [ ] Unit test: `build_tsquery` sanitizes special characters in user input
- [ ] Unit test: `apply_filters` applies entity type filter correctly
- [ ] Unit test: `apply_filters` applies date range filter correctly
- [ ] Unit test: `apply_filters` skips None filter fields (no WHERE clause added)

## Dependencies
- Depends on: Task 1 — Add full-text search migration (tsvector columns must exist for rank queries to reference)
