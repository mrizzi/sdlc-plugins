## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to use PostgreSQL full-text search with relevance scoring
via `ts_rank`, replacing any naive LIKE/ILIKE queries with proper `tsvector`/`tsquery`
matching. This addresses the "results should be more relevant" requirement from TC-9002
by ensuring search results are ranked by relevance rather than returned in arbitrary order.

ASSUMPTION (pending clarification): "More relevant" means implementing weighted
full-text search scoring using PostgreSQL's `ts_rank`, with exact matches ranked
above partial matches.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor SearchService to use `ts_rank` for full-text search scoring, replacing any existing LIKE/ILIKE pattern matching with `tsvector`/`tsquery` queries that leverage the GIN indexes created in Task 1

## Implementation Notes
The search service is in `modules/search/src/service/mod.rs` (SearchService: full-text
search across entities). Modify the search query to:

1. Convert user input to a `tsquery` using `plainto_tsquery` or `websearch_to_tsquery`
2. Match against `tsvector` columns using the `@@` operator
3. Score results using `ts_rank(tsvector_column, tsquery)` 
4. Order results by rank descending (most relevant first)
5. Support prefix matching for partial queries using `:*` suffix on terms

Use SeaORM's raw SQL query capabilities or `Expr::cust()` for PostgreSQL-specific
full-text search functions, following the query builder patterns in
`common/src/db/query.rs`.

Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`,
consistent with existing list endpoints.

All service methods must return `Result<T, AppError>` with `.context()` wrapping,
following the error handling pattern in `common/src/error.rs`.

Per CONVENTIONS.md §Error handling: All handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: List endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Shared filtering, pagination, and sorting utilities that should be reused for constructing the search query
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for paginated search results
- `common/src/error.rs::AppError` — Error type for Result return values

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of LIKE/ILIKE
- [ ] Results are scored using `ts_rank` and ordered by relevance (highest score first)
- [ ] Exact matches rank higher than partial matches
- [ ] Empty search queries return an appropriate response (empty results or validation error)
- [ ] Search continues to return results from all entity types (SBOMs, advisories, packages)
- [ ] Existing search endpoint contract is preserved (no breaking changes to response shape)

## Test Requirements
- [ ] Search for an exact term returns the matching entity ranked first
- [ ] Search for a partial term returns relevant results via prefix matching
- [ ] Search results are ordered by relevance score (most relevant first)
- [ ] Empty or whitespace-only search queries are handled gracefully
- [ ] Search across multiple entity types returns results from all matching types

## Dependencies
- Depends on: Task 1 — Add database indexes for full-text search columns
