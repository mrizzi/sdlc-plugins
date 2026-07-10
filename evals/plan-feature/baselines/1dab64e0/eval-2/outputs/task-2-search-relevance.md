## Repository
trustify-backend

## Target Branch
main

## Description
Improve search result relevance by implementing scoring and ranking in the SearchService. Currently, search results are returned without relevance ordering, which causes users to see irrelevant results prominently. This task adds full-text search ranking to score results by match quality and orders them by relevance score by default.

**Ambiguity note:** The feature description (TC-9002) states "results should be more relevant" without defining relevance criteria or providing examples of good vs. bad results. This task assumes relevance means full-text search ranking (e.g., PostgreSQL `ts_rank` or equivalent SeaORM functionality) to order results by match quality, pending clarification from the feature owner on specific ranking criteria.

## Files to Modify
- `modules/search/src/service/mod.rs` — implement relevance scoring logic using full-text search ranking functions; add score-based ordering to search query results
- `modules/search/src/endpoints/mod.rs` — expose an optional `sort` query parameter to allow sorting by relevance (default) or other fields
- `tests/api/search.rs` — add integration tests verifying that results are ordered by relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort` query parameter (default: `relevance`); response items include a `score` field indicating match relevance

## Implementation Notes
The SearchService in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Enhance the search query to compute a relevance score for each result using PostgreSQL's full-text search ranking capabilities (e.g., `ts_rank`, `ts_rank_cd`). When using SeaORM, this may involve raw SQL expressions or custom select statements to include the ranking function output as a computed column.

Add the relevance score as a field in the search result model so it can be returned to the client and used for ordering. The default sort order should be descending by relevance score (highest relevance first).

Add a `sort` query parameter to the search endpoint in `modules/search/src/endpoints/mod.rs` that allows the client to choose between relevance-based sorting (default) and other sort options (e.g., by name, by date). Use Axum's `Query` extractor for parameter parsing, following the pattern in other list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.

Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs`.

All handlers must return `Result<T, AppError>` with `.context()` wrapping for error handling (see `common/src/error.rs`).

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the search module.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` handler file scope.

Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `common/src/db/query.rs::sorting helpers` — existing sorting utilities that should be extended to support relevance-based ordering rather than implementing sort logic from scratch
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService search` — example of a service that performs search operations; review its query patterns for consistency
- `common/src/model/paginated.rs::PaginatedResults<T>` — standard response wrapper; reuse for ranked search results

## Acceptance Criteria
- [ ] Search results are ordered by relevance score by default (most relevant first)
- [ ] Each search result item includes a relevance `score` field
- [ ] The `sort` query parameter allows switching between relevance-based and other sort orders
- [ ] When no search query is provided or the query is empty, results fall back to a deterministic ordering (e.g., by creation date)
- [ ] All existing search tests continue to pass without modification

## Test Requirements
- [ ] Integration test: search results for a specific query term are ordered by relevance (a result with the term in the title ranks higher than one with the term only in the body)
- [ ] Integration test: search results include a non-zero `score` field for matching results
- [ ] Integration test: `sort=relevance` produces the same ordering as the default (no sort parameter)
- [ ] Integration test: results with no search query return items in a deterministic order
