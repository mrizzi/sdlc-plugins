# Task 2 — Optimize SearchService with full-text search and relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/` to use PostgreSQL full-text search (`tsvector`/`tsquery` with `ts_rank`) instead of the current search implementation. This addresses the "search should be faster" and "results should be more relevant" requirements by leveraging the GIN indexes created in Task 1 and returning results ranked by relevance score.

**Assumption pending clarification:** The relevance ranking uses PostgreSQL's default `ts_rank` normalization. If specific ranking weights are needed (e.g., title matches weighted higher than description matches), this should be clarified with the product owner.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `tsvector`/`tsquery` with `ts_rank` scoring
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` endpoint to accept and pass through relevance parameters
- `modules/search/Cargo.toml` — add any needed dependencies if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: search query now uses full-text search internally; results are ordered by relevance score by default. Response shape adds an optional `rank` field to each result item. Backward compatible — existing callers continue to work.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor it to:
  1. Parse the user's search query into a `tsquery` using `plainto_tsquery('english', $1)` for simple queries or `websearch_to_tsquery('english', $1)` for queries with operators.
  2. Match against the `search_vector` column using the `@@` operator.
  3. Rank results using `ts_rank(search_vector, query)` and order by rank descending.
  4. Fall back to `ILIKE` matching if the tsquery produces no results (to handle partial/prefix matches that full-text search may miss).
- Use the shared query builder in `common/src/db/query.rs` for pagination and sorting. The existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` should be used for the response.
- Follow the error handling pattern using `Result<T, AppError>` with `.context()` wrapping, as established in `common/src/error.rs`.
- For SeaORM raw queries, use `sea_orm::Statement::from_string()` or `sea_orm::DatabaseBackend::Postgres` for PostgreSQL-specific SQL.
- Per `docs/constraints.md` section 5 (Code Change Rules): do not duplicate existing functionality — reuse the query helpers in `common/src/db/query.rs` for pagination and sorting.
- Per `docs/constraints.md` section 2 (Commit Rules): commits must reference TC-9002 and follow Conventional Commits.

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` — the existing search service to be refactored (not replaced); preserve its public API
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers to reuse for result pagination
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for paginated search results
- `common/src/error.rs::AppError` — error type for consistent error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how existing services query with SeaORM; follow the same patterns

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`tsvector`/`tsquery`) for query matching
- [ ] Search results are ranked by relevance using `ts_rank` and returned in descending rank order
- [ ] Search performance is improved over the previous implementation (queries use GIN indexes)
- [ ] The existing `GET /api/v2/search` endpoint continues to work with the same request format (backward compatible)
- [ ] Results include items from all three entity types: SBOMs, advisories, and packages
- [ ] Empty search queries return an appropriate response (not an error)

## Test Requirements
- [ ] Update existing integration tests in `tests/api/search.rs` to verify full-text search behavior
- [ ] Add test: search for a known term returns matching results ranked by relevance
- [ ] Add test: search for a term present in multiple entity types returns results from all matching types
- [ ] Add test: search with no matching results returns an empty paginated response (not an error)
- [ ] Add test: verify that search results are ordered by relevance (a result matching in the title ranks higher than one matching only in description)
- [ ] Verify existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — all search integration tests pass
- `EXPLAIN ANALYZE SELECT ... FROM sbom WHERE search_vector @@ plainto_tsquery('english', 'test')` — confirms GIN index is used

## Documentation Updates
- `README.md` — document the search relevance ranking behavior if the README covers API behavior

## Dependencies
- Depends on: Task 1 — Add full-text search database migration
