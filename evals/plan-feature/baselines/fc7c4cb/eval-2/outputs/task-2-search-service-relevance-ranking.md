## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search with relevance ranking instead of the current search implementation. This improves search result quality by ranking results based on text match relevance using `ts_rank` and supports weighted field matching (e.g., name/title weighted higher than description).

**Ambiguity note:** The feature description (TC-9002) states results should be "more relevant" but provides no definition of relevance, no ranking algorithm, and no examples of expected search behavior. This task assumes PostgreSQL `ts_rank` with weighted fields is the appropriate approach. The product owner should provide concrete examples of searches that currently return poor results and define the expected ranking behavior.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor `SearchService` to use `to_tsquery`/`ts_rank` for full-text search with relevance-based ordering
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint handler to pass-through ranking parameters and return results ordered by relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: Response results are now ordered by relevance score (descending) by default. No breaking change to request parameters; adds optional `sort=relevance` parameter (default behavior).

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor it to use PostgreSQL `to_tsquery` for query parsing and `ts_rank` for scoring results.
- Use weighted ranking: assign weight A to name/title fields and weight B to description fields, following PostgreSQL `setweight` conventions.
- Integrate with the existing query builder helpers in `common/src/db/query.rs` for consistent query construction. The `query.rs` module already provides shared filtering, pagination, and sorting helpers — extend or reuse these for relevance sorting.
- Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`, consistent with all list endpoints in the codebase.
- Follow the error handling pattern using `Result<T, AppError>` with `.context()` wrapping as defined in `common/src/error.rs`.
- Reference the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for how list endpoints are structured.

**Assumption (pending clarification):** Weight distribution (A for title, B for description) is assumed. The product owner should validate whether this weighting produces acceptable results for real-world queries.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Existing filtering, pagination, and sorting utilities that should be extended for relevance-based sorting rather than creating new query logic
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper already used by all list endpoints; must be reused for search results
- `common/src/error.rs::AppError` — Error type used across all handlers; reuse for consistent error handling

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`to_tsquery`/`ts_rank`) for query execution
- [ ] Search results are ranked by relevance score in descending order by default
- [ ] The search endpoint continues to return `PaginatedResults<T>` with pagination support
- [ ] Existing search functionality is not broken — queries that worked before continue to return results
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that search returns results ranked by relevance (a query matching a title should rank higher than a description-only match)
- [ ] Integration test verifying that pagination continues to work with relevance-ranked results
- [ ] Integration test verifying that empty search queries return appropriate results or error responses
- [ ] Integration test verifying that special characters in search queries are handled safely (no SQL injection, no panics)

## Dependencies
- Depends on: Task 1 — Add full-text search migration for searchable entity columns

[sdlc-workflow] Description digest: sha256:31f8fc983613a0933d838adc5f16f128d4ae25f82c81f86bb0aaf810c67802ca
