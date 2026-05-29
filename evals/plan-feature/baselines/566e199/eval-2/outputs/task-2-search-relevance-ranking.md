## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search with `ts_rank` ranking instead of naive string matching. This addresses the "results should be more relevant" requirement by ranking results based on text match quality against the tsvector indexes created by the migration task. The `GET /api/v2/search` endpoint will return results ordered by relevance score while maintaining the existing `PaginatedResults<T>` response structure.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace existing search query logic with `ts_rank`-based full-text search using the tsvector columns
- `modules/search/src/endpoints/mod.rs` — update the search endpoint handler to convert the user query to a tsquery and pass it to the updated `SearchService`

## Implementation Notes
Modify the `SearchService` in `modules/search/src/service/mod.rs` to:
1. Convert the user's search query to a tsquery using `plainto_tsquery('english', $query)` (or `websearch_to_tsquery` for more flexible syntax supporting boolean operators).
2. Filter results using `WHERE search_vector @@ tsquery` against the tsvector columns added by the migration.
3. Rank results using `ts_rank(search_vector, tsquery)` and order by rank descending.
4. Return ranked results through the existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`.

Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting integration. The existing `query.rs` module provides filtering, pagination, and sorting patterns that the new ranking logic should integrate with rather than bypass.

The search endpoint in `modules/search/src/endpoints/mod.rs` should continue to accept the existing query parameter and pass it through the updated `SearchService`. Ensure error handling follows the `Result<T, AppError>` pattern from `common/src/error.rs` with `.context()` wrapping.

Per constraints (docs/constraints.md):
- Commit messages must follow Conventional Commits and reference TC-9002 (§2.1, §2.2).
- Include `--trailer="Assisted-by: Claude Code"` on all commits (§2.3).
- Keep changes scoped to the files listed (§5.1).
- Do not duplicate existing query helper logic — reuse `common/src/db/query.rs` utilities (§5.4).

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; integrate ranking with these existing patterns rather than reimplementing pagination
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by all list endpoints; search results must use this same wrapper
- `common/src/error.rs` — `AppError` enum with `IntoResponse` implementation; follow the same error handling pattern
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` has an existing `search` method that may demonstrate current search patterns to refactor from

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`tsvector`/`tsquery`) for query matching
- [ ] Search results are ranked by `ts_rank` relevance score, most relevant first
- [ ] The `GET /api/v2/search` endpoint returns results ordered by relevance when a query is provided
- [ ] Pagination continues to work correctly with ranked results (uses `PaginatedResults<T>`)
- [ ] Existing search API contract is backward compatible — the endpoint path, query parameter name, and response structure remain unchanged
- [ ] Queries with no matches return an empty result set (not an error)

## Test Requirements
- [ ] Integration test: search with a specific term returns entities containing that term ranked higher than partial matches
- [ ] Integration test: search with no matching results returns empty `PaginatedResults` with total=0
- [ ] Integration test: search results respect pagination parameters (offset, limit) while maintaining rank order
- [ ] Integration test: search query with special characters does not cause SQL injection or errors

## Dependencies
- Depends on: Task 1 — Search indexes migration (migration must exist before the service can query tsvector columns)

[sdlc-workflow] Description digest: sha256:b6323382cef1c580239746e8b931675feb2e79dffd2ca05afdebc16afd9f7a16
