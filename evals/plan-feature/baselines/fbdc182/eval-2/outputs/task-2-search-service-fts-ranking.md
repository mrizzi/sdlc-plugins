## Repository
trustify-backend

## Description
Refactor `SearchService` in `modules/search/src/service/mod.rs` to execute PostgreSQL full-text search queries using the `search_vector` generated columns added in Task 1, and order results by `ts_rank` descending. This replaces any existing `ILIKE`-based or unranked search with relevance-ranked results, addressing the "results should be more relevant" MVP requirement.

**Assumptions pending clarification**:
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs text matching across SBOM, advisory, and package entities. If it delegates to per-entity services (e.g. `SbomService`, `AdvisoryService`) rather than querying directly, this task may need to extend those services as well — that will be confirmed during implementation.
- `ts_rank` ordering alone is treated as sufficient for relevance. Domain-specific boosting (e.g. weighting advisory severity higher) is out of scope until specified.
- The search query from the client is treated as a plain-text input and converted to a `tsquery` using `plainto_tsquery('english', $1)` to handle multi-word queries safely.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace current search query logic with `tsvector @@ tsquery` predicate and `ts_rank` ordering

## Implementation Notes
Use SeaORM's `query_by_statement` or `Statement::from_sql_and_values` to execute the raw SQL search query, since SeaORM's query builder does not natively support `@@` and `ts_rank`. Follow the error-handling pattern used throughout the codebase: wrap database errors with `.context("search query failed")` and return `Result<_, AppError>` from `common/src/error.rs`.

The core query pattern for each entity type:

```sql
SELECT *, ts_rank(search_vector, plainto_tsquery('english', $1)) AS rank
FROM sbom
WHERE search_vector @@ plainto_tsquery('english', $1)
ORDER BY rank DESC
LIMIT $2 OFFSET $3;
```

Repeat the same pattern for `advisory` and `package` tables, then merge and re-rank results before returning. If the current implementation returns a union of entity results, maintain that structure but apply per-entity ranking before merging.

Use `common/src/model/paginated.rs`'s `PaginatedResults<T>` as the return type for the merged result set, consistent with all other list endpoints in the codebase.

Use `common/src/db/query.rs` helpers for pagination parameters (limit/offset extraction) rather than duplicating that logic.

## Reuse Candidates
- `common/src/db/query.rs` — existing pagination and query builder helpers; use for limit/offset extraction from request parameters
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper; use as the return type for search results
- `common/src/error.rs::AppError` — error type; all service methods must return `Result<_, AppError>`
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` for reference on how the existing service layer constructs SeaORM queries and wraps results in `PaginatedResults`
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` for same reference pattern

## Acceptance Criteria
- [ ] A search query for a term present in SBOM names returns those SBOMs ranked higher than SBOMs where the term appears only in the description
- [ ] A search query for a term that matches no documents returns an empty `PaginatedResults` with `total: 0`, not an error
- [ ] The service compiles and all existing `tests/api/search.rs` integration tests pass
- [ ] Search queries against the GIN index are measurably faster than sequential scans for datasets of >= 1,000 rows (verified via `EXPLAIN ANALYZE` during development)

## Test Requirements
- [ ] Update `tests/api/search.rs` to assert that results are returned in relevance order for a controlled dataset (insert documents where ranking is predictable, then assert the order of results)
- [ ] Test empty-query behavior: a blank or whitespace-only query should return an appropriate error or empty result, not a PostgreSQL syntax error from an empty `tsquery`
- [ ] Test that results include all three entity types (SBOM, advisory, package) when the query term appears in each

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass
- `cargo build` — project compiles without warnings in the search module

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration (requires `search_vector` columns to exist)
