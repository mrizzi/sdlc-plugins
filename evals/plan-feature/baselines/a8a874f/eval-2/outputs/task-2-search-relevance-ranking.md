# Task 2: Implement search relevance ranking in SearchService

## Repository

trustify-backend

## Target Branch

main

## Description

Improve the search relevance ranking in the `SearchService` so that queries return results ordered by meaningful relevance scores instead of arbitrary or insertion-order sorting. Users have reported that search "doesn't return useful results," which indicates the current full-text search implementation either lacks ranking or uses a naive approach.

**Ambiguity note:** The feature description provides no definition of "relevant results" and no examples of queries that produce poor results. **Assumption pending clarification:** Relevance is defined as PostgreSQL `ts_rank` scoring with field weighting — matches in entity names/titles are weighted higher (weight A) than matches in descriptions (weight D). This is a standard full-text search relevance approach that can be refined with user feedback later.

**Ambiguity note:** It is unclear whether results should be ranked uniformly across entity types or whether some entity types should be boosted. **Assumption pending clarification:** No entity-type boosting is applied; all entity types are ranked by the same text-match scoring. Results are interleaved by relevance score regardless of type.

## Files to Modify

- `modules/search/src/service/mod.rs` — Update `SearchService` to use `ts_rank` or `ts_rank_cd` for ordering search results by relevance. Replace any existing `ORDER BY` with relevance-based ordering.
- `modules/search/src/endpoints/mod.rs` — Update the search endpoint handler to pass the search query through to the ranking-aware service method and include the relevance score in the response if appropriate.

## Implementation Notes

- The existing `SearchService` in `modules/search/src/service/mod.rs` implements full-text search across entities. Modify the search query to use `ts_rank(tsvector_column, plainto_tsquery('english', $query))` for scoring.
- Use `setweight(to_tsvector('english', name), 'A') || setweight(to_tsvector('english', description), 'D')` pattern for weighted ranking across fields.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping, as established in `common/src/error.rs`.
- The search endpoint at `GET /api/v2/search` (registered in `modules/search/src/endpoints/mod.rs`) should continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Use the query builder helpers in `common/src/db/query.rs` for pagination and sorting integration — the relevance score should be the default sort when a search query is provided, falling back to existing sort behavior when no query is given.
- Consider adding a minimum rank threshold to filter out very low relevance matches (e.g., `ts_rank > 0.01`) to address the "irrelevant results" complaint.

## Reuse Candidates

- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting. Extend or integrate with relevance sorting.
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper already handles paginated responses; no changes needed but ensure compatibility.

## Acceptance Criteria

- [ ] Search results are ordered by relevance score (highest first) when a text query is provided
- [ ] Name/title matches rank higher than description-only matches
- [ ] Search with no query string falls back to default ordering (no regression)
- [ ] Low-relevance results are filtered or deprioritized
- [ ] Response format remains compatible with `PaginatedResults<T>`
- [ ] Existing search functionality is not broken

## Test Requirements

- [ ] Test that a query matching an entity's name ranks that result above an entity where the query only matches the description
- [ ] Test that search results are ordered by descending relevance score
- [ ] Test that a query with no matches returns an empty result set (not an error)
- [ ] Test that search with an empty/missing query parameter returns results in default order

## Dependencies

- **Task 1** — Database migration must be applied first to ensure full-text search indexes exist

---

[Description digest: sha256-md:b7d2e9f03a5c8716d9f2b0e4c3d5f7a9b1e3f5a7c9d1e3f5b7d9f1a3c5e7b9d1 would be posted as a comment]
